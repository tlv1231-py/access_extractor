import json
import logging
import pathlib
from dataclasses import dataclass

from extractor.engine.session import AccessSession
from tools.summarize import run_summarize
from extractor.extractors.controls import ControlExtractor
from extractor.extractors.events import analyze_procedure_source, resolve_event_bindings
from extractor.extractors.modules import ModuleExtractor
from extractor.extractors.queries import QueryExtractor
from extractor.extractors.relationships import RelationshipExtractor
from extractor.extractors.subforms import extract_subform_hierarchy
from extractor.extractors.tables import TableExtractor
from extractor.graph.builder import GraphBuilder
from extractor.graph.nodes import Node, NodeKind

_AC_DESIGN = 1
_AC_FORM = 2


@dataclass
class ExtractionJob:
    mdb_path: str
    output_path: str


def run_extraction(job) -> dict:
    builder = GraphBuilder()

    with AccessSession(job.mdb_path) as access:
        try:
            builder.add(*TableExtractor(access, builder).extract())
        except Exception as exc:
            logging.warning("TableExtractor failed: %s", exc)

        try:
            builder.add(*QueryExtractor(access, builder).extract())
        except Exception as exc:
            logging.warning("QueryExtractor failed: %s", exc)

        try:
            builder.add(*RelationshipExtractor(access, builder).extract())
        except Exception as exc:
            logging.warning("RelationshipExtractor failed: %s", exc)

        try:
            builder.add(*ModuleExtractor(access, builder).extract())
        except Exception as exc:
            logging.warning("ModuleExtractor failed: %s", exc)

        processed_form_names: list[str] = []
        form_module_sources: dict[str, list[str]] = {}
        try:
            all_forms = access.CurrentProject.AllForms
            for i in range(all_forms.Count):
                try:
                    form_name = all_forms(i).Name
                except Exception as exc:
                    logging.warning("Failed to read form at index %d: %s", i, exc)
                    continue
                processed_form_names.append(form_name)
                _process_form(access, form_name, builder, form_module_sources)
        except Exception as exc:
            logging.warning("Forms iteration failed: %s", exc)

        _materialize_proc_nodes(builder)

        module_sources = builder.get_module_sources()
        sorted_form_names = sorted(processed_form_names, key=len, reverse=True)
        for node in builder.nodes.values():
            if node.kind != NodeKind.Procedure:
                continue
            match = _find_source_for_proc(node.name, sorted_form_names, form_module_sources, module_sources)
            if match is None:
                continue
            matched_form, lines = match
            for edge in analyze_procedure_source(node.id, lines):
                builder.add_edge(edge)

    output = pathlib.Path(job.output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(builder.to_dict(), indent=2), encoding="utf-8")

    summary = _summary(builder)
    try:
        paths = run_summarize(output)
        summary["summary_md"]   = str(paths["summary_md"])
        summary["compact_json"] = str(paths["compact_json"])
        summary["index_json"]   = str(paths["index_json"])
    except Exception as exc:
        logging.warning("Summarizer failed: %s", exc)

    return summary


# ------------------------------------------------------------------
# Helpers


def _process_form(
    access, form_name: str, builder: GraphBuilder,
    form_module_sources: dict[str, list[str]],
) -> None:
    if form_name.startswith("~") or form_name.startswith("USys"):
        return

    try:
        access.DoCmd.OpenForm(form_name, _AC_DESIGN)
    except Exception as exc:
        logging.warning("Skipping form %r (failed to open in design mode): %s", form_name, exc)
        return

    try:
        form = access.Forms(form_name)

        try:
            source = form.Module.Lines(1, form.Module.CountOfLines)
            form_module_sources[form_name] = source.splitlines()
        except Exception:
            form_module_sources[form_name] = []

        builder.add(*extract_subform_hierarchy(form, form_name, builder))

        ctrl_nodes, ctrl_edges = ControlExtractor(
            access, builder, form, f"form:{form_name}"
        ).extract()
        builder.add(ctrl_nodes, ctrl_edges)

        for node in ctrl_nodes:
            if node.properties.get("events"):
                builder.add(*resolve_event_bindings(node, builder))

    except Exception as exc:
        logging.warning("Error processing form %r: %s", form_name, exc)
    finally:
        try:
            access.DoCmd.Close(_AC_FORM, form_name)
        except Exception:
            pass


def _materialize_proc_nodes(builder: GraphBuilder) -> None:
    """Create Procedure nodes for every proc: ID referenced in edges."""
    for edge in builder.edges:
        if edge.dst.startswith("proc:") and not builder.has_node(edge.dst):
            proc_name = edge.dst.removeprefix("proc:")
            builder.add_node(Node(
                id=edge.dst,
                kind=NodeKind.Procedure,
                name=proc_name,
            ))


def _find_source_for_proc(
    proc_name: str,
    sorted_form_names: list[str],
    form_module_sources: dict[str, list[str]],
    module_sources: dict[str, list[str]],
) -> tuple[str, list[str]] | None:
    # sorted_form_names is pre-sorted longest-first so the first match is most specific.
    # proc_name is "FormName_CtrlName_EventName" where FormName may contain spaces.
    for form_name in sorted_form_names:
        if proc_name.startswith(form_name + "_"):
            # Form class module takes priority over standalone modules
            source = form_module_sources.get(form_name) or module_sources.get(form_name)
            if source:
                return form_name, source
    return None


def _summary(builder: GraphBuilder) -> dict:
    counts: dict[NodeKind, int] = {}
    for node in builder.nodes.values():
        counts[node.kind] = counts.get(node.kind, 0) + 1

    return {
        "forms": counts.get(NodeKind.Form, 0),
        "tables": counts.get(NodeKind.Table, 0),
        "queries": counts.get(NodeKind.Query, 0),
        "modules": counts.get(NodeKind.Module, 0),
        "nodes_total": len(builder.nodes),
        "edges_total": len(builder.edges),
    }

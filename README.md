# Access Extractor

A compiler-grade reverse-engineering engine for Microsoft Access databases (`.accdb` / `.mdb`). Extracts structural and behavioral intelligence into a structured knowledge graph for AI reasoning, migration tooling, and automatic documentation.

## What It Does

Most Access tooling tells you *what exists*. This tells you *how it behaves*.

The extractor produces a full runtime intelligence model:

- **Structural graph** — tables, queries, relationships, modules
- **Form hierarchy** — recursive subform nesting, tab controls, embedded children
- **Control metadata** — every control on every form with coordinates, bindings, and state
- **Event binding graph** — OnClick, AfterUpdate, OnLoad, etc. resolved to VBA procedures or macros
- **VBA static analysis** — traces `DoCmd.OpenForm`, `DoCmd.RunQuery`, control modifications, and procedure calls across the codebase
- **AI summary pipeline** — compresses a 2MB Access database into ~23k tokens of structured, queryable knowledge

## Output

Running the extractor produces `access_compiled.json` — a graph document containing:

```json
{
  "nodes": [...],       // Form, Control, Query, Table, Module, Event, Procedure, Macro
  "edges": [...],       // CONTAINS, EVENT_TRIGGERS, EVENT_OPENS_FORM, CALLS, EMBEDS_SUBFORM, ...
  "hierarchy": {...},   // Nested subform tree
  "structural": {...}   // Tables, queries, relationships
}
```

Running the summarizer produces three AI-optimized files:

| File | Size | Purpose |
|---|---|---|
| `access_summary.md` | ~42KB | Natural language app overview, data model, navigation flows |
| `access_graph_compact.json` | ~200KB | Stripped graph — forms, procedures, and behavioral edges only |
| `access_index.json` | ~81KB | Per-form lookup: events, controls, subforms, field bindings |

## Architecture

```
[ Tkinter UI ]
      ↓
[ run_extraction(job) ]
      ↓
[ AccessSession (COM) ]
      ↓
[ Extractors: tables, queries, relationships, modules, forms, subforms, controls, events ]
      ↓
[ GraphBuilder → nodes + edges + hierarchy ]
      ↓
[ access_compiled.json ]
      ↓
[ tools/summarize.py → summary + compact graph + index ]
```

The UI layer is strictly thin — all Access intelligence lives in the extractor engine.

## Requirements

- Windows (COM/win32 required)
- Microsoft Access installed
- Python 3.9+
- `pywin32`

```bash
pip install pywin32
```

## Usage

```bash
# Run the UI
python main.py

# Or run the summarizer directly against an existing compiled JSON
python tools/summarize.py path/to/access_compiled.json
```

## Edge Types

| Edge | Meaning |
|---|---|
| `CONTAINS` | Form → Control |
| `EMBEDS_SUBFORM` | Control → Child Form |
| `EVENT_TRIGGERS` | Event → VBA Procedure or Macro |
| `EVENT_OPENS_FORM` | Procedure → Form/Report opened via DoCmd |
| `EVENT_RUNS_QUERY` | Procedure → Query executed via DoCmd |
| `EVENT_MODIFIES` | Procedure → Control property changed |
| `CALLS` | Procedure → Procedure |
| `DEPENDS_ON` | Table → Table (relationship) |
| `REFERENCES` | Control → Field/Query (control source) |

## Use Cases

- **AI-assisted migration** — feed the summary + index to an LLM to reason about the app
- **Dead code detection** — controls with no events and no control source
- **Impact analysis** — trace what breaks if a table field changes
- **Automatic documentation** — generate human-readable app descriptions
- **Graph database import** — nodes/edges map directly to Neo4j or similar

## AI Usage

The summarizer produces three files designed to be attached to an AI assistant (e.g. a Claude project). Each serves a distinct purpose:

**`access_summary.md`**
> "Use this file to orient yourself on the application. It contains the data model, form hierarchy, navigation flows, key logic hubs, and dead controls. Read this first before answering any question."

**`access_index.json`**
> "Use this file to answer questions about specific forms. For any form name, look up its events, controls, subforms, and field bindings here."

**`access_graph_compact.json`**
> "Use this file only when tracing cross-form dependencies — which procedures call which, which events open which forms. Do not load this whole file; query it for specific nodes."

**Recommended context budget:**
- Most questions: summary + index (~30k tokens)
- Dependency tracing: add compact graph (~50k tokens additional)
- Full load: ~80k tokens, fits comfortably in a 200k context window
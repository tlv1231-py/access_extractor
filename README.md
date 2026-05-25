# Access Extractor

**AI-native extraction and context engine for Microsoft Access databases.**

Extract schema, forms, queries, VBA, and object relationships from `.accdb`/`.mdb` files into structured JSON — then serve that context to LLMs and AI agents via a versioned SDK.

---

## What It Does

Most Access tooling is ancient, migration-focused, and AI-unaware.

This tool is different:

- Extracts a full object dependency graph (tables, forms, controls, events, VBA procedures, queries, relationships)
- Builds AI-readable context packs (summary markdown, compact graph, per-form event index)
- Pushes exports to a GitHub repo as a versioned storage layer
- Serves context to LLMs via a built-in SDK with caching, version pinning, and token-efficient slicing

.accdb / .mdb
↓
Access Extractor
↓
Structured JSON exports
↓
GitHub (versioned storage)
↓
context-sdk → LLM / AI Agent

---

## Features

### Extraction
- Tables (fields, types, record counts)
- Queries (SQL)
- Relationships
- Forms and subform hierarchy
- Controls and control sources
- VBA events and procedure bindings
- Standalone VBA modules
- Full object dependency graph (nodes + edges)

### Output Files
| File | Purpose |
|------|---------|
| `<db>.json` | Full compiled object graph |
| `access_summary.md` | Human-readable overview |
| `access_graph_compact.json` | Stripped graph for AI ingestion |
| `access_index.json` | Per-form event and subform index |

### Context SDK
- Load context files from GitHub with one line
- Version pinning (branch, tag, or commit SHA)
- Two-tier cache (memory + optional disk)
- Merge multiple databases into one context
- Token-efficient slicing for LLM prompt injection

---

## Quickstart

### 1. Install

```bash
git clone https://github.com/tlv1231-py/access_extractor
cd access_extractor
pip install -e .
```

### 2. Run the UI

```bash
python main.py
```

- Select your `.accdb` or `.mdb` file
- Select an output folder
- Optionally enter a GitHub repo and token to auto-push exports
- Hit Run

### 3. Use the SDK

```python
from context_sdk import ContextEngine

engine = ContextEngine(repo="your-org/your-exports-repo", token="ghp_...")
ctx = engine.load_context("ai_context/access_graph_compact.json")

prompt_block = engine.slice_for_prompt(
    ctx,
    keys=["tables", "forms"],
    prefix="## Database Schema",
)
```

---

## Repository Structure

access_extractor/
├── extractor/          # Extraction engine
│   ├── engine/         # Runner, compiler, session
│   ├── extractors/     # Tables, forms, queries, VBA, relationships
│   └── graph/          # Node/edge graph builder
├── context_sdk/        # Context engine SDK
│   ├── core/           # ContextEngine, GitHubClient
│   ├── cache/          # Two-tier cache
│   ├── schema/         # ContextEnvelope, metadata models
│   └── context/        # Merger, slicer
├── publisher/          # GitHub publishing layer
├── tools/              # Summarizer
├── ui/                 # Tkinter UI
└── examples/           # Usage examples

---

## CLI

```bash
# Fetch a context file
context-sdk fetch org/repo ai_context/access_graph_compact.json

# Fetch specific keys only
context-sdk fetch org/repo ai_context/access_graph_compact.json --keys tables forms

# List available context files
context-sdk list org/repo ai_context/

# Pin current HEAD to a SHA for deterministic loads
context-sdk pin org/repo

# Merge multiple context files
context-sdk merge org/repo ai_context/access_graph_compact.json ai_context/access_index.json
```

---

## Using with Claude (AI Context Setup)

After pushing exports to a private GitHub repo, you can configure Claude to use them as live database context.

### Claude Project Instructions Template

Add the following to your Claude Project instructions, customized for your repo:

~~~
## Database Context

You have access to live exports from a Microsoft Access database.
Always use these exports as the authoritative source for schema, forms, queries, and VBA.
Never guess at table names, field names, or form structure — read from the exports.

### Repository
Repository: your-org/your-exports-repo
Files under ai_context/:
- access_graph_compact.json — primary reference for tables, forms, procedures
- access_index.json — per-form events, controls, subforms, bound fields
- access_summary.md — counts and overview
- <dbname>.json — full compiled graph (deep analysis only)

### Loading Rules
- Default to access_graph_compact.json for schema and structure questions
- Use access_index.json for form behavior and event questions
- Never load all files at once unless explicitly asked
- Only load the full compiled JSON when compact and index files are insufficient
- When a file is loaded, confirm which file was used

### Behavior
- Treat exports as ground truth
- Validate all table and field names against exports before writing VBA or queries
- When exports appear outdated, flag it and suggest running a fresh extraction
~~~

### Multiple Databases
If you have separate frontend and backend databases, create separate private repos
for each and reference both in your Claude Project instructions with clear labels.

### Token Efficiency Tips
- The compact graph is 80-90% smaller than the full compiled JSON
- Use get_context_slice() in the SDK to further reduce tokens per query
- SHA-pin your ref in production for deterministic, cached context loads

---

## Requirements

- Python 3.11+
- Microsoft Access must be installed (extraction uses COM automation)
- Zero required dependencies for the SDK (stdlib only)

---

## License

MIT

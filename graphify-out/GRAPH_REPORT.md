# Graph Report - blog  (2026-07-08)

## Corpus Check
- 7 files · ~9,806 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 78 nodes · 82 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `59639e9e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 7|Community 7]]

## God Nodes (most connected - your core abstractions)
1. `Part 2 — Templates, Static Files, and Single Post View` - 14 edges
2. `Part 3 — Path Parameters, Validation, and Custom Error Handling` - 14 edges
3. `Part 1 — Getting Started` - 13 edges
4. `general_exception_handler()` - 5 edges
5. `PostBase` - 5 edges
6. `validation_exception_handler()` - 4 edges
7. `PostCreate` - 4 edges
8. `PostResponse` - 4 edges
9. `scripts` - 3 edges
10. `home()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `create_post()` --references--> `PostCreate`  [EXTRACTED]
  main.py → schemas.py

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (14): Blog — FastAPI Tutorial, Endpoints summary, Part 1 — Getting Started, Prerequisites, Project structure (Part 1), Step 1 — Create the project, Step 2 — Install FastAPI, Step 3 — Create the FastAPI application (+6 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (14): Endpoints summary (after Part 2), Part 2 — Templates, Static Files, and Single Post View, Project structure (Part 2), Running the app (Part 2), Step 1 — Install Jinja2, Step 2 — Set up Jinja2 templates, Step 3 — Serve static files, Step 4 — Set up Tailwind CSS (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (14): Endpoints summary (after Part 3), Error handling summary, Part 3 — Path Parameters, Validation, and Custom Error Handling, Project structure (Part 3), Reference, Step 1 — Separate web and API routes for a single post, Step 2 — Raise HTTPException for missing resources, Step 3 — Understand automatic path parameter validation (+6 more)

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (9): BaseModel, create_post(), get_posts(), FastAPI automatically serializes the response to JSON, PostBase, PostCreate, PostResponse, Response model for a post. ConfigDict is used to convert the model to a dictiona (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (9): JSONResponse, general_exception_handler(), home(), The code to handle the exception and return the appropriate response for both AP, show_post(), validation_exception_handler(), Request, RequestValidationError (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (8): devDependencies, tailwindcss, @tailwindcss/cli, name, private, scripts, build, dev

## Knowledge Gaps
- **46 isolated node(s):** `name`, `private`, `dev`, `build`, `@tailwindcss/cli` (+41 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Part 2 — Templates, Static Files, and Single Post View` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `Part 3 — Path Parameters, Validation, and Custom Error Handling` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **What connects `FastAPI automatically serializes the response to JSON`, `The code to handle the exception and return the appropriate response for both AP`, `name` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
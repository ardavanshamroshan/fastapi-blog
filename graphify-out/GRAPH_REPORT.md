# Graph Report - blog  (2026-07-09)

## Corpus Check
- 26 files · ~11,586 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 156 nodes · 290 edges · 12 communities (11 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `645f6ddc`
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
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `PostService` - 22 edges
2. `Post` - 17 edges
3. `UserRepository` - 17 edges
4. `User` - 16 edges
5. `PostRepository` - 14 edges
6. `Part 2 — Templates, Static Files, and Single Post View` - 14 edges
7. `Part 3 — Path Parameters, Validation, and Custom Error Handling` - 14 edges
8. `UserService` - 13 edges
9. `Part 1 — Getting Started` - 13 edges
10. `NotFoundError` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Post` --uses--> `Base`  [INFERRED]
  app/models/post.py → config/database.py
- `User` --uses--> `Base`  [INFERRED]
  app/models/user.py → config/database.py
- `PostService` --uses--> `NotFoundError`  [INFERRED]
  app/services/post_service.py → config/config.py
- `UserService` --uses--> `NotFoundError`  [INFERRED]
  app/services/user_service.py → config/config.py
- `store()` --references--> `PostCreate`  [EXTRACTED]
  routers/posts.py → app/schemas/post.py

## Import Cycles
- None detected.

## Communities (12 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (13): Endpoints summary, Part 1 — Getting Started, Prerequisites, Project structure (Part 1), Step 1 — Create the project, Step 2 — Install FastAPI, Step 3 — Create the FastAPI application, Step 4 — Run the development server (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (14): Endpoints summary (after Part 2), Part 2 — Templates, Static Files, and Single Post View, Project structure (Part 2), Running the app (Part 2), Step 1 — Install Jinja2, Step 2 — Set up Jinja2 templates, Step 3 — Serve static files, Step 4 — Set up Tailwind CSS (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (24): Blog — FastAPI Tutorial, Endpoints summary (after Part 3), Endpoints summary (after Part 4), Error handling summary, Part 3 — Path Parameters, Validation, and Custom Error Handling, Part 4 — Pydantic Schemas for Request and Response Validation, Project structure (Part 3), Project structure (Part 4) (+16 more)

### Community 3 - "Community 3"
Cohesion: 0.23
Nodes (16): create_app(), _error_page(), _is_api_request(), Depends, FastAPI, get_post_service, JSONResponse, Request (+8 more)

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (3): NotFoundError, Post, PostRepository

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (8): devDependencies, tailwindcss, @tailwindcss/cli, name, private, scripts, build, dev

### Community 8 - "Community 8"
Cohesion: 0.19
Nodes (10): ConflictError, DbSession, Exception, User, get_post_repository(), get_post_service(), get_user_repository(), get_user_service() (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.30
Nodes (10): BaseModel, get_user_service, show(), store(), PostBase, PostCreate, PostResponse, UserBase (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.19
Nodes (6): BaseSettings, Settings, Base, get_db(), DeclarativeBase, Session

## Knowledge Gaps
- **52 isolated node(s):** `name`, `private`, `dev`, `build`, `@tailwindcss/cli` (+47 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PostService` connect `Community 3` to `Community 8`, `Community 11`, `Community 4`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `UserRepository` connect `Community 8` to `Community 3`, `Community 4`, `Community 13`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `Part 2 — Templates, Static Files, and Single Post View` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `PostService` (e.g. with `NotFoundError` and `Post`) actually correct?**
  _`PostService` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Post` (e.g. with `Base` and `User`) actually correct?**
  _`Post` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `UserRepository` (e.g. with `User` and `PostService`) actually correct?**
  _`UserRepository` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `User` (e.g. with `Post` and `Base`) actually correct?**
  _`User` has 4 INFERRED edges - model-reasoned connections that need verification._
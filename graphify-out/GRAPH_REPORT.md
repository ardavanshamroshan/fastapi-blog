# Graph Report - blog  (2026-07-10)

## Corpus Check
- 26 files · ~14,804 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 200 nodes · 368 edges · 14 communities (13 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d54dcc92`
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
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `PostService` - 27 edges
2. `Part 5 — SQLAlchemy Database, ORM Models, and Dependency Injection` - 23 edges
3. `Post` - 21 edges
4. `UserRepository` - 17 edges
5. `User` - 16 edges
6. `PostRepository` - 16 edges
7. `UserService` - 15 edges
8. `NotFoundError` - 14 edges
9. `Part 2 — Templates, Static Files, and Single Post View` - 14 edges
10. `Part 3 — Path Parameters, Validation, and Custom Error Handling` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Post` --uses--> `Base`  [INFERRED]
  app/models/post.py → config/database.py
- `PostService` --uses--> `NotFoundError`  [INFERRED]
  app/services/post_service.py → config/config.py
- `User` --uses--> `Base`  [INFERRED]
  app/models/user.py → config/database.py
- `store()` --references--> `PostCreate`  [EXTRACTED]
  routers/api/posts.py → app/schemas/post.py
- `update()` --references--> `PostUpdate`  [EXTRACTED]
  routers/api/posts.py → app/schemas/post.py

## Import Cycles
- None detected.

## Communities (14 total, 1 thin omitted)

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
Cohesion: 0.38
Nodes (14): index(), show(), store(), update(), update_partial(), posts(), Depends, get_post_service (+6 more)

### Community 4 - "Community 4"
Cohesion: 0.24
Nodes (4): Post, PostRepository, Update a post partially. for fields that were not provided in the request, the f, PostUpdate

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (8): devDependencies, tailwindcss, @tailwindcss/cli, name, private, scripts, build, dev

### Community 8 - "Community 8"
Cohesion: 0.62
Nodes (5): DbSession, get_post_repository(), get_post_service(), get_user_repository(), get_user_service()

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (35): API — `routers/api/posts.py`, API — `routers/api/users.py` (new), `app/models/post.py`, `app/models/user.py`, `app/providers/database.py`, `app/providers/services.py`, `app/repositories/post_repository.py`, `app/repositories/user_repository.py` (+27 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (11): create_app(), _error_page(), _is_api_request(), BaseSettings, ConflictError, NotFoundError, Settings, Exception (+3 more)

### Community 11 - "Community 11"
Cohesion: 0.27
Nodes (10): show(), store(), BaseModel, get_user_service, PostBase, PostCreate, PostResponse, UserBase (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (6): Base, get_db(), DeclarativeBase, User, UserRepository, Session

## Knowledge Gaps
- **80 isolated node(s):** `name`, `private`, `dev`, `build`, `@tailwindcss/cli` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Part 5 — SQLAlchemy Database, ORM Models, and Dependency Injection` connect `Community 9` to `Community 2`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `PostService` connect `Community 3` to `Community 4`, `Community 8`, `Community 10`, `Community 11`, `Community 13`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Part 2 — Templates, Static Files, and Single Post View` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `PostService` (e.g. with `NotFoundError` and `Post`) actually correct?**
  _`PostService` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Post` (e.g. with `Base` and `User`) actually correct?**
  _`Post` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `UserRepository` (e.g. with `User` and `PostService`) actually correct?**
  _`UserRepository` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `User` (e.g. with `Post` and `Base`) actually correct?**
  _`User` has 4 INFERRED edges - model-reasoned connections that need verification._
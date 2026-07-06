# Blog — FastAPI Tutorial (Part 1)

A minimal blog API and HTML preview, built while following [FastAPI Full Course](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz) — Part 1.

**Part 1 goals:** install FastAPI, create a basic app, return JSON from API routes, run the server from the command line, explore automatic API docs, add dummy data, and preview HTML responses.

---

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (package manager)

---

## Step 1 — Create the project

Initialize a new Python project:

```bash
uv init blog
cd blog
```

This creates `pyproject.toml` and a virtual environment.

---

## Step 2 — Install FastAPI

Add FastAPI with the standard extras (includes Uvicorn, CLI tools, and other dev dependencies):

```bash
uv add "fastapi[standard]"
```

Your `pyproject.toml` should look like:

```toml
[project]
name = "blog"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "fastapi[standard]>=0.139.0",
]
```

`uv.lock` pins exact versions of all transitive dependencies.

---

## Step 3 — Create the FastAPI application

Create `main.py` and instantiate the app:

```python
from fastapi import FastAPI

app = FastAPI()
```

`FastAPI()` is the application object. All routes attach to it.

---

## Step 4 — Run the development server

Start the server with auto-reload:

```bash
uv run fastapi dev main.py
```

Or with Uvicorn directly:

```bash
uv run uvicorn main:app --reload
```

The app runs at **http://127.0.0.1:8000**.

---

## Step 5 — Explore automatic API documentation

FastAPI generates interactive docs from your route definitions:

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |

Only routes included in the OpenAPI schema appear here. HTML-only routes can be hidden (see Step 8).

---

## Step 6 — Add dummy post data

Before real database work (later in the series), store posts in memory:

```python
posts: list[dict] = [
    {
        "id": 1,
        "author": "John Doe",
        "title": "My First Post",
        "content": "This is my first post",
        "date_created": "2021-01-01",
        "date_updated": "2021-01-01",
        "tags": ["python", "fastapi", "blog"],
    },
    {
        "id": 2,
        "author": "Alex Smith",
        "title": "My Second Post",
        "content": "This is my second post",
        "date_created": "2021-01-02",
        "date_updated": "2021-01-02",
        "tags": ["python", "fastapi", "blog"],
    },
]
```

This is temporary in-memory storage. Later parts replace it with SQLAlchemy and a real database.

---

## Step 7 — Create a JSON API endpoint

Add a route that returns all posts as JSON:

```python
@app.get("/api/posts")
def get_posts():
    """FastAPI automatically serializes the response to JSON"""
    return posts
```

**Try it:**

```bash
curl http://127.0.0.1:8000/api/posts
```

Or open http://127.0.0.1:8000/api/posts in the browser.

FastAPI serializes Python lists and dicts to JSON. No manual `json.dumps()` needed.

---

## Step 8 — Return HTML responses

Add browser-facing pages that render HTML instead of JSON:

```python
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"
```

**Key points:**

1. **Route order matters** — FastAPI matches routes in the order they are defined.
2. **`response_class=HTMLResponse`** — tells FastAPI to return HTML, not JSON.
3. **`include_in_schema=False`** — hides these routes from `/docs` and `/redoc` (they are pages, not API endpoints).

**Try it:**

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/posts

Both show the title of the first post as a simple HTML heading.

---

## Project structure (Part 1)

```
blog/
├── main.py           # FastAPI app, routes, dummy data
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # Locked dependency versions
└── README.md         # This file
```

---

## Endpoints summary

| Method | Path | Response | In API docs |
|--------|------|----------|-------------|
| GET | `/` | HTML (first post title) | No |
| GET | `/posts` | HTML (first post title) | No |
| GET | `/api/posts` | JSON (all posts) | Yes |

---

## What we learned (Part 1)

- Set up a FastAPI project with **uv**
- Create an app with `FastAPI()`
- Define routes with `@app.get()`
- Return JSON from API endpoints (auto-serialized)
- Return HTML with `HTMLResponse`
- Run the dev server with `fastapi dev` or `uvicorn`
- Use built-in Swagger UI and ReDoc
- Store temporary data in a Python list

---

## What's next (later parts)

The full course continues with:

- SQLAlchemy database setup
- Pydantic models for validation
- Full CRUD operations
- User registration and login (password hashing, JWT)
- File uploads (profile pictures)
- Background tasks (email)
- Code organization with routers

---

## Reference

- [FastAPI Full Course — Part 1 (YouTube)](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz)
- [FastAPI documentation](https://fastapi.tiangolo.com/)

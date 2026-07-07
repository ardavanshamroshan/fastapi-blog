# Blog — FastAPI Tutorial

A minimal blog API with styled HTML pages, built while following the [FastAPI Full Course](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz) on YouTube.

| Part | Video | Topics |
|------|-------|--------|
| 1 | [Part 1](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz) | FastAPI setup, JSON API, inline HTML |
| 2 | [Part 2](https://youtu.be/G4NIB9Rx9Qs?si=ZXfoVQvaBLzCIM9K) | Jinja2 templates, static files, Tailwind CSS, single post view |

---

# Part 1 — Getting Started

**Goals:** install FastAPI, create a basic app, return JSON from API routes, run the server from the command line, explore automatic API docs, add dummy data, and preview HTML responses.

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

---

# Part 2 — Templates, Static Files, and Single Post View

**Goals:** replace inline HTML strings with Jinja2 templates, serve CSS/JS/images via static files, style the site with Tailwind CSS, list all posts on a home page, and add a single-post detail page with path parameters and 404 handling.

Video: [FastAPI Full Course — Part 2](https://youtu.be/G4NIB9Rx9Qs?si=ZXfoVQvaBLzCIM9K)

---

## Step 1 — Install Jinja2

FastAPI's template support is built on Jinja2. Add it explicitly:

```bash
uv add jinja2
```

`fastapi[standard]` already pulls Jinja2 in transitively, but pinning it in `pyproject.toml` makes the dependency explicit:

```toml
dependencies = [
    "fastapi[standard]>=0.139.0",
    "jinja2>=3.1.6",
]
```

---

## Step 2 — Set up Jinja2 templates

Import `Jinja2Templates` and point it at a `templates/` directory:

```python
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
```

Create the folder structure:

```
templates/
├── layout.html   # base layout (header, footer, sidebar)
├── home.html     # post list page
└── post.html     # single post page
```

---

## Step 3 — Serve static files

Mount a `static/` directory so CSS, JavaScript, images, and icons are served at `/static/...`:

```python
from fastapi.staticfiles import StaticFiles

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
```

**Important:** mount static files **before** defining routes that might conflict, or keep the `/static` prefix distinct.

```
static/
├── css/
│   ├── input.css     # Tailwind source (you edit this)
│   └── main.css      # compiled output (generated)
├── js/
│   └── utils.js      # theme toggle, mobile nav
├── icons/            # favicon, PWA icons
├── profile_pics/
│   └── default.jpg
└── site.webmanifest
```

---

## Step 4 — Set up Tailwind CSS

Install Node dependencies for the Tailwind CLI:

```bash
npm install
```

`package.json` defines two scripts:

```json
{
  "scripts": {
    "dev": "tailwindcss -i ./static/css/input.css -o ./static/css/main.css --watch",
    "build": "tailwindcss -i ./static/css/input.css -o ./static/css/main.css --minify"
  }
}
```

Run the CSS watcher in a separate terminal while developing:

```bash
npm run dev
```

`static/css/input.css` imports Tailwind and scans your templates for class names:

```css
@import "tailwindcss";

@source "../../templates/**/*.html";
```

The compiled file is `static/css/main.css`, linked from `layout.html`:

```html
<link rel="stylesheet" type="text/css" href="/static/css/main.css">
```

---

## Step 5 — Create a base layout template

`layout.html` defines the shared page shell — header, navigation, sidebar, footer — using Jinja2 **blocks**:

```html
<title>{% block title %}FastAPI Blog{% endblock title %}</title>

<main>
    {% block content %}
    {% endblock content %}
</main>
```

Child templates extend the layout and fill in blocks:

```html
{% extends "layout.html" %}

{% block title %}Posts — Blog{% endblock title %}

{% block content %}
    <!-- page-specific HTML -->
{% endblock content %}
```

The layout also includes:

- Google Fonts (Inter)
- Favicon and PWA manifest links
- Theme toggle (light / dark / system) via `utils.js`
- Responsive mobile navigation

---

## Step 6 — Build the home page (post list)

Replace the inline `f"<h1>..."` HTML with `TemplateResponse`:

```python
@app.get(path="/", include_in_schema=False, name="home.index")
@app.get(path="/posts", include_in_schema=False, name="home.posts")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"posts": posts},
    )
```

**Key changes from Part 1:**

| Part 1 | Part 2 |
|--------|--------|
| `response_class=HTMLResponse` | `TemplateResponse` (returns HTML automatically) |
| `return f"<h1>..."` | `return templates.TemplateResponse(...)` |
| No `request` param | `request: Request` required for templates |
| No route names | `name="home.posts"` for `url_for()` |

`home.html` loops over posts with Jinja2:

```html
{% for post in posts %}
<article class="post-card group">
    <a href="{{ url_for('posts.show', post_id=post.id) }}">
        <h2 class="post-title">{{ post.title }}</h2>
        <p class="post-excerpt">{{ post.content }}</p>
        {% for tag in post.tags %}
        <span class="badge badge-secondary">{{ tag }}</span>
        {% endfor %}
    </a>
</article>
{% endfor %}
```

**Try it:** http://127.0.0.1:8000/posts

---

## Step 7 — Name your routes for `url_for()`

Add `name=` to route decorators so templates can generate URLs without hardcoding paths:

```python
@app.get(path="/api/posts", name="posts.index")
def get_posts():
    return posts

@app.get(path="/api/posts/{post_id}", name="posts.show")
def get_post(request: Request, post_id: int):
    ...
```

In templates:

```html
<a href="{{ url_for('home.posts') }}">Back to posts</a>
<a href="{{ url_for('posts.show', post_id=post.id) }}">{{ post.title }}</a>
```

`url_for('posts.show', post_id=2)` → `/api/posts/2`

---

## Step 8 — Add a single post view with path parameters

Add a route that accepts a `post_id` path parameter:

```python
from fastapi.exceptions import HTTPException

@app.get(path="/api/posts/{post_id}", name="posts.show")
def get_post(request: Request, post_id: int):
    post = next(
        (post for post in posts if post["id"] == post_id),
        None,
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": post},
    )
```

**How it works:**

1. FastAPI converts `{post_id}` in the URL to an `int` automatically.
2. `next(..., None)` finds the matching post or returns `None`.
3. `HTTPException(404)` returns a proper error when the ID does not exist.
4. `post.html` extends `layout.html` and overrides `title`, `description`, and `content` blocks.

**Try it:**

- http://127.0.0.1:8000/api/posts/1 — first post
- http://127.0.0.1:8000/api/posts/2 — second post
- http://127.0.0.1:8000/api/posts/99 — 404 Not Found

---

## Step 9 — Add client-side interactivity

`static/js/utils.js` handles:

- **Theme switching** — light, dark, or system preference (persisted in `localStorage`)
- **Mobile nav toggle** — hamburger menu on small screens
- **Theme menu dropdown** — open/close with click-outside handling

Loaded at the bottom of `layout.html`:

```html
<script src="/static/js/utils.js"></script>
```

---

## Project structure (Part 2)

```
blog/
├── main.py
├── pyproject.toml
├── uv.lock
├── package.json
├── package-lock.json
├── templates/
│   ├── layout.html
│   ├── home.html
│   └── post.html
├── static/
│   ├── css/
│   │   ├── input.css
│   │   └── main.css
│   ├── js/
│   │   └── utils.js
│   ├── icons/
│   ├── profile_pics/
│   └── site.webmanifest
└── README.md
```

---

## Running the app (Part 2)

You need **two terminals** during development:

**Terminal 1 — Tailwind watcher:**

```bash
npm run dev
```

**Terminal 2 — FastAPI server:**

```bash
uv run fastapi dev main.py
```

---

## Endpoints summary (after Part 2)

| Method | Path | Response | In API docs | Route name |
|--------|------|----------|-------------|------------|
| GET | `/` | HTML (post list) | No | `home.index` |
| GET | `/posts` | HTML (post list) | No | `home.posts` |
| GET | `/api/posts` | JSON (all posts) | Yes | `posts.index` |
| GET | `/api/posts/{post_id}` | HTML (single post) | Yes | `posts.show` |

---

## What we learned (Part 2)

- Render HTML with **Jinja2** via `Jinja2Templates` and `TemplateResponse`
- Serve assets with **`StaticFiles`** mount at `/static`
- Use **template inheritance** (`extends`, `block`) for shared layouts
- Loop and filter data in templates (`{% for %}`, `{{ variable }}`)
- Generate URLs with **`url_for()`** and named routes
- Accept **path parameters** (`{post_id}`) with automatic type conversion
- Return **404 errors** with `HTTPException`
- Style pages with **Tailwind CSS** (CLI build from `input.css` → `main.css`)
- Add client-side behavior with vanilla JavaScript

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
- [FastAPI Full Course — Part 2 (YouTube)](https://youtu.be/G4NIB9Rx9Qs?si=ZXfoVQvaBLzCIM9K)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Jinja2 documentation](https://jinja.palletsprojects.com/)
- [Tailwind CSS documentation](https://tailwindcss.com/docs)

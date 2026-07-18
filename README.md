# Blog — FastAPI Tutorial

A minimal blog API with styled HTML pages, built while following the [FastAPI Full Course](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz) on YouTube.

| Part | Video | Topics |
|------|-------|--------|
| 1 | [Part 1](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz) | FastAPI setup, JSON API, inline HTML |
| 2 | [Part 2](https://youtu.be/G4NIB9Rx9Qs?si=ZXfoVQvaBLzCIM9K) | Jinja2 templates, static files, Tailwind CSS, single post view |
| 3 | [Part 3](https://youtu.be/WRjXIA5pMtk?si=n6uJOrhtggajfJKz) | Path parameters, API vs web routes, validation errors, custom exception handlers |
| 4 | [Part 4](https://youtu.be/9GHxnttXxrA?si=a0H4pr6UwjQeoKkm) | Pydantic schemas, field validation, `response_model`, POST create |
| 5 | [Part 5](https://youtu.be/NvOV3ig2tGY?si=SYpgR6_fNCHQy3Ba) | SQLAlchemy, SQLite, ORM models, repositories, services, dependency injection |
| 6 | [Part 6](https://youtu.be/VyoGAoxQhxM?si=9gPDm9_53fXVvLQg) | PUT / PATCH / DELETE, partial updates, cascade delete |
| 7 | [Part 7](https://youtu.be/2JPDt-Jp6fM?si=4OlTPXFiG1TvSDqY) | Sync vs async, async SQLAlchemy, aiosqlite, await everywhere |
| 8 | [Part 8](https://youtu.be/NkgIHa6KtHg?si=PiDtpeWly1twPCP7) | `APIRouter`, split routes into modules, `include_router` |
| 9 | [Part 9](https://youtu.be/vqjZOyT4QRs?si=1cDeYpf-DUCGQEoa) | Interactive frontend, Fetch API, modal forms, create/edit/delete in browser |

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

# Part 3 — Path Parameters, Validation, and Custom Error Handling

**Goals:** use path parameters in FastAPI to build dynamic routes that fetch specific resources from your data. Split single-post access into a JSON API endpoint and a browser-facing template page. Add type validation with `HTTPException` for missing resources, and register custom exception handlers that return JSON for API routes and styled HTML error pages for web routes.

Video: [FastAPI Full Course — Part 3](https://youtu.be/WRjXIA5pMtk?si=n6uJOrhtggajfJKz)

---

## Step 1 — Separate web and API routes for a single post

In Part 2, the single-post route lived under `/api/posts/{post_id}` but returned HTML. Part 3 splits responsibilities:

| Client | Path | Response |
|--------|------|----------|
| Browser | `/posts/{post_id}` | HTML (`post.html`) |
| API | `/api/posts/{post_id}` | JSON (post dict) |

**Web route** — renders the template:

```python
from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


@app.get(path="/posts/{post_id}", name="posts.show", include_in_schema=False)
def show_post(request: Request, post_id: int):
    post = next(
        (post for post in posts if post["id"] == post_id),
        None,
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": post},
    )
```

**API route** — returns JSON:

```python
@app.get(path="/api/posts/{post_id}", name="api.posts.show")
def get_post(post_id: int) -> dict:
    post = next(
        (post for post in posts if post["id"] == post_id),
        None,
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return post
```

**Key points:**

1. **`{post_id}` in the path** — FastAPI extracts the URL segment and passes it as a function argument.
2. **`post_id: int`** — FastAPI validates the type automatically. `/posts/abc` fails validation before your handler runs.
3. **`name="posts.show"`** — used by `url_for()` in `home.html` to link to `/posts/1`, not the API path.
4. **`include_in_schema=False`** on the web route — keeps browser pages out of `/docs`.

**Try it:**

| URL | Expected |
|-----|----------|
| http://127.0.0.1:8000/posts/1 | HTML single post |
| http://127.0.0.1:8000/posts/99 | 404 (styled HTML error page) |
| http://127.0.0.1:8000/api/posts/1 | `{"id": 1, "title": "...", ...}` |
| http://127.0.0.1:8000/api/posts/99 | 404 JSON `{"detail": "Post not found"}` |
| http://127.0.0.1:8000/posts/abc | 422 validation error |

Update `home.html` links to use the web route name:

```html
<a href="{{ url_for('posts.show', post_id=post.id) }}">
```

`url_for('posts.show', post_id=2)` → `/posts/2`

---

## Step 2 — Raise HTTPException for missing resources

When a post ID does not exist, raise `HTTPException` instead of returning `None` or an empty response:

```python
from fastapi import status
from fastapi.exceptions import HTTPException

if not post:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found",
    )
```

**Why `HTTPException`?**

- Sets the correct HTTP status code (404, 403, 400, etc.)
- Carries a `detail` message for clients
- Integrates with FastAPI's exception-handling pipeline
- Works for both API and web routes — your custom handler decides the response format

Use `status.HTTP_404_NOT_FOUND` instead of bare `404` for readability and consistency.

---

## Step 3 — Understand automatic path parameter validation

FastAPI validates path parameters against your type annotations before the route handler executes.

```python
def show_post(request: Request, post_id: int):  # post_id must be an int
```

| Request | Result |
|---------|--------|
| `/posts/1` | Handler runs with `post_id=1` |
| `/posts/abc` | `RequestValidationError` — not a valid integer |
| `/posts/1.5` | `RequestValidationError` — not a valid integer |

Without a custom handler, FastAPI returns a default JSON 422 response even for browser routes. Part 3 fixes that next.

---

## Step 4 — Register a custom HTTP exception handler

By default, `HTTPException` always returns JSON. For a blog with both API clients and browser users, branch on the request path:

```python
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(StarletteHTTPException)
def general_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
) -> JSONResponse:
    message = (
        exception.detail
        if exception.detail
        else "An unexpected error occurred. Please check the request and try again."
    )

    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )
```

**How it works:**

1. **`StarletteHTTPException`** — FastAPI's `HTTPException` subclasses this. Register the handler on the Starlette base class to catch all HTTP errors.
2. **`request.url.path.startswith("/api/")`** — simple content negotiation: API paths get JSON, everything else gets HTML.
3. **`templates.TemplateResponse(..., status_code=...)`** — returns the error page with the correct HTTP status (404, 403, etc.), not 200.

**Try it:**

```bash
# API — JSON 404
curl -i http://127.0.0.1:8000/api/posts/99

# Browser — styled HTML 404
open http://127.0.0.1:8000/posts/99
```

---

## Step 5 — Handle validation errors the same way

Path parameter type failures raise `RequestValidationError`. Register a second handler with the same API-vs-web branching:

```python
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": "Unprocessable Entity",
            "message": ", ".join(error["msg"] for error in exception.errors()),
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
```

**API response** (`/api/posts/abc`) — structured error list:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "post_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "abc"
    }
  ]
}
```

**Web response** (`/posts/abc`) — styled 422 page with a human-readable message.

---

## Step 6 — Create a styled error page template

Add `templates/errors/error.html` that extends `layout.html`:

```
templates/
├── errors/
│   └── error.html    # shared error page for all HTTP errors
├── layout.html
├── home.html
└── post.html
```

The template receives three context variables from the exception handler:

| Variable | Purpose |
|----------|---------|
| `status_code` | HTTP status (404, 422, 500, …) |
| `title` | Short label (or status code) |
| `message` | Human-readable error detail |

`error.html` maps status codes to friendly headings and shows navigation back to the post list:

```html
{% extends "layout.html" %}

{% set headings = {
  404: "Page not found",
  422: "Unprocessable entity",
  500: "Internal server error",
} %}
{% set heading = headings.get(status_code, "Something went wrong") %}

{% block title %}{{ status_code }} — {{ heading }}{% endblock title %}

{% block content %}
  <h1>{{ heading }}</h1>
  <p>{{ message }}</p>
  <a href="{{ url_for('home.posts') }}">Back to posts</a>
{% endblock content %}
```

The full template in this repo also includes status badges, icons, and a "Go back" button — see `templates/errors/error.html`.

---

## Step 7 — Update imports

Part 3 adds several imports to `main.py`:

```python
from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
```

| Import | Used for |
|--------|----------|
| `status` | Named HTTP status constants (`HTTP_404_NOT_FOUND`, etc.) |
| `HTTPException` | Raising errors inside route handlers |
| `RequestValidationError` | Catching type/parsing failures |
| `JSONResponse` | Returning JSON from exception handlers |
| `StarletteHTTPException` | Registering the catch-all HTTP error handler |

---

## Project structure (Part 3)

```
blog/
├── main.py
├── pyproject.toml
├── uv.lock
├── package.json
├── templates/
│   ├── errors/
│   │   └── error.html      # styled error pages (new)
│   ├── layout.html
│   ├── home.html
│   └── post.html
├── static/
│   └── ...
└── README.md
```

---

## Endpoints summary (after Part 3)

| Method | Path | Response | In API docs | Route name |
|--------|------|----------|-------------|------------|
| GET | `/` | HTML (post list) | No | `home.index` |
| GET | `/posts` | HTML (post list) | No | `home.posts` |
| GET | `/posts/{post_id}` | HTML (single post) | No | `posts.show` |
| GET | `/api/posts` | JSON (all posts) | Yes | `api.posts.index` |
| GET | `/api/posts/{post_id}` | JSON (single post) | Yes | `api.posts.show` |

---

## Error handling summary

| Error | Trigger | API response (`/api/...`) | Web response (everything else) |
|-------|---------|---------------------------|--------------------------------|
| 404 | Post ID not found | JSON `{"detail": "Post not found"}` | `errors/error.html` with 404 |
| 422 | Invalid `post_id` type (e.g. `abc`) | JSON `{"detail": [...]}` | `errors/error.html` with 422 |
| Other HTTP errors | `HTTPException` with any status | JSON `{"detail": "..."}` | `errors/error.html` with matching status |

---

## What we learned (Part 3)

- Use **path parameters** (`{post_id}`) to build dynamic routes that fetch specific resources
- Let FastAPI **validate types** automatically from function annotations (`post_id: int`)
- **Split API and web routes** — JSON at `/api/posts/{post_id}`, HTML at `/posts/{post_id}`
- Raise **`HTTPException`** with `status` constants for proper error responses
- Register **custom exception handlers** with `@app.exception_handler()`
- Return **JSON for API clients** and **styled HTML for browsers** based on the request path
- Handle **`RequestValidationError`** separately from HTTP errors for 422 responses
- Build a reusable **error page template** that extends the site layout

---

---

# Part 4 — Pydantic Schemas for Request and Response Validation

**Goals:** define an API contract with Pydantic models, add field-level validation (`min_length` / `max_length`), wire `response_model` on GET endpoints, and create a POST endpoint that accepts a validated body and returns a new post.

Video: [FastAPI Full Course — Part 4](https://youtu.be/9GHxnttXxrA?si=a0H4pr6UwjQeoKkm)

Schemas = API contract. FastAPI uses them for **validation**, **serialization**, and **OpenAPI docs**.

---

## Step 1 — Create `schemas.py`

Keep request/response shapes out of `main.py`. New file:

```python
from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    """Shared fields. No defaults → required."""
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=1000)
    author: str = Field(min_length=1, max_length=50)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_created: str
    date_updated: str
```

**Why three models?**

| Model | Role |
|-------|------|
| `PostBase` | Shared `title` / `content` / `author` + length rules |
| `PostCreate` | Request body for POST (client cannot set `id` or dates) |
| `PostResponse` | Response shape — adds `id`, timestamps |

Inheritance: create + response reuse base → no duplicated field definitions.

`ConfigDict(from_attributes=True)` — later ORM objects can feed response models via attributes (not only dicts).

Import in `main.py`:

```python
from schemas import PostCreate, PostResponse
```

---

## Step 2 — Field validation with `Field`

`Field(min_length=..., max_length=...)` rejects bad input before your handler runs.

| Field | Constraints |
|-------|-------------|
| `title` | 1–100 chars |
| `content` | 1–1000 chars |
| `author` | 1–50 chars |

Empty string / too-long string → **422** (your Part 3 `RequestValidationError` handler formats it).

---

## Step 3 — Add `response_model` to GET endpoints

Tell FastAPI what response JSON looks like:

```python
@app.get(
    path="/api/posts",
    response_model=list[PostResponse],
    name="api.posts.index",
)
def get_posts() -> list[dict]:
    return posts


@app.get(
    path="/api/posts/{post_id}",
    response_model=PostResponse,
    name="api.posts.show",
)
def get_post(post_id: int) -> dict:
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post
```

**What `response_model` does:**

1. **Validates** outgoing data against the schema
2. **Filters** extra keys (e.g. `tags` in dummy data not on `PostResponse` → dropped in JSON)
3. **Documents** response schema in `/docs`

Return type hint can stay `list[dict]` / `dict` — in-memory storage still uses dicts. FastAPI converts for the wire.

---

## Step 4 — Create a POST endpoint

```python
import datetime

@app.post(
    path="/api/posts",
    name="api.posts.create",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    now = datetime.datetime.today().isoformat()
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_created": now,
        "date_updated": now,
    }
    posts.append(new_post)
    return new_post
```

**Flow:**

1. Client sends JSON body
2. FastAPI parses body → `PostCreate` (fails → 422)
3. Handler builds dict, assigns `id` + timestamps (server-owned)
4. Append to in-memory `posts`
5. Return `new_post` → validated/serialized as `PostResponse`
6. Status **201 Created** (not 200)

**Try it** (Swagger at `/docs`, or curl):

```bash
curl -X POST http://127.0.0.1:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"World","author":"Ada"}'
```

Bad body (empty title):

```bash
curl -X POST http://127.0.0.1:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"","content":"World","author":"Ada"}'
```

→ 422 Unprocessable Entity.

---

## Request vs response contract

```
Client POST body          Server response
─────────────────         ─────────────────
title                     id            (server)
content                   title
author                    content
                          author
                          date_created  (server)
                          date_updated  (server)
```

Client never sends `id` / dates. Schema split enforces that.

---

## Project structure (Part 4)

```
blog/
├── main.py          # routes + exception handlers
├── schemas.py       # PostBase, PostCreate, PostResponse (new)
├── templates/
├── static/
└── ...
```

---

## Endpoints summary (after Part 4)

| Method | Path | Body | Response | Status | Route name |
|--------|------|------|----------|--------|------------|
| GET | `/` | — | HTML list | 200 | `home.index` |
| GET | `/posts` | — | HTML list | 200 | `home.posts` |
| GET | `/posts/{post_id}` | — | HTML post | 200 | `posts.show` |
| GET | `/api/posts` | — | `list[PostResponse]` | 200 | `api.posts.index` |
| GET | `/api/posts/{post_id}` | — | `PostResponse` | 200 | `api.posts.show` |
| POST | `/api/posts` | `PostCreate` | `PostResponse` | **201** | `api.posts.create` |

---

## What we learned (Part 4)

- Put API shapes in **`schemas.py`** with Pydantic `BaseModel`
- Share fields via **`PostBase`**; split **create** vs **response** models
- Constrain strings with **`Field(min_length=..., max_length=...)`**
- Use **`response_model=`** for validation, filtering, and OpenAPI docs
- Accept a validated body with **`post: PostCreate`**
- Return **201** with `status_code=status.HTTP_201_CREATED`
- Let server own **`id`** and **timestamps**

---

---

# Part 5 — SQLAlchemy Database, ORM Models, and Dependency Injection

**Goals:** replace the in-memory `posts` list with a persistent SQLite database, define SQLAlchemy ORM models with User–Post relationships, split database logic into repositories and services, wire everything with FastAPI dependency injection, and reorganize the app into a scalable layered structure.

Video: [FastAPI Full Course — Part 5](https://youtu.be/NvOV3ig2tGY?si=SYpgR6_fNCHQy3Ba)

**Why this matters:** in-memory data dies on server restart. A real database persists data. Separating ORM models, Pydantic schemas, repositories, and services keeps each layer focused and makes it easy to swap SQLite for Postgres or MySQL later.

---

## Architecture overview

```mermaid
flowchart TB
    subgraph HTTP
        Web[routers/web.py]
        API_P[routers/api/posts.py]
        API_U[routers/api/users.py]
    end

    subgraph DI["Dependency injection"]
        GP[get_post_service]
        GU[get_user_service]
        GDB[get_db]
    end

    subgraph Services
        PS[PostService]
        US[UserService]
    end

    subgraph Repos
        PR[PostRepository]
        UR[UserRepository]
    end

    subgraph DB
        Session[SQLAlchemy Session]
        SQLite[(database/blog.db)]
    end

    Web --> GP & GU
    API_P --> GP
    API_U --> GU & GP
    GP --> PS
    GU --> US
    PS --> PR & UR
    US --> UR
    PR & UR --> Session
    GDB --> Session
    Session --> SQLite
```

**Request flow (example: `GET /api/posts/1`):**

1. Router calls `post_service.get_post(1)` via `Depends(get_post_service)`
2. FastAPI resolves `get_post_service` → needs `PostRepository` + `UserRepository`
3. Those need `Session` from `get_db()`
4. `get_db()` opens a session, yields it, closes on response
5. `PostService` asks `PostRepository.get_by_id(1)`
6. Repository runs SQLAlchemy query with `joinedload(Post.author)`
7. ORM `Post` object returned → FastAPI serializes to `PostResponse` JSON

---

## Step 1 — Install new dependencies

```bash
uv add sqlalchemy pydantic-settings
```

Update `pyproject.toml`:

```toml
dependencies = [
    "fastapi[standard]>=0.139.0",
    "jinja2>=3.1.6",
    "pydantic-settings>=2.0.0",
    "sqlalchemy>=2.0.51",
]
```

| Package | Purpose |
|---------|---------|
| `sqlalchemy` | ORM, engine, sessions, models |
| `pydantic-settings` | Load config from `.env` |
| `email-validator` | Pulled transitively — required for `EmailStr` in user schemas |

---

## Step 2 — Environment configuration (`.env`)

Create `.env` in the project root (gitignored):

```env
APP_NAME=Blog

DATABASE_URL=sqlite:///./database/blog.db

TEMPLATES_DIR=templates

STATIC_URL_PREFIX=/static
STATIC_DIR=static

STORAGE_URL_PREFIX=/media
STORAGE_DIR=storage
```

Create the database directory:

```bash
mkdir -p database storage
```

`DATABASE_URL` format for SQLite: `sqlite:///./database/blog.db` (three slashes = relative file path).

For Postgres later, change to something like `postgresql://user:pass@localhost/blog` — SQLAlchemy handles both.

---

## Step 3 — Settings and shared config (`config/config.py`)

Move app-wide settings out of hardcoded values:

```python
from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class NotFoundError(Exception):
    def __init__(self, resource: str, identifier: int | str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} {identifier} not found")


class ConflictError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(validation_alias="APP_NAME")
    database_url: str = Field(validation_alias="DATABASE_URL")
    static_url_prefix: str = Field(validation_alias="STATIC_URL_PREFIX")
    storage_url_prefix: str = Field(validation_alias="STORAGE_URL_PREFIX")
    templates_dir: Path = Field(validation_alias="TEMPLATES_DIR")
    static_dir: Path = Field(validation_alias="STATIC_DIR")
    storage_dir: Path = Field(validation_alias="STORAGE_DIR")


settings = Settings()
settings.templates_dir = BASE_DIR / settings.templates_dir
settings.static_dir = BASE_DIR / settings.static_dir
settings.storage_dir = BASE_DIR / settings.storage_dir
templates = Jinja2Templates(directory=str(settings.templates_dir))
```

**New domain exceptions:**

- `NotFoundError` — post/user not found (replaces inline `HTTPException` in services)
- `ConflictError` — duplicate username/email on user create

Handlers in `app/main.py` convert these to JSON (API) or HTML error pages (web).

---

## Step 4 — Database engine and session (`config/database.py`)

```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config.config import settings


class Base(DeclarativeBase):
    pass


connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session]:
    with SessionLocal() as db:
        yield db
```

| Piece | Role |
|-------|------|
| `Base` | Declarative base — all ORM models inherit from it |
| `engine` | Connection pool to the database |
| `SessionLocal` | Factory for database sessions |
| `get_db()` | Yields one session per request, closes after response |
| `check_same_thread: False` | Required for SQLite with FastAPI's threaded server |

---

## Step 5 — SQLAlchemy ORM models

### `app/models/user.py`

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=...)
    date_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=..., onupdate=...)

    posts: Mapped[list[Post]] = relationship(back_populates="author")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"
```

### `app/models/post.py`

```python
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=...)
    date_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=..., onupdate=...)

    author: Mapped[User] = relationship(back_populates="posts")
```

### Relationship diagram

```
users                          posts
─────                          ─────
id (PK)          ◄────────────  user_id (FK)
username                       title
email                          content
image_file                     date_created
date_created                   date_updated
date_updated

User.posts  ──►  list[Post]
Post.author ──►  User
```

**Key change from Part 4:** `author` is no longer a plain string on posts. Posts belong to a `User` via `user_id` foreign key.

Register models in `app/models/__init__.py`:

```python
from app.models.post import Post
from app.models.user import User

__all__ = ["Post", "User"]
```

Import models in `app/main.py` so SQLAlchemy registers them:

```python
import app.models  # noqa: F401
```

---

## Step 6 — Create database tables

Run once to create tables from ORM models:

```python
# create_tables.py (one-off script)
from config.database import Base, engine
import app.models  # noqa: F401

Base.metadata.create_all(bind=engine)
```

```bash
uv run python create_tables.py
```

This creates `database/blog.db` with `users` and `posts` tables matching your models.

---

## Step 7 — ORM models vs Pydantic schemas

| | SQLAlchemy ORM (`app/models/`) | Pydantic (`app/schemas/`) |
|--|-------------------------------|----------------------------|
| **Purpose** | Database tables and relationships | API request/response validation |
| **Used by** | Repositories, services | Routers, OpenAPI docs |
| **Lifespan** | Persisted in DB | Per-request, in memory |
| **Example** | `Post` with `user_id`, `relationship` | `PostCreate` with `user_id`; `PostResponse` with nested `author` |

**Rule:** never return ORM models directly without `response_model` — Pydantic controls what leaves the API. `ConfigDict(from_attributes=True)` lets Pydantic read ORM object attributes.

Move schemas from root `schemas.py` → `app/schemas/`:

### `app/schemas/user.py`

```python
class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_file: str | None = None
    image_path: str
    date_created: datetime
    date_updated: datetime
```

### `app/schemas/post.py`

```python
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=1000)


class PostCreate(PostBase):
    user_id: int   # was `author: str` in Part 4


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_created: datetime
    date_updated: datetime
    author: UserResponse   # nested user object
```

**Breaking change:** `POST /api/posts` body is now:

```json
{
  "title": "Hello",
  "content": "World",
  "user_id": 1
}
```

Not `"author": "John Doe"`.

---

## Step 8 — Repository layer (database access)

Repositories encapsulate SQLAlchemy queries. Routes never touch `Session` directly.

### `app/repositories/user_repository.py`

```python
class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, user_id: int) -> User | None: ...
    def get_by_username_or_email(self, *, username: str, email: str) -> User | None: ...
    def exists(self, user_id: int) -> bool: ...
    def create(self, *, username: str, email: str) -> User: ...
```

### `app/repositories/post_repository.py`

```python
class PostRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _base_query(self):
        return select(Post).options(joinedload(Post.author))

    def list_all(self) -> list[Post]: ...
    def get_by_id(self, post_id: int) -> Post | None: ...
    def list_by_user_id(self, user_id: int) -> list[Post]: ...
    def create(self, *, title: str, content: str, user_id: int) -> Post: ...
```

**`joinedload(Post.author)`** — eager-loads the related `User` in one query (avoids N+1 when serializing `PostResponse.author`).

Repository `create()` pattern:

```python
def create(self, *, title: str, content: str, user_id: int) -> Post:
    post = Post(title=title, content=content, user_id=user_id)
    self._db.add(post)
    self._db.commit()
    self._db.refresh(post)
    # re-fetch with joinedload so author is available
    return self._db.scalar(self._base_query().where(Post.id == post.id))
```

---

## Step 9 — Service layer (business logic)

Services sit between routers and repositories. They enforce rules and raise domain exceptions.

### `app/services/user_service.py`

```python
class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def get_user(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user

    def create_user(self, data: UserCreate) -> User:
        existing = self._repository.get_by_username_or_email(
            username=data.username, email=data.email
        )
        if existing:
            raise ConflictError("Username or email already exists")
        return self._repository.create(username=data.username, email=data.email)
```

### `app/services/post_service.py`

```python
class PostService:
    def __init__(self, repository: PostRepository, user_repository: UserRepository) -> None:
        self._repository = repository
        self._user_repository = user_repository

    def list_posts(self) -> list[Post]: ...
    def get_post(self, post_id: int) -> Post: ...       # raises NotFoundError
    def list_posts_for_user(self, user_id: int) -> list[Post]: ...
    def create_post(self, data: PostCreate) -> Post:   # validates user exists first
```

---

## Step 10 — Dependency injection (`app/providers/`)

FastAPI's `Depends()` wires the chain automatically per request.

### `app/providers/database.py`

```python
from config.database import get_db

__all__ = ["get_db"]
```

### `app/providers/services.py`

```python
DbSession = Annotated[Session, Depends(get_db)]


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


def get_post_repository(db: DbSession) -> PostRepository:
    return PostRepository(db)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)


def get_post_service(
    post_repository: Annotated[PostRepository, Depends(get_post_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> PostService:
    return PostService(post_repository, user_repository)
```

**Dependency chain:**

```
get_db
  └── get_user_repository / get_post_repository
        └── get_user_service / get_post_service
              └── route handler
```

Each request gets a fresh `Session`. One session shared across repos in the same request.

---

## Step 11 — App factory pattern (`app/main.py`)

Replace monolithic `main.py` with `create_app()`:

```python
def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.mount(settings.static_url_prefix, StaticFiles(directory=str(settings.static_dir)), name="static")
    app.mount(settings.storage_url_prefix, StaticFiles(directory=str(settings.storage_dir)), name="media")

    app.include_router(web.router)
    app.include_router(users.router)
    app.include_router(posts.router)

    # exception handlers for NotFoundError, ConflictError, HTTPException, RequestValidationError
    ...

    return app
```

Root `main.py` becomes thin:

```python
from app.main import create_app

app = create_app()
```

---

## Step 12 — Router reorganization

Split routes into modules:

```
routers/
├── web.py              # HTML pages
└── api/
    ├── posts.py        # /api/posts
    └── users.py        # /api/users
```

### API — `routers/api/posts.py`

```python
router = APIRouter(prefix="/api/posts", tags=["posts"])

@router.get("", response_model=list[PostResponse], name="api.posts.index")
def index(post_service: Annotated[PostService, Depends(get_post_service)]):
    return post_service.list_posts()

@router.get("/{post_id}", response_model=PostResponse, name="api.posts.show")
def show(post_id: int, post_service: Annotated[PostService, Depends(get_post_service)]):
    return post_service.get_post(post_id)

@router.post("", response_model=PostResponse, status_code=201, name="api.posts.store")
def store(post: PostCreate, post_service: Annotated[PostService, Depends(get_post_service)]):
    return post_service.create_post(post)
```

### API — `routers/api/users.py` (new)

```python
router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201, name="api.users.store")
def store(user: UserCreate, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse, name="api.users.show")
def show(user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.get_user(user_id)

@router.get("/{user_id}/posts", response_model=list[PostResponse], name="api.users.posts")
def posts(user_id: int, post_service: Annotated[PostService, Depends(get_post_service)]):
    return post_service.list_posts_for_user(user_id)
```

### Web — `routers/web.py`

HTML routes now use services instead of the in-memory list:

```python
@router.get("/posts", name="posts.index")
def index(request: Request, post_service: Annotated[PostService, Depends(get_post_service)]):
    return templates.TemplateResponse(
        request=request,
        name="posts/index.html",
        context={"posts": post_service.list_posts()},
    )

@router.get("/users/{user_id}/posts", name="users.posts.index")
def user_posts(request, user_id, post_service, user_service):
    author = user_service.get_user(user_id)
    posts = post_service.list_posts_for_user(user_id)
    return templates.TemplateResponse(..., context={"posts": posts, "author": author})
```

---

## Step 13 — Updated exception handlers

`app/main.py` handles domain exceptions separately from HTTP/validation errors:

| Exception | API (`/api/...`) | Web |
|-----------|------------------|-----|
| `NotFoundError` | 404 JSON | `errors/error.html` |
| `ConflictError` | 422 JSON | `errors/error.html` |
| `HTTPException` | JSON | `errors/error.html` |
| `RequestValidationError` | 422 JSON | `errors/error.html` |

Path check helper:

```python
def _is_api_request(request: Request) -> bool:
    return request.url.path.startswith("/api/")
```

---

## Step 14 — Template updates for author relationship

Templates now use `post.author` as a **User object**, not a string:

```html
<!-- home.html -->
<img src="{{ post.author.image_path }}" alt="{{ post.author.username }}" />
<a href="{{ url_for('users.posts.index', user_id=post.author.id) }}">
  {{ post.author.username }}
</a>
<time>{{ post.date_created.strftime("%A %B %d, %Y") }}</time>
```

Dates are `datetime` objects from the DB — use `.strftime()` in templates.

---

## Step 15 — Seed and test the API

**1. Create a user:**

```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","email":"john@example.com"}'
```

**2. Create a post (use `user_id` from step 1):**

```bash
curl -X POST http://127.0.0.1:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"My First DB Post","content":"Persisted in SQLite","user_id":1}'
```

**3. List posts:**

```bash
curl http://127.0.0.1:8000/api/posts
```

**4. Get user's posts:**

```bash
curl http://127.0.0.1:8000/api/users/1/posts
```

**5. Browse HTML:**

- http://127.0.0.1:8000/posts
- http://127.0.0.1:8000/posts/1
- http://127.0.0.1:8000/users/1/posts

Restart the server — data persists in `database/blog.db`.

---

## Project structure (Part 5)

```
blog/
├── main.py                          # thin entry: app = create_app()
├── .env                             # environment config (gitignored)
├── database/
│   └── blog.db                      # SQLite database file
├── config/
│   ├── config.py                    # Settings, exceptions, templates
│   └── database.py                  # engine, SessionLocal, get_db, Base
├── app/
│   ├── main.py                      # create_app(), mounts, exception handlers
│   ├── models/
│   │   ├── user.py                  # User ORM model
│   │   └── post.py                  # Post ORM model
│   ├── schemas/
│   │   ├── user.py                  # UserCreate, UserResponse
│   │   └── post.py                  # PostCreate, PostResponse
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── post_repository.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── post_service.py
│   └── providers/
│       ├── database.py              # re-exports get_db
│       └── services.py              # DI: repos → services
├── routers/
│   ├── web.py                       # HTML routes
│   └── api/
│       ├── posts.py
│       └── users.py
├── templates/
├── static/
├── storage/                         # user uploads (profile pics later)
├── pyproject.toml
└── README.md
```

---

## Endpoints summary (after Part 5)

| Method | Path | Body | Response | Status | Route name |
|--------|------|------|----------|--------|------------|
| GET | `/` | — | HTML list | 200 | `home.index` |
| GET | `/posts` | — | HTML list | 200 | `posts.index` |
| GET | `/posts/{post_id}` | — | HTML post | 200 | `posts.show` |
| GET | `/users/{user_id}/posts` | — | HTML user posts | 200 | `users.posts.index` |
| GET | `/api/posts` | — | `list[PostResponse]` | 200 | `api.posts.index` |
| GET | `/api/posts/{post_id}` | — | `PostResponse` | 200 | `api.posts.show` |
| POST | `/api/posts` | `PostCreate` | `PostResponse` | **201** | `api.posts.store` |
| POST | `/api/users/` | `UserCreate` | `UserResponse` | **201** | `api.users.store` |
| GET | `/api/users/{user_id}` | — | `UserResponse` | 200 | `api.users.show` |
| GET | `/api/users/{user_id}/posts` | — | `list[PostResponse]` | 200 | `api.users.posts` |

---

## What changed from Part 4

| Part 4 | Part 5 |
|--------|--------|
| `posts: list[dict]` in memory | SQLite via SQLAlchemy |
| `schemas.py` at root | `app/schemas/` package |
| `author: str` on posts | `user_id` FK + `User` relationship |
| Routes call list/dict directly | Routes → Service → Repository → DB |
| `HTTPException` in route handlers | `NotFoundError` / `ConflictError` in services |
| Monolithic `main.py` | `create_app()` + routers |
| Manual id/timestamp assignment | DB defaults + `onupdate` |
| No users | Full user CRUD foundation |

---

## What we learned (Part 5)

- Connect FastAPI to **SQLite** with SQLAlchemy 2.0 (`create_engine`, `sessionmaker`)
- Define **ORM models** with `Mapped`, `mapped_column`, `relationship`, `ForeignKey`
- Separate **ORM models** (persistence) from **Pydantic schemas** (API contract)
- Use **`get_db()`** generator for per-request database sessions
- Organize DB access in **repositories** and business rules in **services**
- Wire layers with **`Depends()`** dependency injection
- Eager-load relationships with **`joinedload()`**
- Load config from **`.env`** with `pydantic-settings`
- Use an **app factory** (`create_app()`) for testability and clean structure
- Split routes into **web** and **api** modules
- Raise **domain exceptions** in services; handle them centrally in the app

---

---

# Part 6 — Complete CRUD: PUT, PATCH, and DELETE

**Goals:** finish Create / Read / Update / Delete for posts and users. Add full updates (`PUT`), partial updates (`PATCH`), deletes (`DELETE`), and cascade deletion so removing a user also removes their posts.

Video: [FastAPI Full Course — Part 6](https://youtu.be/VyoGAoxQhxM?si=9gPDm9_53fXVvLQg)

---

## PUT vs PATCH

| | PUT | PATCH |
|--|-----|-------|
| **Intent** | Full replace of updatable fields | Change only fields you send |
| **Missing fields** | Treated as required / must be provided for a full update | Omitted fields stay unchanged |
| **Pydantic trick** | Assign every field from the body | `model_dump(exclude_unset=True)` then `setattr` only those keys |
| **HTTP** | `PUT /resource/{id}` | `PATCH /resource/{id}` (or a dedicated partial path) |

Both return the updated resource as `PostResponse` / `UserResponse`.

---

## Step 1 — Update schemas (`PostUpdate`, `UserUpdate`)

All update fields are **optional** (`None` default) so PATCH can send a subset. Same schema can serve PUT (client sends all fields) and PATCH (client sends some).

### `app/schemas/post.py`

```python
class PostUpdate(PostBase):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1, max_length=1000)
    user_id: int | None = Field(default=None)
```

### `app/schemas/user.py`

```python
class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None)
```

`Field(min_length=...)` still runs when a value **is** present — empty string rejected even on PATCH.

---

## Step 2 — Cascade delete on User → Posts

When a user is deleted, their posts must go too. Configure the ORM relationship:

```python
# app/models/user.py
posts: Mapped[list["Post"]] = relationship(
    back_populates="author",
    cascade="all, delete-orphan",
)
```

| Option | Meaning |
|--------|---------|
| `all` | Persist / merge / delete operations cascade to related posts |
| `delete-orphan` | Posts removed from `user.posts` (or parent deleted) are deleted from DB |

`Post.author` stays a normal `relationship(back_populates="posts")` — cascade lives on the **parent** (`User`) side.

Flow: `DELETE /api/users/{id}` → `session.delete(user)` → SQLAlchemy deletes related `posts` rows → commit.

---

## Step 3 — Repository update and delete methods

### Posts — `app/repositories/post_repository.py`

**Full update (PUT):**

```python
def update(self, post: Post, data: PostUpdate) -> Post:
    post.title = data.title
    post.content = data.content
    self._db.commit()
    self._db.refresh(post)
    return post
```

**Partial update (PATCH):**

```python
def update_partial(self, post: Post, data: PostUpdate) -> Post:
    data = data.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(post, field, value)
    self._db.commit()
    self._db.refresh(post)
    return post
```

`exclude_unset=True` — only keys the client **actually sent** appear in the dict. Fields left out of JSON are not overwritten with `None`.

**Delete:**

```python
def delete(self, post: Post):
    self._db.delete(post)
    self._db.commit()
    return post
```

### Users — `app/repositories/user_repository.py`

Same pattern: `update()` assigns all fields, `update_partial()` uses `model_dump(exclude_unset=True)`, `delete()` removes the user (cascade removes posts).

---

## Step 4 — Service layer rules

### Posts — `app/services/post_service.py`

```python
def update_post(self, post_id: int, data: PostUpdate) -> Post:
    post = self._repository.get_by_id(post_id)
    if post is None:
        raise NotFoundError("Post", post_id)
    if post.user_id != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this post",
        )
    return self._repository.update(post, data)

def update_post_partial(self, post_id: int, data: PostUpdate) -> Post:
    post = self._repository.get_by_id(post_id)
    if post is None:
        raise NotFoundError("Post", post_id)
    return self._repository.update_partial(post, data)

def delete_post(self, post_id: int) -> None:
    post = self._repository.get_by_id(post_id)
    if post is None:
        raise NotFoundError("Post", post_id)
    return self._repository.delete(post)
```

PUT checks ownership (`user_id` in body must match post owner) → **403** if mismatch. Missing post → **404**.

### Users — `app/services/user_service.py`

```python
def update_user(self, user_id: int, data: UserUpdate) -> User: ...
def update_user_partial(self, user_id: int, data: UserUpdate) -> User: ...
def delete_user(self, user_id: int) -> None: ...
```

Helpers: `findOrRaise()` → 404; username/email availability checks before update.

---

## Step 5 — API routes for posts

`routers/api/posts.py`:

```python
@router.put("/{post_id}", response_model=PostResponse, name="api.posts.update")
def update(post_id: int, post: PostUpdate, post_service: Annotated[...]):
    return post_service.update_post(post_id, post)

@router.patch(
    "/partial/{post_id}",
    response_model=PostResponse,
    name="api.posts.update.partial",
)
def update_partial(post_id: int, post: PostUpdate, post_service: Annotated[...]):
    return post_service.update_post_partial(post_id, post)

@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="api.posts.delete",
)
def delete(post_id: int, post_service: Annotated[...]):
    return post_service.delete_post(post_id)
```

**Note:** post PATCH uses path `/api/posts/partial/{post_id}` so it does not collide with `GET /{post_id}` routing order. User PATCH uses `/{user_id}` with a different HTTP method (safe).

---

## Step 6 — API routes for users

`routers/api/users.py`:

```python
@router.put("/{user_id}", response_model=UserResponse, name="api.users.update")
def update(...):
    return user_service.update_user(user_id, user)

@router.patch("/{user_id}", response_model=UserResponse, name="api.users.update.partial")
def update_partial(...):
    return user_service.update_user_partial(user_id, user)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="api.users.delete",
)
def delete(...):
    return user_service.delete_user(user_id)
```

**204 No Content** — delete succeeds with empty body. No `response_model` needed.

---

## Step 7 — Try the endpoints

Assume user `1` owns post `1`.

**PUT post (full update):**

```bash
curl -X PUT http://127.0.0.1:8000/api/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","content":"Full new body","user_id":1}'
```

Wrong `user_id` → 403.

**PATCH post (partial):**

```bash
curl -X PATCH http://127.0.0.1:8000/api/posts/partial/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Only title changes"}'
```

Content / author unchanged.

**DELETE post:**

```bash
curl -X DELETE http://127.0.0.1:8000/api/posts/1
# → 204
```

**PUT / PATCH user:**

```bash
curl -X PUT http://127.0.0.1:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username":"newname","email":"new@example.com","image_file":null}'

curl -X PATCH http://127.0.0.1:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username":"patched"}'
```

**DELETE user (cascade):**

```bash
curl -X DELETE http://127.0.0.1:8000/api/users/1
# → 204; all posts for user 1 gone from DB
```

Verify:

```bash
curl http://127.0.0.1:8000/api/users/1/posts
# → 404 User not found
```

---

## Request / response cheat sheet

```
PUT    /api/posts/{id}           body: PostUpdate (full)     → 200 PostResponse
PATCH  /api/posts/partial/{id}   body: PostUpdate (partial)  → 200 PostResponse
DELETE /api/posts/{id}           —                           → 204

PUT    /api/users/{id}           body: UserUpdate (full)     → 200 UserResponse
PATCH  /api/users/{id}           body: UserUpdate (partial)  → 200 UserResponse
DELETE /api/users/{id}           —                           → 204 (+ cascade posts)
```

---

## Error cases

| Situation | Status |
|-----------|--------|
| Post / user id not found | 404 |
| PUT post with wrong `user_id` | 403 |
| Invalid field lengths / email | 422 |
| Duplicate username/email on user update | conflict handling via service checks |

---

## Endpoints summary (after Part 6)

| Method | Path | Body | Response | Status | Route name |
|--------|------|------|----------|--------|------------|
| GET | `/api/posts/` | — | `list[PostResponse]` | 200 | `api.posts.index` |
| GET | `/api/posts/{post_id}` | — | `PostResponse` | 200 | `api.posts.show` |
| POST | `/api/posts/` | `PostCreate` | `PostResponse` | 201 | `api.posts.store` |
| PUT | `/api/posts/{post_id}` | `PostUpdate` | `PostResponse` | 200 | `api.posts.update` |
| PATCH | `/api/posts/partial/{post_id}` | `PostUpdate` | `PostResponse` | 200 | `api.posts.update.partial` |
| DELETE | `/api/posts/{post_id}` | — | — | **204** | `api.posts.delete` |
| POST | `/api/users/` | `UserCreate` | `UserResponse` | 201 | `api.users.store` |
| GET | `/api/users/{user_id}` | — | `UserResponse` | 200 | `api.users.show` |
| GET | `/api/users/{user_id}/posts` | — | `list[PostResponse]` | 200 | `api.users.posts` |
| PUT | `/api/users/{user_id}` | `UserUpdate` | `UserResponse` | 200 | `api.users.update` |
| PATCH | `/api/users/{user_id}` | `UserUpdate` | `UserResponse` | 200 | `api.users.update.partial` |
| DELETE | `/api/users/{user_id}` | — | — | **204** | `api.users.delete` |

(+ web HTML routes from earlier parts unchanged)

---

## What we learned (Part 6)

- **PUT** = full update; **PATCH** = partial update
- Optional fields on `PostUpdate` / `UserUpdate` for flexible bodies
- **`model_dump(exclude_unset=True)`** so unset fields are not wiped
- **`setattr` loop** for dynamic partial updates in repositories
- **DELETE** returns **204 No Content**
- **`cascade="all, delete-orphan"`** on `User.posts` removes posts when user deleted
- Ownership check on post PUT → **403 Forbidden**
- Full CRUD for posts and users with validation + error handling

---

---

# Part 7 — Sync vs Async, and Converting the App to Async SQLAlchemy

**Goals:** understand synchronous vs asynchronous code in FastAPI, know when async helps (and when it does not), then convert the whole stack — database config, repositories, services, routes, eager loading, lifespan, and exception handlers — to async with SQLAlchemy + aiosqlite.

Video: [FastAPI Full Course — Part 7](https://youtu.be/2JPDt-Jp6fM?si=4OlTPXFiG1TvSDqY)

---

## Concepts: Sync vs Async

### What "synchronous" means

**Sync** = one thing at a time on that worker. Call blocks until it finishes.

```python
def get_posts():
    posts = db.query(Post).all()   # thread waits here for DB
    return posts                   # then continues
```

While the database replies, that thread sits idle. Under load, FastAPI (via Starlette) can run sync routes in a **threadpool**, but each blocked thread is still occupied until I/O completes.

### What "asynchronous" means

**Async** = cooperative multitasking on one event loop. When code `await`s I/O, the loop can run other tasks.

```python
async def get_posts():
    posts = await db.scalars(select(Post))  # yield control while waiting
    return list(posts.all())
```

`async def` marks a **coroutine**. `await` pauses it until the awaited I/O finishes — without blocking the whole process. Other requests can progress on the same worker.

```
Sync (one worker, blocking I/O):

  Request A ████████████████  (waiting on DB)  ████ reply
  Request B                   (queued / other thread)

Async (event loop):

  Request A ██ await DB ┄┄┄┄┄ ┄┄ ██ reply
  Request B    ██ await DB ┄┄ ██ reply
               ↑ loop switches while A waits
```

### Sync vs async at a glance

| | Synchronous | Asynchronous |
|--|-------------|--------------|
| Function | `def` | `async def` |
| Call I/O | Blocking call | `await` non-blocking I/O |
| While waiting | Thread stuck | Event loop runs other work |
| DB driver | `sqlite3`, `psycopg2`, sync SQLAlchemy | `aiosqlite`, `asyncpg`, async SQLAlchemy |
| Mental model | Simple, linear | Coroutines + `await` discipline |
| FastAPI default | Fully supported | Preferred when I/O-bound |

### When async **helps**

Use async when the route spends most time **waiting** on I/O:

- Database queries (network or disk wait)
- HTTP calls to other APIs
- Redis / message queues
- File uploads over the network
- Many concurrent connections, mostly idle waiting

Benefit: one process handles many concurrent waiters without one thread per request.

### When async **does not help** (or hurts)

Stay sync (or offload) when work is **CPU-bound** or libraries are sync-only:

| Situation | Prefer |
|-----------|--------|
| Heavy CPU (image resize, PDF, crypto, ML inference) | Sync route, or `run_in_executor` / background worker |
| Sync-only library with no async port | Sync `def` route (FastAPI runs it in threadpool) |
| Tiny app, low traffic, simple code | Sync is fine — less complexity |
| Accidental sync call inside `async def` | **Bad** — blocks the event loop for everyone |

**Critical rule:** never call blocking sync I/O directly inside `async def` without wrapping it. That freezes the loop.

```python
# BAD — blocks event loop
async def bad():
    time.sleep(5)           # sync sleep
    open("big.bin").read()  # sync disk

# GOOD — async I/O or thread offload
async def good():
    await asyncio.sleep(5)
    await async_db.execute(...)
```

### FastAPI + sync/async mixing

FastAPI supports both:

| Route style | How FastAPI runs it |
|-------------|---------------------|
| `async def` | On the event loop — must not block |
| `def` | In a threadpool — OK to block on sync DB/libs |

You can mix routes. For this blog we go **fully async** end-to-end so DB I/O never blocks the loop.

### Async SQLAlchemy mental model

| Sync (Part 5–6) | Async (Part 7) |
|-----------------|----------------|
| `create_engine` | `create_async_engine` |
| `sessionmaker` + `Session` | `async_sessionmaker` + `AsyncSession` |
| `sqlite:///...` | `sqlite+aiosqlite:///...` |
| `db.commit()` | `await db.commit()` |
| `db.scalars(...)` | `await db.scalars(...)` |
| `joinedload(...)` | Prefer `selectinload(...)` for async |
| Sync `get_db` generator | `async def get_db` + `AsyncGenerator` |

---

## Step 1 — Install async dependencies

```bash
uv add aiosqlite greenlet
```

| Package | Why |
|---------|-----|
| `aiosqlite` | Async SQLite driver (replaces sync `sqlite3` path) |
| `greenlet` | Required by SQLAlchemy async ORM internals |

`pyproject.toml`:

```toml
dependencies = [
    "aiosqlite>=0.22.1",
    "fastapi[standard]>=0.139.0",
    "greenlet>=3.5.3",
    "jinja2>=3.1.6",
    "pydantic-settings>=2.0.0",
    "sqlalchemy>=2.0.51",
    ...
]
```

---

## Step 2 — Switch the database URL

`.env`:

```env
# Before (sync)
# DATABASE_URL=sqlite:///./database/blog.db

# After (async)
DATABASE_URL=sqlite+aiosqlite:///./database/blog.db
```

Dialect `sqlite+aiosqlite` tells SQLAlchemy to use the async aiosqlite driver.

For Postgres later: `postgresql+asyncpg://user:pass@host/db`.

---

## Step 3 — Async engine and session (`config/database.py`)

Replace sync engine/session with async versions:

```python
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.config import settings

connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_async_engine(
    url=settings.database_url,
    connect_args=connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

**What changed:**

| Piece | Role |
|-------|------|
| `create_async_engine` | Async connection pool |
| `async_sessionmaker` | Factory for `AsyncSession` |
| `expire_on_commit=False` | Objects stay usable after commit (avoids lazy-load surprises in async) |
| `async def get_db` | Yields session; `async with` closes it after the request |

Update `app/providers/services.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession

DbSession = Annotated[AsyncSession, Depends(get_db)]
```

---

## Step 4 — Eager loading: `joinedload` → `selectinload`

In async SQLAlchemy, **lazy loading is dangerous** — accessing `post.author` after the query can trigger implicit I/O that is not awaited → errors or blocked behavior.

Part 5–6 used `joinedload(Post.author)` (one SQL JOIN). For async, prefer **`selectinload`**:

```python
from sqlalchemy.orm import selectinload

def _base_query(self):
    return select(Post).options(selectinload(Post.author))
```

| Strategy | How it loads | Async fit |
|----------|--------------|-----------|
| `joinedload` | JOIN in same statement | Works, but can duplicate rows |
| `selectinload` | Second `WHERE id IN (...)` query | Clear, async-friendly |
| Lazy (`post.author` later) | Extra query on attribute access | **Avoid in async** |

After create, refresh related data explicitly if needed:

```python
await self._db.refresh(post, attribute_names=["author"])
```

---

## Step 5 — Convert repositories to `async` / `await`

Every DB call becomes async.

### Pattern

```python
# Before
def list_all(self) -> list[Post]:
    return list(self._db.scalars(...).all())

# After
async def list_all(self) -> list[Post]:
    result = await self._db.scalars(...)
    return list(result.all())
```

### Commits, deletes, refresh

```python
await self._db.commit()
await self._db.refresh(post)
await self._db.delete(post)   # AsyncSession.delete is awaitable
```

### `PostRepository` (sketch)

```python
class PostRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_all(self) -> list[Post]:
        result = await self._db.scalars(
            self._base_query().order_by(Post.date_created.desc())
        )
        return list(result.all())

    async def get_by_id(self, post_id: int) -> Post | None:
        return await self._db.scalar(self._base_query().where(Post.id == post_id))

    async def create(self, *, title: str, content: str, user_id: int) -> Post:
        post = Post(title=title, content=content, user_id=user_id)
        self._db.add(post)
        await self._db.commit()
        await self._db.refresh(post, attribute_names=["author"])
        loaded = await self._db.scalar(self._base_query().where(Post.id == post.id))
        ...
        return loaded

    async def update(...): ...
    async def update_partial(...): ...
    async def delete(self, post: Post) -> Post:
        await self._db.delete(post)
        await self._db.commit()
        return post
```

Same conversion for `UserRepository` — all methods `async`, all I/O `await`ed.

---

## Step 6 — Convert services

Services await repositories:

```python
async def get_post(self, post_id: int) -> Post:
    post = await self._repository.get_by_id(post_id)
    if post is None:
        raise NotFoundError("Post", post_id)
    return post

async def list_posts_for_user(self, user_id: int) -> list[Post]:
    if not await self._user_repository.exists(user_id):
        raise NotFoundError("User", user_id)
    return await self._repository.list_by_user_id(user_id)
```

Rule: if a method calls something that awaits, **it must be `async`** and callers must `await` it. Async spreads up the stack.

---

## Step 7 — Convert all routes to `async def`

### API example — `routers/api/posts.py`

```python
@router.get("/", response_model=list[PostResponse], name="api.posts.index")
async def index(
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return await post_service.list_posts()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, name="api.posts.delete")
async def delete(
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    await post_service.delete_post(post_id)
```

### Web example — `routers/web.py`

```python
@router.get("/", name="home.index")
async def home(
    request: Request,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"posts": await post_service.list_posts()},
    )
```

Do the same for every route in `routers/api/users.py` and `routers/web.py`.

---

## Step 8 — Async lifespan (create tables on startup)

Sync `Base.metadata.create_all(bind=engine)` does not work on an async engine. Use lifespan + `run_sync`:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: close pool
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    ...
```

| Hook | Action |
|------|--------|
| Before `yield` | App starting — create schema |
| After `yield` | App stopping — `engine.dispose()` |
| `run_sync(...)` | Run sync metadata API on async connection |

---

## Step 9 — Exception handlers (async where needed)

Handlers that call FastAPI's built-in **async** helpers must themselves be `async`:

```python
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
) -> Response | JSONResponse:
    if _is_api_request(request):
        return await http_exception_handler(request=request, exc=exception)
    message = exception.detail or "An unexpected error occurred..."
    return _error_page(request, exception.status_code, message)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    if _is_api_request(request):
        return await request_validation_exception_handler(
            request=request, exc=exception
        )
    message = ", ".join(error["msg"] for error in exception.errors())
    return _error_page(request, status.HTTP_422_UNPROCESSABLE_ENTITY, message)
```

Domain handlers (`NotFoundError`, `ConflictError`) can stay sync `def` if they only build responses — no `await` needed.

---

## Conversion checklist (sync → async)

Work bottom-up so nothing calls an async function without `await`:

1. [ ] Add `aiosqlite` + `greenlet`
2. [ ] Change `DATABASE_URL` to `sqlite+aiosqlite://...`
3. [ ] Rewrite `config/database.py` (async engine, session, `get_db`)
4. [ ] Point `DbSession` at `AsyncSession`
5. [ ] Repos: `AsyncSession`, `async def`, `await` all I/O; `selectinload`
6. [ ] Services: `async def` + `await` repos
7. [ ] Routes: `async def` + `await` services
8. [ ] Lifespan: `create_all` via `run_sync`, `engine.dispose()`
9. [ ] Exception handlers that await FastAPI helpers → `async def`
10. [ ] Smoke-test CRUD + HTML pages under concurrent load

---

## Sync → async diff cheat sheet

```python
# Engine
create_engine(...)              →  create_async_engine(...)
sessionmaker(...)               →  async_sessionmaker(..., class_=AsyncSession)
sqlite:///                      →  sqlite+aiosqlite:///

# Session dependency
def get_db():                   →  async def get_db():
    with SessionLocal() as db:  →      async with AsyncSessionLocal() as session:
        yield db                →          yield session

# Queries
db.scalars(q)                   →  await db.scalars(q)
db.commit()                     →  await db.commit()
db.refresh(obj)                 →  await db.refresh(obj)
db.delete(obj)                  →  await db.delete(obj)

# Eager load
joinedload(Post.author)         →  selectinload(Post.author)

# Routes / services
def index(...):                 →  async def index(...):
    return service.list()       →      return await service.list()
```

---

## Decision guide (keep this)

```
Is the work mostly waiting on I/O (DB, HTTP, disk network)?
  YES → async def + async libraries (this part)
  NO  → is it CPU-heavy?
          YES → sync def, or process/thread pool / worker queue
          NO  → either works; pick clarity

Do you have a sync-only library?
  YES → sync route, OR await asyncio.to_thread(sync_fn)
  NO  → prefer async stack if already async elsewhere

Are you inside async def?
  NEVER call blocking sync I/O without to_thread / executor
```

---

## What we learned (Part 7)

- **Sync** blocks a thread until I/O finishes; **async** yields the event loop with `await`
- Async helps **I/O-bound** concurrency; not magic for **CPU-bound** work
- Mixing: FastAPI runs sync `def` in a threadpool; `async def` must stay non-blocking
- Wire async SQLAlchemy: `create_async_engine`, `AsyncSession`, `sqlite+aiosqlite`
- Prefer **`selectinload`** for relationships under async (avoid lazy loads)
- Convert bottom-up: DB → repos → services → routes
- Use **lifespan** + `run_sync(create_all)` and `engine.dispose()`
- Make exception handlers `async` when they `await` framework helpers

---

---

# Part 8 — Organize Routes with APIRouter

**Goals:** stop putting every endpoint on the FastAPI app object in one giant file. Split routes into modules with `APIRouter`, then mount them with `include_router`.

Video: [FastAPI Full Course — Part 8](https://youtu.be/NkgIHa6KtHg?si=PiDtpeWly1twPCP7)

> **Already done in this project.** Starting in Part 5 you moved routes into `routers/`. Part 8 of the video series covers the same idea formally. This section documents *why* and *how* — matching your current layout.

---

## The problem

Early parts used a single `main.py`:

```python
app = FastAPI()

@app.get("/api/posts")
def get_posts(): ...

@app.post("/api/posts")
def create_post(): ...

@app.get("/api/users/{user_id}")
def get_user(): ...
# ... grows forever
```

As CRUD, users, HTML pages, and exception handlers pile up, `main.py` becomes hard to navigate, review, and test.

---

## The fix: `APIRouter`

`APIRouter` = mini FastAPI app for a group of related routes. Same decorators (`@router.get`, `@router.post`, …). You attach the router to the real app later.

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/posts", tags=["posts"])

@router.get("/")
async def index(): ...
```

Then in `create_app()`:

```python
from routers.api import posts

app.include_router(posts.router)
```

Paths combine: `prefix="/api/posts"` + `@router.get("/")` → `/api/posts/`.

---

## Why routers help

| Benefit | Detail |
|---------|--------|
| **Separation** | Posts, users, web pages live in separate files |
| **Prefixes** | Set `/api/posts` once — no copy-paste on every path |
| **OpenAPI tags** | `tags=["posts"]` groups endpoints in `/docs` |
| **Schema control** | Web router can use `include_in_schema=False` |
| **Thin app factory** | `app/main.py` only mounts routers + handlers |
| **Team scale** | Different people edit different modules |

---

## Your project layout (already in place)

```
routers/
├── web.py              # HTML pages (not in OpenAPI)
└── api/
    ├── posts.py        # /api/posts  CRUD
    └── users.py        # /api/users  CRUD
```

```
app/main.py             # create_app() → include_router(...)
main.py                 # app = create_app()
```

---

## Step 1 — Create a posts router

`routers/api/posts.py`:

```python
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/", response_model=list[PostResponse], name="api.posts.index")
async def index(post_service: Annotated[PostService, Depends(get_post_service)]):
    return await post_service.list_posts()


@router.get("/{post_id}", response_model=PostResponse, name="api.posts.show")
async def show(...): ...

@router.post("/", ..., name="api.posts.store")
async def store(...): ...

# put / patch / delete likewise — all on `router`, not `app`
```

**Key options on `APIRouter(...)`:**

| Option | Your value | Effect |
|--------|------------|--------|
| `prefix` | `/api/posts` | Prepended to every path |
| `tags` | `["posts"]` | Swagger UI section label |

Use `@router.get` / `@router.post` / … instead of `@app.get`.

---

## Step 2 — Create a users router

`routers/api/users.py`:

```python
router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", ..., name="api.users.store")
async def store(...): ...

@router.get("/{user_id}", ..., name="api.users.show")
async def show(...): ...

@router.get("/{user_id}/posts", ..., name="api.users.posts")
async def posts(...): ...
# put / patch / delete ...
```

Same pattern — different prefix and tags.

---

## Step 3 — Create a web router (HTML)

`routers/web.py`:

```python
router = APIRouter(include_in_schema=False)

@router.get("/", name="home.index")
async def home(...): ...

@router.get("/posts", name="posts.index")
async def index(...): ...
```

`include_in_schema=False` — HTML pages stay out of `/docs` / OpenAPI. API routers stay documented.

---

## Step 4 — Mount routers in the app factory

`app/main.py` stays focused on wiring:

```python
from routers.api import posts, users
from routers import web

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.mount(...)  # static / media

    app.include_router(web.router)
    app.include_router(users.router)
    app.include_router(posts.router)

    # exception handlers stay on `app`
    ...
    return app
```

Order of `include_router` rarely matters for distinct prefixes. Keep static mounts before or beside routers as you already do.

Root `main.py`:

```python
from app.main import create_app

app = create_app()
```

---

## Step 5 — Optional: router-level dependencies / config

Useful later (auth, rate limits):

```python
router = APIRouter(
    prefix="/api/posts",
    tags=["posts"],
    # dependencies=[Depends(require_auth)],  # applies to all routes on this router
)
```

You can also nest routers:

```python
api = APIRouter(prefix="/api")
api.include_router(posts.router)   # if posts had prefix="/posts"
api.include_router(users.router)
app.include_router(api)
```

Your project puts the full prefix on each child router (`/api/posts`, `/api/users`) — also valid and clear.

---

## Before vs after

| Before (monolith) | After (routers) |
|-------------------|-----------------|
| `@app.get("/api/posts")` in `main.py` | `@router.get("/")` in `routers/api/posts.py` |
| All paths written in full | Shared `prefix` |
| One huge file | One module per resource |
| Hard to find endpoints | Open `posts.py` / `users.py` / `web.py` |
| App owns every route | App only `include_router` |

---

## How this maps to earlier parts

| Series video timing | Your repo |
|---------------------|-----------|
| Part 8 teaches routers | You introduced `routers/` in **Part 5** while adding SQLAlchemy + services |
| Video may still show sync + simple structure | Your routers are already **async** + DI (`Depends(get_post_service)`) |

No code move required if structure already matches. Part 8 = conceptual checkpoint + docs alignment.

---

## Quick mental model

```
create_app()
   ├── include_router(web.router)      → /, /posts, /posts/{id}, ...
   ├── include_router(users.router)    → /api/users/...
   └── include_router(posts.router)    → /api/posts/...

Each router file:
   router = APIRouter(prefix=..., tags=...)
   @router.get / post / put / patch / delete
```

---

## What we learned (Part 8)

- Fat `main.py` does not scale — split by resource
- **`APIRouter`** groups related endpoints like a sub-app
- **`prefix`** and **`tags`** cut duplication and clarify OpenAPI
- **`include_router`** mounts modules onto the FastAPI app
- Web routes can hide from docs with **`include_in_schema=False`**
- App factory keeps lifespan, mounts, and exception handlers; routers own HTTP endpoints

---

---

# Part 9 — Interactive Frontend with the Fetch API

**Goals:** make the read-only pages interactive. Use JavaScript + the Fetch API to **create**, **edit**, and **delete** posts straight from the browser. Show forms in modals, give feedback with toasts, and keep the user on the same page — no full reloads.

Video: [FastAPI Full Course — Part 9](https://youtu.be/vqjZOyT4QRs?si=1cDeYpf-DUCGQEoa)

> **Stack note:** the video uses **Bootstrap** modals. This project uses **Tailwind + Alpine.js** modals and a custom toast store. Same idea — a form in a modal that calls the JSON API with `fetch`. Code below matches *this* project.

---

## The concept

Until now web pages only **read** data (server renders HTML). Part 9 adds **writes** from the browser:

```
Browser form  ──fetch(POST/PUT/DELETE)──►  /api/posts...  ──►  DB
      ▲                                                          │
      └──────────  JSON response + toast  ◄──────────────────────┘
      (stay on page, update UI)
```

Two APIs already exist (Parts 4–6):

| Action | Method | Endpoint |
|--------|--------|----------|
| Create | POST | `/api/posts/` |
| Edit (full) | PUT | `/api/posts/{id}` |
| Edit (partial) | PATCH | `/api/posts/partial/{id}` |
| Delete | DELETE | `/api/posts/{id}` |

Part 9 is **frontend only** — no new backend routes. JS talks to those endpoints.

---

## Fetch API basics

`fetch()` returns a Promise. Send JSON, read JSON back:

```js
const res = await fetch("/api/posts/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title, content, user_id: 1 }),
});

if (!res.ok) {
  const err = await res.json();
  throw new Error(err.detail ?? "Request failed");
}

const post = await res.json();   // PostResponse
```

| Piece | Why |
|-------|-----|
| `method` | POST / PUT / PATCH / DELETE |
| `headers` Content-Type | Tell FastAPI the body is JSON |
| `JSON.stringify(...)` | Serialize the form data |
| `res.ok` | `false` for 4xx/5xx — handle errors |
| `res.json()` | Parse response (or `err.detail` on error) |
| DELETE → 204 | No body — do **not** call `res.json()` |

---

## Current UI building blocks (already in project)

| File | Role |
|------|------|
| `templates/posts/index.html` | "Add post" button → `post_modal` |
| `templates/posts/show.html` | Edit / Delete buttons → `post_modal` + `confirm_modal` |
| `templates/components/post_modal.html` | `post_modal()` + `confirm_modal()` macros |
| `static/js/alpine.min.js` | Alpine.js — modal open/close state |
| `static/js/toast.js` | Toast store + `window.notify(...)` |
| `templates/layouts/base.html` | Toast container + script includes |

Modals open with Alpine state (`x-data="{ open: false }"`, `@click="open = true"`). Toasts fire via `notify('message', 'success')`.

---

## Step 1 — Modal markup (recap)

`post_modal` renders a form with title + content inputs. `confirm_modal` renders a delete confirmation. Both are Jinja macros so add/edit/delete reuse one definition:

```jinja
{% from "components/post_modal.html" import post_modal, confirm_modal %}

{{ post_modal(
  state="open", heading="Add post", submit_label="Publish",
  submit_message="Post created successfully", dom_id="add-post"
) }}
```

Alpine controls visibility; the `<form>` inside is where Fetch gets wired.

---

## Step 2 — From placeholder to real Fetch

The starter form only closes + toasts:

```html
<!-- placeholder: no API call -->
<form @submit.prevent="open = false; notify('Post created successfully', 'success')">
```

Replace with a real request. Give the form an Alpine component and a submit handler:

```html
<form
  x-data="postForm({ mode: 'create', postId: null })"
  @submit.prevent="submit()"
>
  <input x-model="title" class="input" required />
  <textarea x-model="content" class="input" required></textarea>

  <button type="button" class="btn btn-outline" @click="open = false">Cancel</button>
  <button type="submit" class="btn btn-default" :disabled="loading">
    <span x-text="loading ? 'Saving...' : submitLabel"></span>
  </button>
</form>
```

---

## Step 3 — The Fetch component (`static/js/posts.js`)

Add a new JS file with the create/edit/delete logic:

```js
function postForm({ mode, postId, title = "", content = "", userId = 1 }) {
  return {
    mode,
    postId,
    title,
    content,
    userId,
    loading: false,
    submitLabel: mode === "create" ? "Publish" : "Save changes",

    async submit() {
      this.loading = true;
      try {
        const isCreate = this.mode === "create";
        const url = isCreate ? "/api/posts/" : `/api/posts/${this.postId}`;
        const method = isCreate ? "POST" : "PUT";

        const res = await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            title: this.title,
            content: this.content,
            user_id: this.userId,
          }),
        });

        if (!res.ok) {
          const err = await res.json();
          const detail = Array.isArray(err.detail)
            ? err.detail.map((e) => e.msg).join(", ")
            : err.detail;
          throw new Error(detail || "Request failed");
        }

        const post = await res.json();
        notify(
          isCreate ? "Post created successfully" : "Post updated successfully",
          "success"
        );
        // stay on page: redirect to the post, or refresh the list
        window.location = isCreate ? `/posts/${post.id}` : window.location.href;
      } catch (e) {
        notify(e.message, "error");
      } finally {
        this.loading = false;
      }
    },

    async remove() {
      this.loading = true;
      try {
        const res = await fetch(`/api/posts/${this.postId}`, { method: "DELETE" });
        if (!res.ok && res.status !== 204) {
          const err = await res.json();
          throw new Error(err.detail || "Delete failed");
        }
        notify("Post deleted successfully", "success");
        window.location = "/posts";
      } catch (e) {
        notify(e.message, "error");
      } finally {
        this.loading = false;
      }
    },
  };
}
```

Register the script in `base.html` (before Alpine so the function exists on init, or use `alpine:init`):

```html
<script src="{{ url_for('static', path='js/posts.js') }}"></script>
<script defer src="{{ url_for('static', path='js/alpine.min.js') }}"></script>
```

---

## Step 4 — Wire create (index page)

`templates/posts/index.html` — the "Add post" modal form uses `mode: 'create'`:

```html
<form x-data="postForm({ mode: 'create' })" @submit.prevent="submit()">
  ...
</form>
```

Submitting POSTs to `/api/posts/`, toasts success, and navigates to the new post.

---

## Step 5 — Wire edit (show page)

`templates/posts/show.html` — the edit modal preloads current values and uses `mode: 'edit'`:

```html
<form
  x-data="postForm({
    mode: 'edit',
    postId: {{ post.id }},
    title: {{ post.title | tojson }},
    content: {{ post.content | tojson }},
    userId: {{ post.user_id }}
  })"
  @submit.prevent="submit()"
>
  ...
</form>
```

`| tojson` safely escapes server values into JS strings. Submitting PUTs to `/api/posts/{id}`.

**PUT vs PATCH:** PUT sends all fields (needs `user_id` for the ownership check from Part 6). For "change only title", call PATCH `/api/posts/partial/{id}` with just the changed keys.

---

## Step 6 — Wire delete (confirm modal)

`confirm_modal` button calls `remove()` instead of just toasting:

```html
<button
  type="button"
  class="btn btn-destructive"
  x-data="postForm({ mode: 'edit', postId: {{ post.id }} })"
  @click="remove()"
>
  Delete
</button>
```

DELETE returns **204** — the handler checks `res.status !== 204` before reading a body, then redirects to `/posts`.

---

## Step 7 — Error handling and UX

| Concern | Handling |
|---------|----------|
| Validation error (422) | `err.detail` is a list → join `e.msg` into one toast |
| Not found (404) / forbidden (403) | Show `err.detail` string as error toast |
| Network failure | `try/catch` → error toast |
| Double submit | `loading` flag disables the button |
| Keep user on page | No `<form action>`; `@submit.prevent` + `fetch` |
| Feedback | `notify(msg, 'success' | 'error')` toast store |

---

## Request lifecycle (create post)

```mermaid
sequenceDiagram
    participant U as User
    participant M as Modal form (Alpine)
    participant JS as fetch (posts.js)
    participant API as /api/posts (FastAPI)
    participant DB as SQLite

    U->>M: Click "Add post", fill fields, Submit
    M->>JS: submit() (@submit.prevent)
    JS->>API: POST JSON {title, content, user_id}
    API->>DB: INSERT post
    DB-->>API: new row
    API-->>JS: 201 PostResponse
    JS->>U: notify success + redirect to /posts/{id}
    Note over JS,U: On error → notify(err.detail, 'error'), stay open
```

---

## Files touched (Part 9)

```
static/js/
├── posts.js        # NEW: postForm() create/edit/delete via fetch
├── toast.js        # existing: notify() feedback
└── alpine.min.js   # existing: modal state

templates/
├── posts/index.html            # Add-post modal → mode:'create'
├── posts/show.html             # Edit + Delete modals → mode:'edit'
├── components/post_modal.html  # form wired to submit()/remove()
└── layouts/base.html           # include posts.js
```

No backend changes — reuses Part 4–6 API.

---

## What we learned (Part 9)

- Turn read-only pages into interactive ones with the **Fetch API**
- Send JSON with `method`, `Content-Type`, `JSON.stringify`
- Reuse existing **POST / PUT / PATCH / DELETE** endpoints from the browser
- Show forms in **modals** and feedback with **toasts** — no page navigation
- Handle **422 / 404 / 403** responses via `res.ok` + `err.detail`
- Guard against double submit with a `loading` flag
- `DELETE` returns **204** — skip `res.json()`
- Escape server data into JS with Jinja **`| tojson`**

---

## What's next (later parts)

The full course continues with:

- User registration and login (password hashing, JWT)
- File uploads (profile pictures → `storage/`)
- Background tasks (email)
- Alembic migrations (schema versioning)

---

## Reference

- [FastAPI Full Course — Part 1 (YouTube)](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz)
- [FastAPI Full Course — Part 2 (YouTube)](https://youtu.be/G4NIB9Rx9Qs?si=ZXfoVQvaBLzCIM9K)
- [FastAPI Full Course — Part 3 (YouTube)](https://youtu.be/WRjXIA5pMtk?si=n6uJOrhtggajfJKz)
- [FastAPI Full Course — Part 4 (YouTube)](https://youtu.be/9GHxnttXxrA?si=a0H4pr6UwjQeoKkm)
- [FastAPI Full Course — Part 5 (YouTube)](https://youtu.be/NvOV3ig2tGY?si=SYpgR6_fNCHQy3Ba)
- [FastAPI Full Course — Part 6 (YouTube)](https://youtu.be/VyoGAoxQhxM?si=9gPDm9_53fXVvLQg)
- [FastAPI Full Course — Part 7 (YouTube)](https://youtu.be/2JPDt-Jp6fM?si=4OlTPXFiG1TvSDqY)
- [FastAPI Full Course — Part 8 (YouTube)](https://youtu.be/NkgIHa6KtHg?si=PiDtpeWly1twPCP7)
- [FastAPI Full Course — Part 9 (YouTube)](https://youtu.be/vqjZOyT4QRs?si=1cDeYpf-DUCGQEoa)
- [MDN — Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [Alpine.js documentation](https://alpinejs.dev/)
- [FastAPI — Bigger Applications / Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [FastAPI — SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy — Asynchronous I/O](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Jinja2 documentation](https://jinja.palletsprojects.com/)
- [Tailwind CSS documentation](https://tailwindcss.com/docs)

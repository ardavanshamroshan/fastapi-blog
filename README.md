# Blog — FastAPI Tutorial

A minimal blog API with styled HTML pages, built while following the [FastAPI Full Course](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz) on YouTube.

| Part | Video | Topics |
|------|-------|--------|
| 1 | [Part 1](https://youtu.be/7AMjmCTumuo?si=1KWXniowqB-o05Mz) | FastAPI setup, JSON API, inline HTML |
| 2 | [Part 2](https://youtu.be/G4NIB9Rx9Qs?si=ZXfoVQvaBLzCIM9K) | Jinja2 templates, static files, Tailwind CSS, single post view |
| 3 | [Part 3](https://youtu.be/WRjXIA5pMtk?si=n6uJOrhtggajfJKz) | Path parameters, API vs web routes, validation errors, custom exception handlers |

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
- [FastAPI Full Course — Part 3 (YouTube)](https://youtu.be/WRjXIA5pMtk?si=n6uJOrhtggajfJKz)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [FastAPI — Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [FastAPI — Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Jinja2 documentation](https://jinja.palletsprojects.com/)
- [Tailwind CSS documentation](https://tailwindcss.com/docs)

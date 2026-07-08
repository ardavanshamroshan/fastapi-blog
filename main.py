import datetime
from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse

app = FastAPI()
app.mount(path='/static', app=StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

posts: list[dict] = [
    {
        'id': 1,
        'author': 'John Doe',
        'title': 'My First Post',
        'content': 'This is my first post',
        'date_created': '2021-01-01',
        'date_updated': '2021-01-01',
        'tags': ['python', 'fastapi', 'blog'],
    },
    {
        'id': 2,
        'author': 'Alex Smith',
        'title': 'My Second Post',
        'content': 'This is my second post',
        'date_created': '2021-01-02 11:40:21',
        'date_updated': '2021-01-02 12:00:00',
        'tags': ['python', 'fastapi', 'blog'],
    },
]

"""
1. The routes are defined in the order they are defined in the code.
2. response_class=HTMLResponse is used to return a HTML response
3. Include_in_schema=False is used to exclude the route from the API documentation
"""

# Web Routes


@app.get(path='/', include_in_schema=False, name='home.index')
@app.get(path='/posts', include_in_schema=False, name='home.posts')
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context={
            'posts': posts
        },
    )


@app.get(path='/posts/{post_id}', name='posts.show', include_in_schema=False)
def show_post(request: Request, post_id: int):
    post = next(
        (post for post in posts if post['id'] == post_id),
        None
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

    return templates.TemplateResponse(
        request=request,
        name='post.html',
        context={
            'post': post,
            'title': post['title'],
        },
    )

# API Routes


@app.get(path='/api/posts', response_model=list[PostResponse], name='api.posts.index')
def get_posts() -> list[dict]:
    """FastAPI automatically serializes the response to JSON"""
    return posts


@app.get(path='/api/posts/{post_id}', response_model=PostResponse, name='api.posts.show')
def get_post(post_id: int) -> dict:

    post = next(
        (post for post in posts if post['id'] == post_id),
        None
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found'
        )

    return post


@app.post(
    path='/api/posts',
    name='api.posts.create',
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(post: PostCreate):
    new_id = max(post['id'] for post in posts) + 1 if posts else 1
    now = datetime.datetime.today().isoformat()
    new_post = {
        'id': new_id,
        'author': post.author,
        'title': post.title,
        'content': post.content,
        'date_created': now,
        'date_updated': now,
    }

    posts.append(new_post)
    return new_post

# Exception Handlers


@app.exception_handler(StarletteHTTPException)
def general_exception_handler(request: Request, exception: StarletteHTTPException) -> JSONResponse:
    """The code to handle the exception and return the appropriate response for both API and web requests"""

    message = (
        exception.detail if exception.detail else 'An unexpected error occurred. Please check the request and try again.'
    )

    if request.url.path.startswith('/api/'):
        return JSONResponse(
            status_code=exception.status_code,
            content={
                'detail': message
            }
        )

    return templates.TemplateResponse(
        request=request,
        name='errors/error.html',
        context={
            'status_code': exception.status_code,
            'title': exception.status_code,
            'message': message
        },
        status_code=exception.status_code
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError) -> JSONResponse:
    if request.url.path.startswith('/api/'):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'detail': exception.errors()
            }
        )

    return templates.TemplateResponse(
        request=request,
        name='errors/error.html',
        context={
            'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'title': 'Unprocessable Entity',
            'message': ', '.join([error['msg'] for error in exception.errors()])
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

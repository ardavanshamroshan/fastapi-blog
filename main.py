from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException

app = FastAPI()
app.mount(path='/static', app=StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory="templates")

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


@app.get(path='/', include_in_schema=False, name='home.index')
@app.get(path='/posts', include_in_schema=False, name='home.posts')
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={"posts": posts})


@app.get(path='/api/posts', name='posts.index')
def get_posts():
    """FastAPI automatically serializes the response to JSON"""
    return posts


@app.get(path='/api/posts/{post_id}', name='posts.show')
def get_post(request: Request, post_id: int):
    post = next(
        (post for post in posts if post['id'] == post_id),
        None
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": post},
    )

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

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
        'date_created': '2021-01-02',
        'date_updated': '2021-01-02',
        'tags': ['python', 'fastapi', 'blog'],
    },
]

"""
1. The routes are defined in the order they are defined in the code.
2. response_class=HTMLResponse is used to return a HTML response
3. Include_in_schema=False is used to exclude the route from the API documentation
"""


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
@app.get('/posts', response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"


@app.get('/api/posts')
def get_posts():
    """FastAPI automatically serializes the response to JSON"""
    return posts

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
    {
        "id": 1,
        "author": "Saif Rasheed",
        "title": "Why I'm Learning Backend Alongside AI",
        "content": "Prompt engineering taught me what AI can do — now I want to understand how the systems around it actually work.",
        "date_posted": "June 29, 2026",
    },
    {
        "id": 2,
        "author": "Saif Rasheed",
        "title": "FastAPI First Impressions",
        "content": "Auto-generated docs at /docs felt like magic — now I want to know what's happening underneath.",
        "date_posted": "June 29, 2026",
    },
]


@app.get("/", response_class=HTMLResponse, include_in_schema = False)
@app.get("/poxt", response_class=HTMLResponse , include_in_schema = False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"
    

@app.get("/api/posts")
def get_posts():
    return posts

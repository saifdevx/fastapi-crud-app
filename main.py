from fastapi import FastAPI , Request

from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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


@app.get("/", include_in_schema = False)
@app.get("/poxt" , include_in_schema = False)
def home(request : Request):
    return templates.TemplateResponse(request , "home.html" , {"posts" : posts , "title" : "Home"} )
    

@app.get("/api/posts")
def get_posts():
    return posts

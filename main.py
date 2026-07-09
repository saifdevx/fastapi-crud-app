from fastapi import FastAPI, Request, HTTPException, status , Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from schemas import PostCreate , PostResponse , UserCreate , UserResponse 

from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base , engine , get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media" , StaticFiles(directory = "media") , name = "media")

@app.exception_handler(HTTPException)
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )





@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False , name = "posts") 
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )



@app.get("/posts/{post_id}" , include_in_schema=False , name = "post")
def get_post_page(request : Request , post_id : int):
    for post in posts:
        if post.get("id") == post_id:
           title = post['title'][:50]
           return templates.TemplateResponse(
        request, "post.html", {"post": post, "title": title},
    )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")

@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)

def create_user(user: UserCreate , db : Annotated[ Session,Depends(get_db) ]):
    resut = db.execute(
        select(models.User).where(models.User.username == user.username), 
        )
    existing_user = resut.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "UserName Already Exits",
        ) 

    resut = db.execute(
        select(models.User).where(models.User.email == user.email), 
        )
    existing_email = resut.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Email Already Exits",
        ) 

    new_user  = models.User(
        username = user.username,
        email = user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
 


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts


## Create Post
@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post




@app.get("/api/posts/{post_id}" , response_model=PostResponse)
def get_post(post_id : int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")




from fastapi import FastAPI,Request,status
from pydantic import BaseModel
from typing import Optional
from .database import Base, engine
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .routers import auth, todos, admin, users
from .rate_limiter import limiter, rate_limit_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os


app=FastAPI()


app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


Base.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory="todo_app/static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


# @app.get("/")
# def test(request: Request):
#     return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Or restrict to ["http://127.0.0.1:5500"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/", include_in_schema=False)
# @limiter.exempt
# def root():
#     return RedirectResponse(url="/static/index.html")


@app.get("/")
def root():
    return {
        "message": "Todo API is running",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "todos": "/todos", 
            "users": "/users",
            "admin": "/admin"
        }
    }

@app.get("/healthy")
@limiter.exempt
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

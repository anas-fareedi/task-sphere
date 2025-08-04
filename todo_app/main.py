from fastapi import FastAPI,Request,status
from pydantic import BaseModel
from typing import Optional
from .database import Base, engine
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .routers import auth, todos, admin, users

app=FastAPI()

Base.metadata.create_all(bind=engine)

# app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

# @app.get("/")
# def test(request: Request):
#     return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


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
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


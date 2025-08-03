from fastapi import FastAPI,HTTPException,requests,status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# from models import Base
# from database import engine
# from routers import auth,users,admin,todos

app=FastAPI()


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime

todos_db = []
todo_counter = 1

@app.get("/")
async def root():
    return {"message": "Hello from your To-Do app!"}

@app.get("/todo")
async def get_todos(response_model=List[Todo]):
    return todos_db

@app.post("/todo",response_model=Todo)
async def create_todo(todo: TodoCreate):

    global todo_counter
    new_todo = Todo(
        id=todo_counter,
        title=todo.title,
        description=todo.description,
        created_at=datetime.now()
    )
    todos_db.append(new_todo)
    todo_counter += 1
    return new_todo


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            updated_data = todo_update.dict(exclude_unset=True)
            updated_todo = todo.copy(update=updated_data)
            todos_db[i] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            del todos_db[i]
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
        
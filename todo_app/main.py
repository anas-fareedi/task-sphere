from fastapi import FastAPI,HTTPException,requests,status,Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from .models import Todos , Users 

app=FastAPI()

Base.metadata.create_all(bind=engine)

# @app.get("/")
# def test(request: Request):
#     return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = "user"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    role: Optional[str] = None
    phone_number: Optional[str] = None
    
    class Config:
        orm_mode = True


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int
    complete: Optional[bool] = False
    owner_id: int

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    complete: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    complete: bool
    owner_id: int
    
    class Config:
        orm_mode = True


@app.get("/")
async def root():
    return {"message": "Hello from your To-Do app!"}


@app.get("/todo", response_model=List[Todo])
async def get_todos(db: Session = Depends(get_db)):
    return db.query(Todos).all()


@app.post("/user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    new_user = Users(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    # Verify the owner exists
    owner = db.query(Users).filter(Users.id == todo.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    new_todo = Todos(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete,
        owner_id=todo.owner_id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

from typing import Annotated,List, Optional
from pydantic import BaseModel, Field
# from slowapi import Limiter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status,Query
from starlette import status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user
from starlette.responses import RedirectResponse
from ..rate_limiter import limiter 
from typing import List

# from fastapi.templating import Jinja2Templates

# templates = Jinja2Templates(directory="TodoApp/templates")

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

# ── Pydantic Models ──
class TodoIn(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int
    
    class Config:
        orm_mode = True

        
# def redirect_to_login():
#     redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
#     redirect_response.delete_cookie(key="access_token")
#     return redirect_response


### Pages ###

# @router.get("/todo-page")
# async def render_todo_page(request: Request, db: db_dependency):
#     try:
#         user = await get_current_user(request.cookies.get('access_token'))

#         if user is None:
#             return redirect_to_login()

#         todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

#         # return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})

#     except:
#         return redirect_to_login()


# @router.get('/add-todo-page')
# async def render_todo_page(request: Request):
#     try:
#         user = await get_current_user(request.cookies.get('access_token'))

#         if user is None:
#             return redirect_to_login()

#         return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

#     except:
#         return redirect_to_login()


# @router.get("/edit-todo-page/{todo_id}")
# async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
#     try:
#         user = await get_current_user(request.cookies.get('access_token'))

#         if user is None:
#             return redirect_to_login()

#         todo = db.query(Todos).filter(Todos.id == todo_id).first()

#         return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

#     except:
#         return redirect_to_login()

### Endpoints ###

@router.get(
    "",                                   # /todos
    response_model=List[TodoOut],
    status_code=status.HTTP_200_OK
)
@limiter.limit("60/minute")
def read_all(
    request: Request,
    user: user_dependency,
    db: db_dependency,
    skip: int = Query(0,  ge=0,  description="How many todos to skip"),
    limit: int = Query(50, ge=1, le=100, description="Max todos to return")
):
    """Return the authenticated user’s todos with offset-limit pagination."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    query = db.query(Todos).filter(Todos.owner_id == user["id"])
    total = query.count()
    todos = query.offset(skip).limit(limit).all()

    # optional: expose pagination meta via headers
    request.state.pagination = {"total": total, "skip": skip, "limit": limit}

    return todos


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_multiple_todos(user: user_dependency, db: db_dependency,
                                todo_requests: List[TodoRequest]):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todos = []
    for todo_request in todo_requests:
        todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
        db.add(todo_model)
        todos.append(todo_model)

    db.commit()

    for t in todos:
        db.refresh(t)

    return {"message": f"{len(todos)} todos created successfully"}


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit() 

 
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()
    
import os
from beanie import PydanticObjectId

from dotenv import load_dotenv
import jwt

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends

from model import User, UserLogin, Todos, SendTodo, TodoUpdate, UserRegister
from database import lifespan

from pymongo.errors import DuplicateKeyError

from security import get_password_hash, verify_password

load_dotenv()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501/"],
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"], # Allows all headers
)

def current_user(token: str = Header(None)):
    if token:
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRECT"), algorithms=["HS256"])
            return payload["email"]
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid token")
    else:
        raise HTTPException(status_code=400, detail="Unauthorized")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
async def register_user(user: UserRegister):
    try:
        new_user = User(email=user.email, password=get_password_hash(user.password), username=user.username)
        await new_user.insert()
        return {
            "message": f"User registered",
            "token": jwt.encode({
                "email": new_user.email
            }, os.getenv("JWT_SECRECT"), algorithm="HS256")
        }

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/login")
async def login_user(user: UserLogin):
    usr = await User.find_one(User.email == user.email)

    if (not usr):
        raise HTTPException(status_code=400, detail="User not found")

    if (not verify_password(user.password, usr.password)):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {
        "message": f"User logged in",
        "username": usr.username,
        "token": jwt.encode({
            "email": user.email
        }, os.getenv("JWT_SECRECT"), algorithm="HS256")
    }

@app.post('/todos')
async def add_todos(todo_data: SendTodo, curr_user: str | dict = Depends(current_user)):  # Renamed to todo_data
    try:
        usr = await User.find_one(User.email == curr_user)

        if not usr:
            raise HTTPException(status_code=400, detail="Unauthorized")

        new_todo = Todos(
            task=todo_data.task,
            completed=todo_data.completed,
            user=usr
        )

        await new_todo.insert()

        user_todos = await Todos.find(Todos.user.id == usr.id).to_list()
        return user_todos

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/todos')
async def get_todos(curr_user: str | dict = Depends(current_user)):
    usr = await User.find_one(User.email == curr_user)

    if not usr:
        raise HTTPException(status_code=400, detail="Unauthorized")

    return await Todos.find(Todos.user.id == usr.id).to_list()

@app.put('/todos/{todo_id}')
async def update_todo(todo_id: PydanticObjectId, todo_data: TodoUpdate, usr: str | dict = Depends(current_user)):
    try:
        if type(usr) is not str:
            raise HTTPException(status_code=400, detail="Unauthorized")

        to_update_todos = await Todos.find_one(Todos.id == todo_id)

        if to_update_todos is None:
            raise HTTPException(status_code=400, detail="Dosent Exists")

        to_update_todos.task = todo_data.task
        to_update_todos.completed = todo_data.completed
        await to_update_todos.save()

        return {"message": "Updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id: PydanticObjectId, curr_user: str | dict = Depends(current_user)):
    try:
        if type(curr_user) is not str:
            return {"message": "Unauthorized"}

        del_item = await Todos.find_one(Todos.id == todo_id)
        if del_item is None:
            raise HTTPException(status_code=400, detail="Dosent Exists")
        await del_item.delete()
        return {"message": "deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

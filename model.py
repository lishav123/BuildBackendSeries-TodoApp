from pydantic import BaseModel
from beanie import Document, Link, Indexed

class User(Document):
    username: str
    email: Indexed(str, unique=True)
    password: str

class Todos(Document):
    task: str
    completed: bool
    user: Link[User]

class SendTodo(BaseModel):
    task: str
    completed: bool = False

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class TodoUpdate(BaseModel):
    task: str
    completed: bool
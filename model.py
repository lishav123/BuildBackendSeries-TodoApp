from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class CreateUser(User):
    username: str

class Todo(BaseModel):
    id: int
    task: str
    completed: bool

class CreateTodo(BaseModel):
    task: str
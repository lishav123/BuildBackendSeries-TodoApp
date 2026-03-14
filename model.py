from pydantic import BaseModel

class User(BaseModel):
    usersname: str
    email: str
    password: str

class Todo(BaseModel):
    id: int
    task: str
    completed: bool

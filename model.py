from pydantic import BaseModel
from beanie import Document, Link, Indexed

class User(Document):
    username: str
    email: Indexed(str, unique=True)
    password: Indexed(str)
    password: str

class Todos(Document):
    task: str
    completed: bool
    user: Link[User]
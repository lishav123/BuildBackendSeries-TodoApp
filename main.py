from fastapi import FastAPI
from model import User, CreateUser

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
def register_user(user: CreateUser):
    return {"message": f"User registered with username {user.username}"}

@app.post("/login")
def login_user(user: User):
    return {"message": f"User logged in with mail {user.email}"}

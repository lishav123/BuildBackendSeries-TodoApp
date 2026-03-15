from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from model import User, CreateUser
from database import lifespan

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
def register_user(user: CreateUser):
    return {"message": f"User registered with username {user.username}"}

@app.post("/login")
def login_user(user: User):
    return {"message": f"User logged in with mail {user.email}"}

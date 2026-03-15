from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import User
from database import lifespan

from pymongo.errors import DuplicateKeyError

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501/"],
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"], # Allows all headers
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
async def register_user(user: User):
    try:
        await user.insert()
        return {"message": f"User registered"}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/login")
def login_user(user: User):
    return {"message": f"User logged in with mail {user.email}"}

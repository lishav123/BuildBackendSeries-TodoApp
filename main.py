from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import User, UserLogin
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
async def login_user(user: UserLogin):
    usr = await User.find_one(User.email == user.email, User.password == user.password)

    if not usr:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {"message": f"User logged in", "username": usr.username, "token": "123456"}

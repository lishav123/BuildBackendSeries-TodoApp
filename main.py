import os
from dotenv import load_dotenv
import jwt

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from model import User, UserLogin, Todos, SendTodo
from database import lifespan

from pymongo.errors import DuplicateKeyError

load_dotenv()
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
        return {
            "message": f"User registered",
            "token": jwt.encode({
                "email": user.email
            }, os.getenv("JWT_SECRECT"), algorithm="HS256")
        }

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/login")
async def login_user(user: UserLogin):
    usr = await User.find_one(User.email == user.email, User.password == user.password)

    if not usr:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {
        "message": f"User logged in",
        "username": usr.username,
        "token": jwt.encode({
            "email": user.email
        }, os.getenv("JWT_SECRECT"), algorithm="HS256")
    }

#
# @app.post('/todos')
# async def add_todos(todos: SendTodo, token: str = Header()):
#
#     try:
#         email = jwt.decode(token, os.getenv("JWT_SECRECT"), algorithms=["HS256"])
#         print(email["email"])
#         usr = await User.find_one(User.email == email["email"])
#         print(usr)
#
#         if not usr:
#             raise HTTPException(status_code=400, detail="Unauthorized")
#
#         todos = Todos(
#             task=todos.task,
#             completed=todos.completed,
#             user=usr
#         )
#
#         await todos.insert()
#         return await Todos.find(Todos.user.id == usr.id).to_list()
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=400, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


@app.post('/todos')
async def add_todos(todo_data: SendTodo, token: str = Header()):  # Renamed to todo_data
    try:
        # Decode token
        payload = jwt.decode(token, os.getenv("JWT_SECRECT"), algorithms=["HS256"])

        # Find user
        usr = await User.find_one(User.email == payload["email"])

        if not usr:
            raise HTTPException(status_code=400, detail="Unauthorized")

        # Create new todo
        new_todo = Todos(
            task=todo_data.task,
            completed=todo_data.completed,
            user=usr
        )

        # Insert it
        await new_todo.insert()

        # THE BULLETPROOF QUERY: Bypass Beanie's python operators and use raw MongoDB syntax
        user_todos = await Todos.find({Todos.user.email: usr.email}).to_list()
        print(user_todos)
        return user_todos

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from model import User, Todos

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database connection started")
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    await init_beanie(database=client.todoapp, document_models=[User, Todos])
    print("Connected to MongoDB!")
    yield
    client.close()
    print("Disconnected from MongoDB!")

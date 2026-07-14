from fastapi import FastAPI
from dotenv import load_dotenv
from routes import base

load_dotenv(".env")

app = FastAPI()
app.include_router(base.base_router)


# @app.get("/api/process")
# def process():
#     return {"message": "Processing request..."}


# @app.get("/api/search")
# def search():
#     return {"message": "Searching..."}


# @app.get("/api/answer")
# def answer():
#     return {"message": "Providing answer..."}

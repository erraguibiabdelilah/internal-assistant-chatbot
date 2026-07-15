from fastapi import FastAPI
from dotenv import load_dotenv
from routers import router

load_dotenv(".env")

app = FastAPI()
app.include_router(router.api_router)


# @app.get("/api/process")
# def process():
#     return {"message": "Processing request..."}


# @app.get("/api/search")
# def search():
#     return {"message": "Searching..."}


# @app.get("/api/answer")
# def answer():
#     return {"message": "Providing answer..."}

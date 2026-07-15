
from fastapi import APIRouter
from routers import documents

api_router = APIRouter()

api_router.include_router(documents.router)

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

base_router = APIRouter(prefix="/api")


@base_router.get("/")
async def welcome():
    return {"message": "Welcome to the API!"}


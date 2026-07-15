from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from services.s3_service import s3_service
import io
import os

router = APIRouter(prefix="/api/documents",tags=["Documents"])


@router.get("/")
async def list_documents(prefix: str = "offcourse_doc/"):
    try:
        documents = s3_service.list_documents(prefix)
        return {
            "success": True,
            "count": len(documents),
            "documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

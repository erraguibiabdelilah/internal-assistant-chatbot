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



@router.get("/download")

async def download_documents(prefix: str = "offcourse_doc/"):

    try:
        documents = s3_service.list_documents(prefix)
        downloaded_files = []
        for doc in documents:
            local_path = os.path.join("assets", doc['filename'])
            s3_service.download_document(doc['key'], local_path)
            downloaded_files.append({
                "filename": doc['filename'],
                "local_path": local_path,
                "size": doc['size']
            })
        return {
            "success": True,
            "message": f"{len(downloaded_files)} fichiers téléchargés dans /assets",
            "files": downloaded_files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


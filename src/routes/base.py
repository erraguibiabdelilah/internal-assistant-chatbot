from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.s3_service import S3Service
import os

base_router = APIRouter(prefix="/api")


@base_router.get("/")
async def welcome():
    return {"message": "Welcome to the API!"}


@base_router.get("/download")
async def download_documents():
    """Télécharge tous les documents depuis S3"""
    try:
        s3 = S3Service()
        keys = s3.list_documents()
        downloaded_files = []
        
        for key in keys:
            local_path = s3.download(key)
            downloaded_files.append({
                "key": key,
                "local_path": local_path
            })
        
        return {
            "success": True,
            "downloaded_count": len(downloaded_files),
            "files": downloaded_files,
            "error": None
        }
    except Exception as exc:
        return {
            "success": False,
            "downloaded_count": 0,
            "files": [],
            "error": str(exc)
        }


@base_router.get("/list-documents")
async def list_documents():
    """Liste tous les documents disponibles sur S3"""
    try:
        s3 = S3Service()
        keys = s3.list_documents()
        return {
            "success": True,
            "count": len(keys),
            "documents": keys,
            "error": None
        }
    except Exception as exc:
        return {
            "success": False,
            "count": 0,
            "documents": [],
            "error": str(exc)
        }


@base_router.get("/download/{document_key:path}")
async def download_single_document(document_key: str):
    """Télécharge un document spécifique depuis S3 et le retourne"""
    try:
        s3 = S3Service()
        local_path = s3.download(document_key)
        
        if not os.path.exists(local_path):
            raise HTTPException(status_code=404, detail="Fichier non trouvé après téléchargement")
        
        # Retourne le fichier pour téléchargement direct
        filename = os.path.basename(local_path)
        return FileResponse(
            path=local_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléchargement: {str(exc)}")
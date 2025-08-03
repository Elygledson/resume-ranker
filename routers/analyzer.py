import os
import uuid
import logging

from uuid import UUID
from typing import Optional
from celery_app.tasks import analyze_resume
from fastapi import APIRouter, Form, HTTPException, UploadFile


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

analyzer = APIRouter()


@analyzer.post(
    "/analyze-resume",
    status_code=200,
    summary="Analisar currículos e identificar o melhor candidato")
async def analyze(
    files: list[UploadFile],
    query: Optional[str] = Form(
        default=None, description="Consulta textual a ser feita nos currículos"),
    request_id: UUID = Form(..., description="Identificador da requisição"),
    user_id: UUID = Form(...,
                         description="Identificador do usuário solicitante")
):
    paths: list[str] = []

    for file in files:
        if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400, detail=f"Arquivo não suportado: {file.filename}")

    for file in files:
        unique_id = uuid.uuid4()
        filename = f"{unique_id}_{file.filename}"
        file_location = os.path.join(UPLOAD_DIR, filename)

        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        paths.append(file_location)

    analyze_resume.delay(paths, str(user_id), str(request_id), query)

    return {"message": "os currículos foram enviados para análises"}

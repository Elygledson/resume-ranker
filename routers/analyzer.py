import os
import uuid
import logging

from uuid import UUID
from typing import List, Optional
from services.log_service import LogService
from celery_app.tasks import analyze_resume, get_log_service
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from schemas import LogCreateSchema, Status, ResumeAnalysisStartedResponse


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

analyzer = APIRouter()


@analyzer.post(
    "/analyze-resume",
    status_code=200,
    response_model=ResumeAnalysisStartedResponse,
    summary="Analisar currículos e identificar o melhor candidato")
async def analyze(
    files: List[UploadFile],
    query: Optional[str] = Form(
        default=None, description="Consulta textual a ser feita nos currículos"),
    request_id: UUID = Form(..., description="Identificador da requisição"),
    user_id: UUID = Form(...,
                         description="Identificador do usuário solicitante"),
    log_service: LogService = Depends(get_log_service)
):
    paths: List[str] = []

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

    log = log_service.create(LogCreateSchema(
        request_id=str(request_id),
        user_id=str(user_id),
        query=query,
        status=Status.PROCESSING
    ))

    analyze_resume.delay(paths, log.id, query)

    return ResumeAnalysisStartedResponse(log_id=log.id)

import os
import uuid
import logging

from uuid import UUID
from http import HTTPStatus
from typing import List, Optional
from config import celery, settings
from config import get_mongo_collection
from services.log_service import LogService
from repositories import LogRepositoryMongo
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from schemas import LogCreateSchema, Status, ResumeAnalysisStartedResponse


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

analyzer = APIRouter()

def get_log_service() -> LogService:
    repo = LogRepositoryMongo(get_mongo_collection('logs'))
    return LogService(repo)


@analyzer.post(
    "/analyze-resume",
    status_code=HTTPStatus.OK,
    response_model=ResumeAnalysisStartedResponse,
    summary="Analisar currículos e identificar o melhor candidato",
    description="Recebe uma lista de arquivos (PDFs ou imagens), armazena-os e inicia uma tarefa para análise dos currículos.")
async def analyze(
    files: List[UploadFile],
    query: Optional[str] = Form(
        default=None, description="Consulta textual a ser feita nos currículos"),
    request_id: UUID = Form(..., description="Identificador da requisição"),
    user_id: UUID = Form(...,
                         description="Identificador do usuário solicitante"),
    log_service: LogService = Depends(get_log_service)
):
    """
    Inicia a análise de currículos enviados e retorna o ID do log associado à análise.

    Args:
        files (List[UploadFile]): Lista de arquivos enviados (PDFs ou imagens).
        query (Optional[str]): Consulta textual para filtrar ou guiar a análise.
        request_id (UUID): ID da requisição.
        user_id (UUID): ID do usuário que fez a requisição.
        log_service (LogService): Serviço de log injetado via dependência.

    Raises:
        HTTPException: Se algum arquivo estiver em formato não suportado.

    Returns:
        ResumeAnalysisStartedResponse: Contém o ID do log da análise iniciada.
    """

    filenames: List[str] = []

    for file in files:
        if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400, detail=f"Arquivo não suportado: {file.filename}")

    for file in files:
        unique_id = uuid.uuid4()
        filename = f"{unique_id}_{file.filename}"
        file_location = os.path.join(settings.STORAGE, filename)

        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        filenames.append(filename)

    log = log_service.create(LogCreateSchema(
        request_id=str(request_id),
        user_id=str(user_id),
        query=query,
        status=Status.PROCESSING
    ))
    celery.send_task("tasks.analyze_resume", args=[log.id, filenames, query])
    return ResumeAnalysisStartedResponse(log_id=log.id)

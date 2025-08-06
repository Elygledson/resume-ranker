import logging

from http import HTTPStatus
from typing import Optional, List
from config import get_mongo_collection
from services.log_service import LogService
from repositories import LogRepositoryMongo
from fastapi import APIRouter, Depends, Query
from schemas import LogOutputSchema, PaginatedLogsSchema

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logs = APIRouter()


def get_log_service() -> LogService:
    """Inicializa e retorna uma instância do serviço de logs."""
    repo = LogRepositoryMongo(get_mongo_collection('logs'))
    return LogService(repo)


@logs.patch(
    "/logs/{log_id}/feedback",
    response_model=LogOutputSchema,
    summary="Atualizar feedback de log",
    description="Atualiza o campo de feedback (positivo/negativo) de um resultado específico."
)
def patch(
    log_id: str,
    feedback: bool,
    log_service: LogService = Depends(get_log_service)
):
    """
    Atualiza o campo de feedback de um log específico.

    Args:
        log_id (str): ID do log a ser atualizado.
        feedback (bool): Valor booleano do feedback (True para positivo, False para negativo).
        log_service (LogService): Serviço de log injetado via dependência.

    Returns:
        LogOutputSchema: Log atualizado com o novo feedback.
    """
    return log_service.patch_feedback(log_id, feedback)


@logs.get(
    "/logs/paginated",
    status_code=HTTPStatus.OK,
    response_model=PaginatedLogsSchema,
    summary="Listar logs com paginação",
    description="Retorna uma lista paginada de logs."
)
def get_all_paginated(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Número máximo de registros para retornar"),
    log_service: LogService = Depends(get_log_service)
):
    """
    Lista paginada de logs.

    Args:
        skip (int): Quantos registros pular (offset).
        limit (int): Quantos registros retornar (limite).
        log_service (LogService): Serviço de log injetado via dependência.

    Returns:
        PaginatedLogsSchema: logs registrados paginados.
    """
    return log_service.get_all_paginated(skip=skip, limit=limit)


@logs.get(
    "/logs/{id}",
    status_code=HTTPStatus.OK,
    response_model=Optional[LogOutputSchema],
    summary="Buscar log por ID",
    description="Retorna um log específico com base no ID fornecido."
)
def get_one(
    id: str,
    log_service: LogService = Depends(get_log_service)
):
    """
    Retorna um log específico pelo ID.

    Args:
        id (str): ID do log no banco de dados.
        log_service (LogService): Serviço de log injetado via dependência.

    Returns:
        Optional[LogOutputSchema]: Log correspondente ao ID, se existir.
    """
    return log_service.get(id)


@logs.get(
    "/logs",
    status_code=HTTPStatus.OK,
    response_model=List[LogOutputSchema],
    summary="Listar todos os logs",
    description="Retorna uma lista de todos os logs armazenados no sistema."
)
def get_all(
    log_service: LogService = Depends(get_log_service)
):
    """
    Lista todos os logs cadastrados no sistema.

    Args:
        log_service (LogService): Serviço de log injetado via dependência.

    Returns:
        List[LogOutputSchema]: Lista de logs registrados.
    """
    return log_service.get_all()

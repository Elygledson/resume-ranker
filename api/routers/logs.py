import logging
from http import HTTPStatus
from typing import Optional, List

from fastapi import APIRouter, Depends

from config import get_mongo_collection
from services.log_service import LogService
from repositories import LogRepositoryMongo
from schemas.logs_schemas import LogOutputSchema

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

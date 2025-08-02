import logging
from http import HTTPStatus
from typing import Optional, List
from fastapi import APIRouter, Depends
from repositories import LogRepositoryMongo
from services.log_service import LogService
from config.database import get_mongo_collection
from schemas.logs_schemas import LogCreateSchema, LogOutputSchema

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logs = APIRouter()


def get_log_service() -> LogService:
    repo = LogRepositoryMongo(get_mongo_collection('logs'))
    return LogService(repo)


@logs.post(
    "/logs",
    status_code=HTTPStatus.CREATED,
    response_model=LogOutputSchema,
    summary="Criar log",
    description="Cria um novo log no banco de dados MongoDB."
)
async def create(
    log_create_schema: LogCreateSchema,
    log_service: LogService = Depends(get_log_service)
):
    """
    Cria um novo log.

    - **request_id**: ID da requisição
    - **user_id**: ID do usuário que gerou o log
    - **timestamp**: Data/hora do log
    - **query**: Pergunta feita pelo usuário
    - **resultado**: Resposta gerada
    """
    return await log_service.create(log_create_schema)


@logs.get(
    "/logs/{id}",
    status_code=HTTPStatus.OK,
    response_model=Optional[LogOutputSchema],
    summary="Buscar log por ID",
    description="Retorna um log específico a partir do ID fornecido."
)
async def get_one(
    id: str,
    log_service: LogService = Depends(get_log_service)
):
    """
    Retorna um log específico.

    - **id**: ID do log no banco de dados
    """
    return await log_service.get(id)


@logs.get(
    "/logs",
    status_code=HTTPStatus.OK,
    response_model=List[LogOutputSchema],
    summary="Listar todos os logs",
    description="Retorna uma lista com todos os logs armazenados."
)
async def get_all(
    log_service: LogService = Depends(get_log_service)
):
    """
    Lista todos os logs cadastrados no sistema.
    """
    return await log_service.get_all()


@logs.delete(
    "/logs/{id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Remover log",
    description="Remove um log específico do banco de dados."
)
async def delete(
    id: str,
    log_service: LogService = Depends(get_log_service)
):
    """
    Remove um log pelo ID.

    - **id**: ID do log que será deletado
    """
    await log_service.delete(id)

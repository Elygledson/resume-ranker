import logging

from celery_app import app
from typing import Optional
from services.log_service import LogService
from config.database import get_mongo_collection
from services import TextProcessorService, ResumeAnalyzerService
from repositories.logs_repository_mongo import LogRepositoryMongo
from schemas import LogCreateSchema, Status, AnalysisOutputSchema, SummaryResume

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_log_service() -> LogService:
    repo = LogRepositoryMongo(get_mongo_collection('logs'))
    return LogService(repo)


@app.task
def analyze_resume(paths: list[str], user_id: str, request_id: str, query: Optional[str] = None) -> None:
    log_service = get_log_service()
    text_processor = TextProcessorService()
    analyzer_service = ResumeAnalyzerService()

    resumes: list[SummaryResume] = []

    try:
        logger.info(
            f"Processando arquivos para request_id={request_id}, user_id={user_id}"
        )

        for filepath in paths:
            logger.debug(f"Extraindo texto de {filepath}")
            content = text_processor.extract_content(filepath)
            summary = analyzer_service.generate_summary(content)
            resumes.append(summary)

        resultado = AnalysisOutputSchema(resumes=resumes, justification=None)

        if query:
            logger.debug(f"Analisando com query: {query}")
            resultado.justification = analyzer_service.find_best_resume(
                query, resumes)

        logger.info(f"Análise concluída para request_id={request_id}")
        log_service.create(LogCreateSchema(
            request_id=request_id,
            user_id=user_id,
            resultado=resultado,
            query=query,
            status=Status.PROCESSED
        ))

    except Exception as e:
        logger.exception(
            f"Erro ao processar os currículos para request_id={request_id} {e}"
        )
        log_service.create(LogCreateSchema(
            request_id=request_id,
            user_id=user_id,
            resultado=None,
            query=query,
            status=Status.PROCESSING_FAILED
        ))

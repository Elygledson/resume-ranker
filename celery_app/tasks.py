import logging

from celery_app import app
from typing import List, Optional
from config import get_mongo_collection
from repositories import LogRepositoryMongo
from schemas import LogUpdateSchema, Status, AnalysisOutputSchema, SummaryResume
from services import ResumeAnalyzerService, VisionTextProcessor, LogService, get_matcher

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_log_service() -> LogService:
    repo = LogRepositoryMongo(get_mongo_collection('logs'))
    return LogService(repo)


@app.task
def analyze_resume(paths: List[str], log_id: str, query: Optional[str] = None) -> None:
    resumes: List[SummaryResume] = []
    matcher = get_matcher("ollama")
    log_service = get_log_service()
    vision_text_processor = VisionTextProcessor()
    resume_analyzer = ResumeAnalyzerService(matcher)

    log = log_service.get(log_id)
    if not log:
        logger.error(f"Log com ID {log_id} não encontrado.")
        return

    try:
        logger.info("Iniciando o processamento dos arquivos")
        for filepath in paths:
            logger.debug(f"Extraindo texto de {filepath}")
            content = vision_text_processor.extract_content(filepath)
            summary = resume_analyzer.generate_summary(content)
            resumes.append(summary)

        resultado = AnalysisOutputSchema(resumes=resumes, justification=None)

        if query:
            logger.debug(f"Analisando com query: {query}")
            resultado.justification = resume_analyzer.find_best_resume(
                query, resumes)

        logger.info(f"Processamento dos currículos finalizado com sucesso.")

        log_service.update(
            log.id,
            LogUpdateSchema(status=Status.PROCESSED, resultado=resultado)
        )

    except Exception as e:
        logger.exception(f"Erro ao processar os currículos {e}")
        log_service.update(log.id, LogUpdateSchema(
            status=Status.PROCESSING_FAILED))

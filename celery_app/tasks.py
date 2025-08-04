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
        logger.info(
            f"[log_id={log_id}] Iniciando o processamento dos arquivos")
        for filepath in paths:
            logger.debug(f"Extraindo texto de {filepath}")
            content = vision_text_processor.extract_content(filepath)
            summary = resume_analyzer.generate_summary(content)
            resumes.append(summary)

        final_resumes = resumes
        justification = None

        if query:
            logger.debug(f"Analisando com query: {query}")
            top_k_resumes = resume_analyzer.rank_resumes(query, resumes)
            final_resumes = top_k_resumes
            justification = resume_analyzer.generate_justification(query, top_k_resumes)

        logger.info(f"Processamento dos currículos finalizado com sucesso.")
        resultado = AnalysisOutputSchema(resumes=final_resumes, justification=justification)
        log_service.update(
            log.id,
            LogUpdateSchema(status=Status.PROCESSED, resultado=resultado)
        )
    except Exception as e:
        logger.exception(f"Erro ao processar os currículos {e}")
        log_service.update(log.id, LogUpdateSchema(
            status=Status.PROCESSING_FAILED))

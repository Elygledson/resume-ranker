import logging

from config import app
from settings import settings
from pymongo import MongoClient
from typing import List, Optional
from services.factory import get_matcher
from services.vision_text_processor import VisionTextProcessor
from services.resume_analyzer_service import ResumeAnalyzerService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_mongo_collection(collection_name: str):
    client = MongoClient(settings.database_url)
    db = client[settings.MONGO_INITDB_ROOT_DBNAME]
    return db.get_collection(collection_name)


@app.task
def analyze_resume(paths: List[str], log_id: str, query: Optional[str] = None) -> None:
    matcher = get_matcher("ollama")
    vision_text_processor = VisionTextProcessor()
    resume_analyzer = ResumeAnalyzerService(matcher)
    database = get_mongo_collection('logs')

    log = database.find_one({"_id": log_id})
    if not log:
        logger.error(f"Log com ID {log_id} não encontrado.")
        return

    try:
        logger.info(
            f"[log_id={log_id}] Iniciando o processamento dos arquivos")
        resumes = []

        for filepath in paths:
            logger.debug(f"Extraindo texto de {filepath}")
            content = vision_text_processor.extract_content(filepath)
            summary = resume_analyzer.generate_summary(content)
            resumes.append(summary)

        final_resumes = resumes
        justification = None

        if query:
            logger.debug(f"Analisando com query: {query}")
            final_resumes = resume_analyzer.rank_resumes(query, resumes)
            justification = resume_analyzer.generate_justification(
                query, final_resumes)

        logger.info(f"Processamento dos currículos finalizado com sucesso.")

        database.update_one(
            {"_id": log_id},
            {"$set": {
                "status": "PROCESSED",
                "resultado": {
                    "resumes": [r.model_dump() if hasattr(r, 'dict') else r for r in final_resumes],
                    "justification": justification
                }
            }}
        )

    except Exception as e:
        logger.exception(f"Erro ao processar os currículos {e}")
        database.update_one(
            {"_id": log_id},
            {"$set": {"status": "PROCESSING_FAILED"}}
        )

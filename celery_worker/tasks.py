import os
import logging

from bson import ObjectId
from settings import settings
from pymongo import MongoClient
from config import celery_worker
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


@celery_worker.task
def analyze_resume(log_id: str, filenames: List[str], query: Optional[str] = None) -> None:
    database = get_mongo_collection('logs')

    log = database.find_one({"_id": ObjectId(log_id)})
    if not log:
        logger.error(f"Log com ID {log_id} não encontrado.")
        return

    try:
        logger.info(
            f"[log_id={log_id}] Iniciando o processamento dos arquivos")

        resumes = []
        vision_text_processor = VisionTextProcessor()
        matcher = get_matcher(settings.AI_SERVICE_NAME)
        resume_analyzer = ResumeAnalyzerService(matcher)

        for filename in filenames:
            logger.debug(f"Extraindo texto de {filename}")
            filepath = os.path.join(settings.STORAGE, filename)
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
            {"_id": ObjectId(log_id)},
            {"$set": {
                "status": "PROCESSED",
                "result": {
                    "resumes": [r.model_dump() if hasattr(r, 'dict') else r for r in final_resumes],
                    "justification": justification
                }
            }}
        )

    except Exception as e:
        logger.exception(f"Erro ao processar os currículos {e}")
        database.update_one(
            {"_id": ObjectId(log_id)},
            {"$set": {"status": "PROCESSING_FAILED"}}
        )

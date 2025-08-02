import logging

from typing import Optional
from schemas.analysis_schemas import AnalysisOutput
from fastapi import APIRouter, Form, HTTPException, UploadFile


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

analyzer = APIRouter()


@analyzer.post(
    "/analyze-resume",
    status_code=201,
    response_model=AnalysisOutput,
    summary="Analisar currículos e identificar o melhor candidato",
    description="""
Este endpoint recebe uma lista de arquivos de currículos (em formato PDF, JPG ou PNG) juntamente com uma consulta textual (`query`).

Com base na query fornecida, a API analisa os currículos e retorna:
- O candidato mais compatível com a consulta (`best_candidate`)
- Um sumário de cada currículo
- A justificativa da escolha
- Um score de compatibilidade (`best_fit_score`)

Se a `query` não for informada, o endpoint pode ser ajustado para retornar apenas os sumários de cada currículo.

**Requisitos dos arquivos**:
- Tipos aceitos: `application/pdf`, `image/jpeg`, `image/png`

**Campos obrigatórios**:
- `files`: lista de currículos
- `request_id`: ID da requisição
- `user_id`: identificador do usuário solicitante
"""
)
async def analyze(
    files: list[UploadFile] = Form(...,
                                   description="Arquivos PDF ou imagens dos currículos"),
    query: Optional[str] = Form(
        default=None, description="Consulta textual a ser feita nos currículos"),
    request_id: int = Form(..., description="Identificador da requisição"),
    user_id: int = Form(...,
                        description="Identificador do usuário solicitante")
):
    for file in files:
        if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400, detail=f"Arquivo não suportado: {file.filename}")

    pass

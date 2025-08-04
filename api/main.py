import uvicorn

from fastapi import FastAPI
from routers import analyzer, logs
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


security = HTTPBasic()

app = FastAPI(
    title='ANALISADOR DE CURRÍCULOS',
    description=(
        "API responsável por analisar, resumir e comparar currículos com base em uma "
        "descrição de vaga ou perfil desejado. Utiliza modelos de linguagem natural para "
        "extrair resumos detalhados e identificar o candidato mais adequado a partir de critérios fornecidos."
    ),
    version="1.0.0",
)

app.include_router(analyzer, prefix='/api/v1', tags=['analyzer'])
app.include_router(logs, prefix='/api/v1', tags=['logs'])

app.mount("/api/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

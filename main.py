import uvicorn
import secrets

from config import settings
from routers import analyzer, logs
from fastapi import Depends, FastAPI
from fastapi import HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


security = HTTPBasic()

app = FastAPI(title='ANALISADOR DE CURRÍCULOS',
              docs_url=None, redoc_url=None, openapi_url=None)

app.include_router(analyzer, prefix='/api/v1', tags=['analyzer'])
app.include_router(logs, prefix='/api/v1', tags=['logs'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4200'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, settings.SWAGGER_USERNAME)
    correct_password = secrets.compare_digest(
        credentials.password, settings.SWAGGER_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/docs", include_in_schema=False)
async def get_documentation(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_redoc_html(openapi_url="/openapi.json", title="ReDoc")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

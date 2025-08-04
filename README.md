# ResumeRanker — Análise Inteligente de Currículos com OCR + LLM

Fabio, gerente de Talent Acquisition da startup TechMatch, enfrentava um grande desafio: analisar manualmente dezenas de currículos em PDF ou imagem todos os dias. O processo era repetitivo, demorado e o impedia de focar em decisões estratégicas de contratação.

Pensando nisso, esta aplicação foi desenvolvida para automatizar a leitura, sumarização e ranqueamento de currículos usando técnicas de OCR e modelos de linguagem (LLMs). Fabio agora pode simplesmente enviar os arquivos, fazer perguntas do tipo _"Qual currículo melhor se encaixa nessa vaga?"_ e receber respostas precisas com justificativas — economizando horas de trabalho.

---

## Funcionalidades

- Upload de múltiplos documentos (PDF, JPG/PNG)
- Extração de texto via OCR (EasyOCR)
- Geração de sumários individuais por currículo
-  Resposta a queries com justificativas baseadas nos currículos
- Registro de logs de uso com:
  - `request_id`
  - `user_id`
  - `timestamp`
  - `query`
  - `resultado`
- Sem armazenamento completo dos arquivos (apenas metadados)
- Empacotado com Docker
- Swagger interativo com exemplos de uso

---

## Tecnologias Utilizadas

- **FastAPI** — API RESTful com documentação automática (Swagger/OpenAPI)  
- **EasyOCR** — Extração de texto de imagens e PDFs  
- **MongoDB** — Banco de dados não relacional para armazenamento de logs  
- **Celery + Redis** — Processamento assíncrono e fila de tarefas  
- **Ollama ou Gemini** — Serviço de IA para geração de respostas e sumários  
- **Docker** — Empacotamento e execução da aplicação  

---

## Fluxo da Aplicação

1. Usuário envia documentos (PDFs ou imagens) via API.
2. Os arquivos são salvos no storage e os nomes são enviados para um **worker Celery**.
3. O worker:
   - Extrai texto com OCR
   - Resume o conteúdo
   - Gera embeddings
   - Calcula a similaridade com a vaga usando **distância do cosseno**
4. Apenas documentos com **score > 60%** são enviados para avaliação do modelo LLM.
5. O modelo retorna os currículos que mais combinam com a vaga, com **justificativas claras**.
6. A execução é registrada no MongoDB para fins de auditoria e rastreabilidade.

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Elygledson/resume-analyzer
cd seu-repositorio
```

---

## Configure o .env

### 2. Crie um arquivo .env com o seguinte conteúdo:

```bash
# REDIS
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# AI SERVICE
AI_SERVICE_NAME=ollama  # ou gemini
AI_SERVICE_KEY=http://localhost:11434/api  # ou sua chave da Gemini

# MONGODB
MONGO_INITDB_ROOT_PORT=27017
MONGO_INITDB_ROOT_DBNAME=teste
MONGO_INITDB_ROOT_HOST=localhost
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123
```

---

## Execute com Docker Compose

```bash
docker compose up -d --build
```

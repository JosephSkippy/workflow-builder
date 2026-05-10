import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_tables, seed_train_data, seed_workflows
from app.executions.router import router as executions_router
from app.workflows.router import router as workflows_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seeding on startup is fine for dev/POC — in prod, use migrations (Alembic) and separate seed scripts.
    create_tables()
    seed_train_data()
    seed_workflows()
    yield


app = FastAPI(title="Mini Workflow Builder API", version="0.1.0", lifespan=lifespan)

app.include_router(workflows_router, prefix="/api")
app.include_router(executions_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}

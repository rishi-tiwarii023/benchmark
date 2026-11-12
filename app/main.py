from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import Base, engine
from app.routes.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Task Manager", lifespan=lifespan)
app.include_router(tasks_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

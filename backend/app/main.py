from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.wellness import router as wellness_router
from app.api.training_sessions import router as training_router
from app.api.pt import router as pt_router
from app.core.database import Base, engine

@asynccontextmanager
async def lifespan(app):
    # Add missing tables only; existing tables and records are preserved.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Athlete Recovery & Rehab Tracker", lifespan=lifespan)
for router in (training_router, wellness_router, pt_router):
    app.include_router(router)
    app.include_router(router, prefix="/api", include_in_schema=False)

@app.get("/health")
def health():
    return {"status": "ok"}

frontend = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if frontend.is_dir():
    app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")
else:
    @app.get("/")
    def read_root():
        return {"message": "Athlete Recovery & Rehab Tracker API"}

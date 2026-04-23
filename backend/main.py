from fastapi import FastAPI

from backend.api.routes import router as api_router


app = FastAPI(title="proyecto_salud_agentes")
app.include_router(api_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}


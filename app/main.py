from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import folders, health

app = FastAPI(title="Lista API", version="0.1.0")

# TODO: lock this down to the real app/staging origins before launch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(folders.router, prefix="/folders", tags=["folders"])


@app.get("/")
def root():
    return {"service": "lista-api", "status": "ok"}

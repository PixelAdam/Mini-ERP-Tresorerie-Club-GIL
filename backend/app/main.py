from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import membres, cotisations, evenements, sponsors, transactions

# Créer les tables si elles n'existent pas encore
import app.models  # noqa: F401 — force l'import de tous les modèles
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini ERP — Club GIL",
    description="API de gestion de trésorerie du Club GIL : membres, cotisations, événements, sponsors et transactions.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS (autoriser le frontend HTML à appeler l'API) ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ En production, remplacer par l'URL exacte du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Enregistrement des routers ─────────────────────────────────────────────────
app.include_router(membres.router)
app.include_router(cotisations.router)
app.include_router(evenements.router)
app.include_router(sponsors.router)
app.include_router(transactions.router)


@app.get("/", tags=["Accueil"])
def root():
    return {
        "message": "Bienvenue sur l'API Mini ERP Club GIL 🎓",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Accueil"])
def health_check():
    return {"status": "ok"}

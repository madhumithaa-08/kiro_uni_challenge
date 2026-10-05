"""FastAPI application factory for DSA Vault."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import learn, progress, review, solutions


def create_app() -> FastAPI:
    app = FastAPI(
        title="DSA Vault API",
        version="1.0.0",
        description="Local-first DSA tracker, notes, and spaced-repetition tool.",
    )

    # Vite dev server runs on 5173; allow it to call the API in development.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "dsa-vault"}

    app.include_router(solutions.router)
    app.include_router(progress.router)
    app.include_router(review.router)
    app.include_router(learn.router)
    return app


app = create_app()

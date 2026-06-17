from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.routers import game, optimization

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="PriceBattle", description="Симулятор конкурентного ценообразования")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(game.router, prefix="/game", tags=["Game"])
app.include_router(optimization.router, prefix="/optimize", tags=["Optimization"])

@app.get("/")
async def home():
    return FileResponse(str(BASE_DIR / "static" / "index.html"))
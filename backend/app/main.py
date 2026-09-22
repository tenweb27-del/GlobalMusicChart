
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.routes import router

app = FastAPI(title="Global Music Chart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder automatically
os.makedirs("uploads", exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "healthy"}
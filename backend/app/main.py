from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router


app = FastAPI(
    title="Global Music Chart API",
    description="The official backend powering the Global Music Chart ecosystem.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
@app.get("/")
async def home():
    return {
        "platform": "Global Music Chart",
        "status": "Foundation Day",
        "version": "0.1.0",
        "message": "Welcome to the future of music analytics."
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
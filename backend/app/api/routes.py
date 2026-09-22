
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from app.models.artist import ArtistRegistration
import os
import shutil
import time
import requests
import json

router = APIRouter(prefix="/api", tags=["Global Music Chart"])

PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")
DATA_FILE = "arena_posts.json"

# ---------------- Arena Storage ----------------

def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

# ---------------- Models ----------------

class ArenaSubmission(BaseModel):
    artist_name: str
    title: str
    media_type: str
    description: str | None = ""

class TurboRequest(BaseModel):
    email: str

class VoteBundleRequest(BaseModel):
    email: str
    bundle: int

# ---------------- General ----------------

@router.get("/about")
async def about():
    return {
        "name": "Global Music Chart",
        "mission": "Building the world's most transparent music intelligence platform.",
        "status": "Growing"
    }

@router.get("/countries")
async def countries():
    return {
        "supported": [
            "Ghana",
            "Nigeria",
            "South Africa",
            "United Kingdom",
            "United States"
        ]
    }

@router.post("/artist/register")
async def register_artist(artist: ArtistRegistration):
    return {
        "message": "Artist registered successfully.",
        "artist": artist.artist_name,
        "country": artist.country,
        "genre": artist.genre
    }

# ---------------- Charts ----------------

@router.get("/charts/global/top10")
async def global_top10():
    return [
        {"rank":1,"song":"Not Like Us","artist":"Kendrick Lamar","trend":"up"},
        {"rank":2,"song":"Houdini","artist":"Eminem","trend":"up"},
        {"rank":3,"song":"Water","artist":"Tyla","trend":"steady"},
        {"rank":4,"song":"Unavailable","artist":"Davido","trend":"down"},
        {"rank":5,"song":"Terminator","artist":"King Promise","trend":"up"},
        {"rank":6,"song":"Sability","artist":"Ayra Starr","trend":"steady"},
        {"rank":7,"song":"Bandana","artist":"Fireboy DML & Asake","trend":"up"},
        {"rank":8,"song":"People","artist":"Libianca","trend":"down"},
        {"rank":9,"song":"Monica","artist":"Kuami Eugene","trend":"up"},
        {"rank":10,"song":"Calm Down","artist":"Rema","trend":"steady"}
    ]

# ---------------- Arena ----------------

@router.get("/arena/feed")
async def arena_feed():
    return load_posts()

@router.post("/arena/upload")
async def upload_arena_entry(
    artist_name: str = Form(...),
    title: str = Form(...),
    media_type: str = Form(...),
    description: str = Form(""),
    media_file: UploadFile = File(...)
):
    posts = load_posts()

    filename = f"{int(time.time())}_{media_file.filename}"
    filepath = os.path.join("uploads", filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(media_file.file, buffer)

    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "artist_name": artist_name,
        "media_type": media_type,
        "description": description,
        "file_url": f"http://127.0.0.1:8000/uploads/{filename}",
        "upvotes": 0,
        "downvotes": 0
    }

    posts.insert(0, new_post)
    save_posts(posts)

    return {
        "message": "Performance uploaded successfully.",
        "entry": new_post
    }

# ---------------- Paystack Turbo ----------------

@router.post("/payments/turbo/init")
async def initialize_turbo_payment(data: TurboRequest):

    if not PAYSTACK_SECRET:
        raise HTTPException(status_code=500, detail="Paystack key not configured")

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        headers={
            "Authorization": f"Bearer {PAYSTACK_SECRET}",
            "Content-Type": "application/json"
        },
        json={
            "email": data.email,
            "amount": 5000,
            "callback_url": "http://127.0.0.1:5500/frontend/arena.html"
        }
    )

    return response.json()

# ---------------- Vote Bundles ----------------

@router.post("/payments/votes/init")
async def initialize_vote_payment(data: VoteBundleRequest):

    if not PAYSTACK_SECRET:
        raise HTTPException(status_code=500, detail="Paystack key not configured")

    prices = {
        5: 500,
        15: 1200,
        50: 3500
    }

    if data.bundle not in prices:
        raise HTTPException(status_code=400, detail="Invalid bundle")

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        headers={
            "Authorization": f"Bearer {PAYSTACK_SECRET}",
            "Content-Type": "application/json"
        },
        json={
            "email": data.email,
            "amount": prices[data.bundle],
            "callback_url": "http://127.0.0.1:5500/frontend/arena.html"
        }
    )

    return response.json()
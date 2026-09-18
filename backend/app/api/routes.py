
from fastapi import APIRouter
from app.models.artist import ArtistRegistration

router = APIRouter(prefix="/api", tags=["Global Music Chart"])


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


@router.get("/charts/global/top10")
async def global_top10():
    return [
        {"rank": 1, "song": "Not Like Us", "artist": "Kendrick Lamar", "trend": "up"},
        {"rank": 2, "song": "Houdini", "artist": "Eminem", "trend": "up"},
        {"rank": 3, "song": "Water", "artist": "Tyla", "trend": "steady"},
        {"rank": 4, "song": "Unavailable", "artist": "Davido", "trend": "down"},
        {"rank": 5, "song": "Terminator", "artist": "King Promise", "trend": "up"},
        {"rank": 6, "song": "Sability", "artist": "Ayra Starr", "trend": "steady"},
        {"rank": 7, "song": "Bandana", "artist": "Fireboy DML & Asake", "trend": "up"},
        {"rank": 8, "song": "People", "artist": "Libianca", "trend": "down"},
        {"rank": 9, "song": "Monica", "artist": "Kuami Eugene", "trend": "up"},
        {"rank": 10, "song": "Calm Down", "artist": "Rema", "trend": "steady"}
    ]
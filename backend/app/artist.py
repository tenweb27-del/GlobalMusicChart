from pydantic import BaseModel, EmailStr
from typing import Optional


class ArtistRegistration(BaseModel):
    artist_name: str
    email: EmailStr
    country: str
    genre: str
    password: str
    bio: Optional[str] = None
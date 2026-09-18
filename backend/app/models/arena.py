from pydantic import BaseModel, Field
from typing import Optional, Literal


class ArenaSubmission(BaseModel):
    title: str
    artist_name: str
    description: Optional[str] = None

    media_type: Literal["video", "audio"]
    file_name: str

    duration_seconds: int = Field(..., le=60)
    file_size_mb: float = Field(..., le=50)

    age_confirmed: bool

    upvotes: int = 0
    downvotes: int = 0

    is_boosted: bool = False
    boost_expires_at: Optional[str] = None

    status: Literal["pending", "approved", "rejected"] = "pending"
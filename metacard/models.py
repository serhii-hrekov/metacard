from pydantic import BaseModel, Field
from typing import Optional

class Font(BaseModel):
    """Model representing font settings."""
    size: Optional[int] = Field(60, description="Font size in points")
    color: Optional[str] = Field("#FFFFFF", description="Font color in HEX format")
    family: Optional[str] = Field("Poppins", description="Font family name")



class Card(BaseModel):
    """Model representing a card with various attributes."""

    title: str = Field("Hello from my API!", max_length=300, description="The title for the thumbnail image")
    footer: bool = False,
    font: Optional[Font] = None
    backgroundColor: Optional[str] = Field("#1a1a1a", description="Background color in HEX format")
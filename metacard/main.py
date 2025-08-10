# In main.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
import io
import re
from fastapi import Query


# Import our generator function from the other file
from . import create_thumbnail

app = FastAPI()

@app.get("/api/generate")
async def generate_thumbnail_endpoint(
    title: str = Query("Hello from my API!", max_length=300, description="The title for the thumbnail image")
):
    """
    API endpoint to generate a thumbnail image.
    Takes a 'title' query parameter.
    """

    # Strip leading/trailing spaces
    title = title.strip()


    # Basic sanitization: remove non-printable chars
    title = re.sub(r"[^\x20-\x7E]+", "", title)

    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty.")
    
    if len(title) > 50:
        title = title[:97] + "..."

    headers = {
        "Cache-Control": "public, max-age=31536000, immutable"  # 1 year
    }

    # Generate the image data in memory
    image_bytes = create_thumbnail.generate_image(title=title)
    
    # Return the image as a streaming response
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png", headers=headers)


@app.get("/")
async def root():
    """
    Root endpoint that returns the favicon.ico image.
    """
    with open("favicon.ico", "rb") as f:
        favicon_bytes = f.read()
    return StreamingResponse(io.BytesIO(favicon_bytes), media_type="image/x-icon")


@app.get("/api/generate/{slug}.png")
async def generate_thumbnail_endpoint(
    slug: str,
    title: str = Query(..., max_length=300, description="The title for the thumbnail image"),
    footer: bool = False,

):
    """
    API endpoint to generate a thumbnail image.
    Slug is used for the image path, title is used for text in the thumbnail.
    """

    # Basic slug validation
    if not re.match(r"^[a-z0-9-]+$", slug):
        raise HTTPException(status_code=400, detail="Invalid slug format.")

    # Sanitize and trim title
    title = title.strip()
    title = re.sub(r"[^\x20-\x7E]+", "", title)  # remove non-printable chars

    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty.")

    if len(title) > 100:
        title = title[:97] + "..."

    # Cache for 1 year
    headers = {
        "Cache-Control": "public, max-age=31536000, immutable"
    }

    # Generate the image data in memory
    image_bytes = create_thumbnail.generate_image(title=title,footer=footer)

    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png", headers=headers)
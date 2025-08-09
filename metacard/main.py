# In main.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io

# Import our generator function from the other file
import create_thumbnail

app = FastAPI()

@app.get("/api/generate")
async def generate_thumbnail_endpoint(title: str = "Hello from my API!"):
    """
    API endpoint to generate a thumbnail image.
    Takes a 'title' query parameter.
    """
    # Generate the image data in memory
    image_bytes = create_thumbnail.generate_image(title=title)
    
    # Return the image as a streaming response
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")
# In main.py
# to run this shit: 
# poetry run uvicorn metacard.main:app --reload
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
import io
import re
from fastapi import Query


# Import our generator function from the other file
from . import create_thumbnail
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint to provide usage instructions.
    Returns a beautiful HTML documentation page for the API.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Metacard API Documentation</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background: #f8f9fa; color: #222; margin: 0; padding: 0; }
            .container { max-width: 700px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); padding: 32px; }
            h1 { color: #2d7ff9; margin-bottom: 0.5em; }
            h2 { color: #444; margin-top: 2em; }
            code, pre { background: #f3f3f3; border-radius: 4px; padding: 2px 6px; font-size: 1em; }
            ul { margin: 1em 0; }
            .endpoint { font-weight: bold; color: #2d7ff9; }
            .footer { margin-top: 2em; font-size: 0.95em; color: #888; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Metacard API Documentation</h1>
            <p>Generate beautiful PNG thumbnail images via HTTP API.</p>
            <h2>Endpoints</h2>
            <ul>
                <li>
                    <span class="endpoint">GET /api/generate</span><br>
                    <code>?title=Your%20Title%20Here&amp;footer=false</code>
                </li>
                <li>
                    <span class="endpoint">GET /api/generate/&lt;slug&gt;.png</span><br>
                    <code>?title=Your%20Title%20Here&amp;footer=false</code>
                </li>
            </ul>
            <h2>Parameters</h2>
            <ul>
                <li><b>title</b> <code>(string, max 300 chars)</code>: The text for the thumbnail.</li>
                <li><b>footer</b> <code>(boolean)</code>: <code>true</code> or <code>false</code> to include a footer (only for admin).</li>
            </ul>
            <h2>Response</h2>
            <ul>
                <li>Returns a <b>PNG image</b> of the generated thumbnail.</li>
            </ul>
            <h2>Example Usage</h2>
            <pre>GET /api/generate?title=Hello%20World</pre>
            <pre>GET /api/generate/my-slug.png?title=Hello%20World</pre>
            <div class="footer">
                &copy; 2024 Metacard API. Powered by FastAPI.
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/generate")
async def generate_thumbnail_endpoint(
    
    title: str = Query("Hello from my API!", max_length=300, description="The title for the thumbnail image"),
    footer: bool = False,
    backgroundColor: str = Query("#1a1a1a", description="Background color in HEX format", max_length=7),
    fontSize: int = Query(60, ge=10, le=200, description="Font size in points"),
    fontColor: str = Query("#FFFFFF", description="Font color in HEX format", max_length=7),
    authorName: str = Query("Serhii Hrekov", description="Author name", max_length=100),
     authorFontColor: str = Query("#cccccc", description="Author font color in HEX format", max_length=7),
    authorFontSize: int = Query(40, ge=10, le=100, description="Author font size in points"),
    authorWebsite: str = Query("hrekov.com", description="Author website URL", max_length=50),
    authorWebsiteFontSize: int = Query(20, ge=10, le=100, description="Author website font size in points"),
   
):
    """
   Endpoint to generate a thumbnail image with customizable text and styling options.
    Args:
        title (str): The title for the thumbnail image. Default is "Hello from my API!". Maximum length is 300 characters.
        footer (bool): Whether to include a footer in the thumbnail. Default is False.
        backgroundColor (str): Background color in HEX format. Default is "#1a1a1a". Maximum length is 7 characters.
        fontSize (int): Font size for the title text in points. Default is 60. Range is 10 to 200.
        fontColor (str): Font color in HEX format. Default is "#FFFFFF". Maximum length is 7 characters.
        authorName (str): Author name to display. Default is "Serhii Hrekov". Maximum length is 100 characters.
        authorFontColor (str): Author font color in HEX format. Default is "#cccccc". Maximum length is 7 characters.
        authorFontSize (int): Author font size in points. Default is 40. Range is 10 to 100.
        authorWebsite (str): Author website URL to display. Default is "hrekov.com". Maximum length is 50 characters.
        authorWebsiteFontSize (int): Author website font size in points. Default is 20. Range is 10 to 100.
    Returns:
        StreamingResponse: PNG image of the generated thumbnail with the specified parameters.
    Raises:
        HTTPException: If the title is empty after sanitization.
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
    image_bytes = create_thumbnail.generate_image(
        title=title,
        footer=footer,
        backgroundColor=backgroundColor,
        fontSize=fontSize,
        fontColor=fontColor,
        authorName=authorName,
        authorWebsite=authorWebsite,
        authorFontColor=authorFontColor,
        authorFontSize=authorFontSize,
        authorWebsiteFontSize=authorWebsiteFontSize,
        )
    
    # Return the image as a streaming response
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png", headers=headers)





@app.get("/api/generate/{slug}.png")
async def generate_thumbnail_endpoint_2(
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
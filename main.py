import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from summarizer import generate_summary
from fastapi import HTTPException

app = FastAPI()

# Update CORS to accept requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UrlRequest(BaseModel):
    url: str


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app"}


@app.post("/process-url")
async def process_url(request: UrlRequest):
    url = request.url

    if not url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="Invalid URL schema. Only HTTP/HTTPS URLs are allowed.",
        )

    try:
        summarized_text = generate_summary(url)
    except Exception as e:
        summarized_text = {"Topic": e}
        raise HTTPException(status_code=500, detail=str(e))

    return summarized_text

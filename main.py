import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from summarizer import generate_summary
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://lgpjnfflgaaecenaeikciemgoaoonhnj"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UrlRequest(BaseModel):
    url: str


@app.post("/process-url")
async def process_url(request: UrlRequest):
    url = request.url
    summarized_text = generate_summary(url)
    return {"summary": summarized_text}

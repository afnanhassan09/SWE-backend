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


if __name__ == "__main__":
    port = int(
        os.getenv("PORT", 8000)
    )  # Use PORT environment variable or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)

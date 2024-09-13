import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from summarizer import generate_summary
from fastapi import HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()
scheduler.start()


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
        summarized_text = {"Topic": str(e)}
        raise HTTPException(status_code=500, detail=str(e))

    return summarized_text


def scheduled_job():
    url = "https://swe-backend-bk7f.onrender.com/" 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Successfull call")
        else:
            print(f"Failed to fetch URL. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")


scheduler.add_job(scheduled_job, "interval", minutes=1)


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

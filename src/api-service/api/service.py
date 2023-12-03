from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import asyncio
# from api.tracker import TrackerService
import pandas as pd
import os
from io import BytesIO
from fastapi import File
from tempfile import TemporaryDirectory
from api import model
from typing import Annotated
from fastapi import FastAPI, Query, UploadFile
from fastapi.responses import StreamingResponse
from google.cloud import storage

# Setup FastAPI app
app = FastAPI(title="API Server", description="API Server", version="v1")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print("Startup tasks")

# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome to the API Service"}

@app.get("/predict/")
async def predict(word1: str = None, word2: str = None):
    instance = [{"sample_key": [word1, word2]}]
    folder_name = model.make_prediction_vertexai(instance)
    storage_client = storage.Client()
    bucket = storage_client.bucket("saved_predictions")
    gif_blob = bucket.blob(f"{folder_name}/test.gif")
    gif_bytes = gif_blob.download_as_bytes()

    return StreamingResponse(iter([gif_bytes]), media_type='image/gif')

@app.get("/status")
async def get_api_status():
    return {
        "version": "2.1",
        # "tf_version": tf.__version__,
    }
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



# Initialize Tracker Service
# tracker_service = TrackerService()

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
    # Start the tracker service
    # asyncio.create_task(tracker_service.track())

# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome to the API Service"}


# @app.post("/predict")
# async def predict(instance: list):
#     print("predict instance:", instance)
#     model.make_prediction_vertexai(instance)

#     return "checkbuckets"

@app.get("/predict/")
async def predict(word1: str = None, word2: str = None):
    instance = [{"sample_key": [word1, word2]}]
    folder_name = model.make_prediction_vertexai(instance)
    storage_client = storage.Client()
    bucket = storage_client.bucket("saved_predictions")
    gif_blob = bucket.blob(f"{folder_name}/test.gif")
    gif_bytes = gif_blob.download_as_bytes()

    return StreamingResponse(iter([gif_bytes]), media_type='image/gif')

# @app.get('/get_gif/{folder_name}', status_code=200)
# async def upload_file(folder_name: str):
#     #get gif from buckets 
#     storage_client = storage.Client()
#     bucket = storage_client.bucket("saved_predictions")
#     gif_blob = bucket.blob(folder_name + "/test.gif")
#     gif_bytes = gif_blob.download_as_bytes()

#     return StreamingResponse(gif_bytes, media_type='image/gif')

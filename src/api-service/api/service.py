from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import asyncio
# from api.tracker import TrackerService
import pandas as pd
import os
from fastapi import File
from tempfile import TemporaryDirectory
from api import model
from typing import Annotated
from fastapi import FastAPI, Query



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

@app.post("/predict/")
async def predict(word1: str = None, word2: str = None):
    instance = [{"sample_key": [word1, word2]}]
    #model.make_prediction_vertexai(instance)
    return instance 


# @app.post("/predict/")
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
#     query_items = {"q": q}
#     return query_items
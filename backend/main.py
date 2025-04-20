import json

from fastapi import FastAPI
from pydantic import BaseModel

from backend.model import Recommender

app = FastAPI()

class Query(BaseModel):
    query: str

# Load assessment data
with open("backend/data/assessments.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

# Load model
recommender = Recommender(assessments)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(data: Query):
    return recommender.recommend(data.query, top_k=10)

@app.get("/")
def home():
    return {"message": "SHL Gen AI API is live. Use `/health` and `/recommend`."}

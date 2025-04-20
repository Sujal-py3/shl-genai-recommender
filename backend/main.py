import json

from fastapi import FastAPI
from model import Recommender
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

# Load data
with open("data/assessments.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

# Load recommender
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

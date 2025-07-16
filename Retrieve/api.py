from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import joblib

from retriever import hybrid_retrieve_issue  # Ensure this function is defined in retriever.py

# Initialize FastAPI
app = FastAPI(title="Hybrid Issue Retriever API")

# Load pre-trained models
tfidf = joblib.load('tfidf_vectorizer.pkl')
embedding_model = SentenceTransformer('embedding_model')

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
collection = client["hybrid_retriever"]["issues"]

# Request schema for querying
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3
    alpha: float = 0.6

# POST endpoint
@app.post("/retrieve")
def retrieve_issues(request: QueryRequest):
    try:
        results = hybrid_retrieve_issue(
            request.query,
            tfidf,
            embedding_model,
            collection,
            top_k=request.top_k,
            alpha=request.alpha
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

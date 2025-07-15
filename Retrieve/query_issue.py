import joblib
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from retriever import hybrid_retrieve_issue

# Load vectorizer and model
tfidf = joblib.load('tfidf_vectorizer.pkl')
embedding_model = SentenceTransformer('embedding_model')

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["hybrid_retriever"]["issues"]

# Input your issue query here
query = "application crashes due to missing config value"

# Retrieve top results
results = hybrid_retrieve_issue(query, tfidf, embedding_model, collection)

# Display
for i, res in enumerate(results):
    print(f"\n Result {i+1} (Score: {res['score']:.4f})")
    print(" Summary:", res['summary'])
    print(" Root Cause:", res['root_cause'])
    print(" Fix:", res['data_fix'])
    print(" Description:", res['detailed_description'])
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import numpy as np
import joblib

def ingest_data(file_path):
    # Load Excel
    df = pd.read_excel(file_path)
    columns = ["Summary", "Detailed Description", "Root Cause", "Data Fix Provided"]
    
    # Keep only rows where Root Cause is not null
    df = df[df["Root Cause"].notnull()].copy()
    
    # Reset index to align with TF-IDF and embeddings index
    df = df.reset_index(drop=True)

    # Replace NaN in other fields with empty strings
    df[columns] = df[columns].fillna("")

    # Concatenate all fields into one full text for vectorization
    df['full_text'] = df[columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

    # TF-IDF Vectorizer
    tfidf = TfidfVectorizer(max_features=1000)
    tfidf_matrix = tfidf.fit_transform(df['full_text'])

    # Sentence Embedding Model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['full_text'].tolist(), show_progress_bar=True)

    # Save vectorizer and model locally
    joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
    model.save('embedding_model')

    # MongoDB Setup
    client = MongoClient("mongodb://localhost:27017/")
    db = client["hybrid_retriever"]
    collection = db["issues"]
    collection.drop()

    # Prepare documents
    records = []
    for idx, row in df.iterrows():
        record = {
            "summary": row["Summary"],
            "detailed_description": row["Detailed Description"],
            "root_cause": row["Root Cause"],
            "data_fix": row["Data Fix Provided"],
            "tfidf_vector": tfidf_matrix[idx].toarray().flatten().tolist(),
            "embedding_vector": embeddings[idx].tolist()
        }
        records.append(record)

    # Insert into MongoDB
    collection.insert_many(records)
    print(f" Inserted {len(records)} issues into MongoDB.")

if __name__ == "__main__":
    ingest_data("ultra_refined_descriptions.xlsx")

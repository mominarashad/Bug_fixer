from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def hybrid_retrieve_issue(query, tfidf, embedding_model, collection, top_k=3, alpha=0.6):
    query_tfidf = tfidf.transform([query]).toarray()
    query_embedding = embedding_model.encode([query])[0].reshape(1, -1)

    docs = list(collection.find({}))
    tfidf_matrix = np.array([doc['tfidf_vector'] for doc in docs])
    embedding_matrix = np.array([doc['embedding_vector'] for doc in docs])

    tfidf_sims = cosine_similarity(query_tfidf, tfidf_matrix)[0]
    emb_sims = cosine_similarity(query_embedding, embedding_matrix)[0]
    combined_sims = alpha * emb_sims + (1 - alpha) * tfidf_sims

    top_indices = combined_sims.argsort()[::-1][:top_k]
    top_docs = [docs[i] for i in top_indices]

    for i, doc in enumerate(top_docs):
        doc['score'] = float(combined_sims[top_indices[i]])

    return top_docs
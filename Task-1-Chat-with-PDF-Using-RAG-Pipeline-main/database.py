import faiss
import numpy as np

def create_faiss_index(embeddings):
    # Create a FAISS index with embeddings (assuming 384-dimensional vectors)
    d = embeddings.shape[1]  # Dimension of the embedding vectors
    index = faiss.IndexFlatL2(d)  # L2 distance index
    index.add(embeddings)  # Add the embeddings to the index
    return index

def query_faiss_index(index, query_embedding, k=5):
    # Perform the query on the FAISS index
    distances, indices = index.search(query_embedding, k)  # Search for k nearest neighbors
    return indices, distances

def update_faiss_index(index, new_embeddings, new_text_chunks):
    # Append the new embeddings to the existing index
    index.add(np.array(new_embeddings))  # Add the new embeddings to the index
    return index

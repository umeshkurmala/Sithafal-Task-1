from sentence_transformers import SentenceTransformer

# Load a pre-trained sentence-transformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(text_list):
    """Generate embeddings for a list of texts."""
    embeddings = model.encode(text_list)
    return embeddings

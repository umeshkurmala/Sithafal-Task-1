import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import pdfplumber
import faiss

app = Flask(__name__)

# Configuration
pdf_folder = r"D:\pdf-folder"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
text_chunks = []


import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extract and clean text from a PDF file."""
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text from the page
                page_text = page.extract_text()
                
                # Clean and refine the extracted text
                if page_text:
                    # Split the page text into lines
                    lines = page_text.split("\n")
                    
                    # Remove any unnecessary whitespace and empty lines
                    cleaned_lines = [line.strip() for line in lines if line.strip()]
                    
                    # Join cleaned lines back together with appropriate line breaks
                    extracted_text += "\n".join(cleaned_lines) + "\n\n"
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {e}")
    return extracted_text



def generate_embeddings(text_list):
    """Generate vector embeddings for a list of texts."""
    return embedding_model.encode(text_list, convert_to_numpy=True)


def create_faiss_index(embeddings):
    """Create and return a FAISS index from embeddings."""
    d = embeddings.shape[1]  # Dimension of embeddings
    index = faiss.IndexFlatL2(d)  # L2 distance metric
    index.add(embeddings)
    return index


def query_faiss_index(index, query_embedding, top_k=5):
    """Query the FAISS index and return top-k results."""
    distances, indices = index.search(query_embedding, top_k)
    return indices, distances


def load_pdfs():
    """Load and process PDFs to create the FAISS index."""
    global index, text_chunks

    all_text_chunks = []
    all_embeddings = []

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            extracted_text = extract_text_from_pdf(pdf_path)
            chunks = extracted_text.split("\n")

            # Skip empty chunks
            chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
            all_text_chunks.extend(chunks)

            # Generate embeddings for each chunk
            embeddings = generate_embeddings(chunks)
            all_embeddings.append(embeddings)

    # Combine all embeddings and build the FAISS index
    all_embeddings = np.vstack(all_embeddings)
    index = create_faiss_index(all_embeddings)
    text_chunks = all_text_chunks


def generate_response(query):
    """Generate a structured response for the user's query."""
    query_embedding = generate_embeddings([query])
    indices, distances = query_faiss_index(index, query_embedding)

    # Fetch top relevant chunks
    relevant_chunks = [text_chunks[i] for i in indices[0]]

    # Organize the response
    organized_response = ""
    for chunk in relevant_chunks:
        lines = chunk.split("\n")
        for line in lines:
            if ":" in line:
                organized_response += f"<p><b>{line.split(':')[0]}</b>: {line.split(':')[1].strip()}</p>"
            else:
                organized_response += f"<p>{line.strip()}</p>"
        organized_response += "<hr>"

    return organized_response



def handle_comparison_query(query):
    """Handle comparison queries."""
    query_embedding = generate_embeddings([query])
    indices, distances = query_faiss_index(index, query_embedding)

    # Fetch relevant chunks
    relevant_chunks = [text_chunks[i] for i in indices[0]]

    # Extract and compare terms/fields
    # (For simplicity, we'll just return the retrieved chunks for now)
    comparison_response = "Comparison Query Results:\n" + "\n".join(relevant_chunks)
    return comparison_response


# Load PDFs and build the FAISS index
load_pdfs()

@app.route("/")
def home():
    return render_template("index.html")


def clean_response(response_text):
    # Remove any repeated characters or noise
    import re
    response_text = re.sub(r'([a-zA-Z])\1+', r'\1', response_text)  # Remove duplicate letters
    response_text = response_text.replace("\n", " ").strip()  # Replace newlines with spaces
    return response_text

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form.get('query')
    # Process query and get response
    response = generate_response(query)  # Your existing response logic
    clean_resp = clean_response(response)
    return jsonify({'response': clean_resp})


@app.route("/update_index", methods=["POST"])
def update_index():
    try:
        new_pdf = request.files["new_pdf"]
        pdf_path = os.path.join(pdf_folder, new_pdf.filename)
        new_pdf.save(pdf_path)

        # Process the new PDF
        extracted_text = extract_text_from_pdf(pdf_path)
        new_chunks = extracted_text.split("\n")
        new_chunks = [chunk.strip() for chunk in new_chunks if chunk.strip()]
        new_embeddings = generate_embeddings(new_chunks)

        # Update the FAISS index
        global index, text_chunks
        text_chunks.extend(new_chunks)
        index.add(new_embeddings)

        return jsonify({"message": "Index updated successfully!"})
    except Exception as e:
        return jsonify({"error": f"Error updating index: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
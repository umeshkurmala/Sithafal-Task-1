# Sithafal-Task-1
Chat with PDF using RAG Pipeline
Overview
This project implements a Retrieval-Augmented Generation (RAG) pipeline to allow users to interact with semi-structured data from PDF files. The system extracts, chunks, embeds, and stores data for efficient retrieval. It answers user queries and performs comparisons using custom logic and embeddings without relying on external LLMs.

Functional Features
1. Data Ingestion
Input: PDF files containing semi-structured data.
Process:
Extract text and structured data from PDFs.
Split data into logical chunks.
Convert text chunks into vector embeddings using Sentence Transformers.
Store embeddings in a vector database (e.g., FAISS).
2. Query Handling
Input: Natural language queries from users.
Process:
Convert user queries into vector embeddings.
Perform a similarity search in the vector database.
Fetch relevant data chunks for further processing.
3. Comparison Queries
Input: Queries requesting comparisons.
Process:
Identify fields or terms to compare.
Retrieve corresponding chunks from the vector database.
Aggregate and structure data for comparisons (e.g., in tables).
4. Response Generation
Input: Retrieved data chunks and user query.
Process:
Use custom logic to generate factual responses.
Ensure responses are structured and contextually accurate.
How It Works
Step 1: Upload PDFs
Upload the PDFs through the web interface for processing.

Step 2: Ask Queries
Ask natural language questions to retrieve relevant answers.

Step 3: Comparison Queries
Use queries like Compare the official languages of Andhra Pradesh and Assam to get comparative outputs.

Step 4: Access the Application
Run the backend server and access the application at http://localhost:5000.

Directory Structure
plaintext
Copy code
Chat-With-PDF-RAG/
│
├── data/                # Directory for PDF uploads
├── embeddings/          # Storage for vector embeddings
├── app.py               # Main backend application (Flask/FastAPI)
├── queryHandler.js      # Frontend logic for handling queries
├── templates/           # Frontend UI files
│   └── index.html       # HTML UI for user interaction
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
API Endpoints
Endpoint	Method	Description
/upload	POST	Uploads and processes a PDF file.
/ask	POST	Handles user queries and retrieves data.
/compare	POST	Processes comparison-related queries.
Example Queries
Simple Query
Input:

plaintext
Copy code
What is the capital of Andhra Pradesh?
Response:

json
Copy code
{
  "State": "Andhra Pradesh",
  "Capital": "Amaravati"
}
Comparison Query
Input:

plaintext
Copy code
Compare the official languages of Andhra Pradesh and Assam.
Response:

State	Official Language	Additional Language
Andhra Pradesh	Telugu	Urdu
Assam	Assamese	None
Technology Stack
Component	Tool/Library
Backend	Python, Flask/FastAPI
PDF Processing	PyPDF2, pdfminer.six
Text Embeddings	Sentence Transformers
Vector Database	FAISS
Frontend	HTML, CSS, JavaScript
Response Generation	Custom logic or locally hosted models
Future Enhancements
Planned Feature	Description
Parallel PDF Processing	Support large-scale PDFs with faster performance.
Advanced Comparison Visuals	Add charts and graphs for better visual comparisons.
Multilingual Support	Handle PDFs and queries in multiple languages.
Hybrid Search Optimization	Combine keyword-based and vector-based retrieval.
Setup Instructions
Clone the Repository

bash
Copy code
git clone https://github.com/your-username/Chat-With-PDF-RAG.git
cd Chat-With-PDF-RAG
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Run the Backend

bash
Copy code
python app.py
Access the Application Open http://localhost:5000 in your browser.

Contributing
Contributions are welcome! Follow these steps to contribute:

Fork the repository.
Create a new branch:
bash
Copy code
git checkout -b feature-branch
Commit your changes:
bash
Copy code
git commit -m "Add new feature"
Push to your branch and submit a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Tool/Library	Purpose
Hugging Face	Pre-trained embeddings (Sentence Transformers).
FAISS	Vector search capabilities.
PyPDF2 / pdfminer.six	PDF text extraction.

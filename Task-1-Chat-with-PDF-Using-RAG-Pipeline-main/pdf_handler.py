import pdfplumber

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            extracted_text = ''
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
        return extracted_text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {e}")

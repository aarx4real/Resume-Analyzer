import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path: str) -> str:
    """
    Given a path to a PDF, opens it and returns the full text content.
    Includes validation for file type and content extraction success.
    """
    # 1. Check if the file actually exists
    if not os.path.exists(file_path):
        return "Error: File not found on server."

    # 2. Validate file extension
    if not file_path.lower().endswith('.pdf'):
        return "Error: The uploaded file is not a PDF."

    try:
        # 3. Open the document
        doc = fitz.open(file_path)
        text = ""
        
        # 4. Iterate through pages and extract text
        for page in doc:
            text += page.get_text()
        
        # 5. Handle cases where PDF might be an image/scan (no selectable text)
        if not text.strip():
            return "Error: No text detected. This PDF might be an image or a scan."

        # 6. Basic cleaning: collapse multiple spaces/newlines into single spaces
        clean_text = " ".join(text.split())
        
        return clean_text

    except Exception as e:
        # Professional projects always catch and log the specific error
        return f"Error processing PDF: {str(e)}"

# This allows you to test this file individually if you run it directly
if __name__ == "__main__":
    print("Extractor Module Loaded Successfully.")
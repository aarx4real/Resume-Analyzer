import pymupdf
import os

def extract_text_from_pdf(file_input) -> str:
    """
    Given a file path or file bytes of a PDF, returns the full text content.
    """
    try:
        if isinstance(file_input, (bytes, bytearray)):
            doc = pymupdf.open(stream=file_input, filetype="pdf")
        elif isinstance(file_input, str):
            if not os.path.exists(file_input):
                return "Error: File not found on server."
            if not file_input.lower().endswith('.pdf'):
                return "Error: The uploaded file is not a PDF."
            doc = pymupdf.open(file_input)
        else:
            return "Error: Invalid file format."

        text = ""
        for page in doc:
            text += page.get_text() + "\n"

        if not text.strip():
            return "Error: No text detected. This PDF might be an image or a scan."

        return " ".join(text.split())

    except Exception as e:
        return f"Error processing PDF: {str(e)}"

# This allows you to test this file individually if you run it directly
if __name__ == "__main__":
    print("Extractor Module Loaded Successfully.")
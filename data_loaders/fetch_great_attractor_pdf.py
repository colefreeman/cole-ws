import requests
from io import BytesIO
import PyPDF2
from datetime import datetime

@data_loader
def load_pdf_from_github(**kwargs):

    # Load PDF from GitHub repository
    github_pdf_url = "https://raw.githubusercontent.com/mage-ai/datasets/master/great_attractor_pdf.pdf"
    
    print(f"Fetching PDF from GitHub: {github_pdf_url}")
    
    # Download the PDF
    try:
        response = requests.get(github_pdf_url)
        response.raise_for_status()  # Ensure we got a valid response
        
        # Read the PDF content
        pdf_content = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        
        # Extract metadata
        pdf_info = {
            "title": "Evidence of the Great Attractor and Great Repeller",
            "author": "Christopher C. O'Neill",
            "num_pages": len(pdf_reader.pages),
            "source_url": github_pdf_url,
            "fetch_time": datetime.now().isoformat()
        }
        
        # Extract text from all pages
        all_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            all_text += page_text + "\n\n"
        
        print(f"Successfully extracted {pdf_info['num_pages']} pages from PDF")
        
        # Create result with both metadata and content
        result = {
            "metadata": pdf_info,
            "content": all_text
        }
        return result
    except Exception as e:
        print(f"Error fetching PDF from GitHub: {e}")
        # Instead of providing sample text, let's throw an error to ensure we don't proceed without the actual document
        raise Exception(f"Failed to load PDF document: {e}")
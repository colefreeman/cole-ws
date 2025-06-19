import re

@transformer
def clean_document(data, **kwargs):
    """
    Clean and format the extracted PDF text
    """
    # Check if data is available
    if data is None or "content" not in data:
        raise Exception("No PDF content available to clean")
    
    # Extract text and metadata from previous block
    text = data["content"]
    metadata = data["metadata"]
    
    print("Cleaning document text...")
    
    # Clean up common PDF extraction issues
    # 1. Replace multiple newlines with a single newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 2. Fix broken words that might have been split across lines
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    
    # 3. Remove headers and footers that repeat on each page
    text = re.sub(r'Journal of High Energy Physics,\s+Gravitation and Cosmology.+?\d+', '', text)
    text = re.sub(r'DOI:.+?\d+', '', text)
    
    # 4. Normalize whitespace
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()
    
    # Add document information at the beginning
    title_header = f"# {metadata['title']}\n"
    author_header = f"## By {metadata['author']}\n"
    source_header = f"Source: {metadata['source_url']}\n\n"
    
    formatted_text = title_header + author_header + source_header + text
    
    # Return cleaned document with metadata
    result = {
        "text": formatted_text,
        "metadata": metadata,
        "character_count": len(formatted_text),
        "processing_time": kwargs.get("execution_date", "Unknown")
    }
    
    print(f"Document cleaned: {len(formatted_text)} characters")
    return result
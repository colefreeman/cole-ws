@transformer
def chunk_document(data, **kwargs):
    """
    Split the cleaned document into manageable chunks with overlap
    """
    # Check if data is available
    if data is None or "text" not in data:
        raise Exception("No cleaned document text available to chunk")

    text = data["text"]
    metadata = data["metadata"]
    
    print("Chunking document with fixed size approach...")
    
    # Set chunking parameters
    chunk_size = 4000  # characters per chunk
    overlap = 500      # overlap between chunks to maintain context
    
    # Calculate how many chunks we'll need
    doc_length = len(text)
    estimated_chunks = (doc_length // (chunk_size - overlap)) + 1
    print(f"Document length: {doc_length} characters")
    print(f"Will create approximately {estimated_chunks} chunks")
    
    # Create chunks with simple fixed-size approach
    chunks = []
    
    # Special case: if text is smaller than chunk_size, just use one chunk
    if doc_length <= chunk_size:
        chunks.append({
            "chunk_id": 0,
            "text": text,
            "start_char": 0,
            "end_char": doc_length,
            "character_count": doc_length,
            "doc_id": metadata['source_url']
        })
    else:
        # Use a straightforward loop with explicit indices
        chunk_id = 0
        for i in range(0, doc_length, chunk_size - overlap):
            # Calculate chunk boundaries
            start = i
            end = min(i + chunk_size, doc_length)
            
            # Don't create tiny chunks at the end
            if end - start < 200 and chunk_id > 0:
                break
                
            # Extract chunk text
            chunk_text = text[start:end]
            
            # Create chunk with metadata
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "start_char": start,
                "end_char": end,
                "character_count": len(chunk_text),
                "doc_id": metadata['source_url']
            })
            
            chunk_id += 1
            
            # Log progress for larger documents
            if chunk_id % 5 == 0:
                print(f"Created {chunk_id} chunks so far...")
    
    # Create result
    result = {
        "chunks": chunks,
        "chunk_count": len(chunks),
        "total_characters": doc_length,
        "metadata": metadata
    }
    
    print(f"Document processed into {len(chunks)} chunks")
    return result
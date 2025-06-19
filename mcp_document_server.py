#!/usr/bin/env python3
import asyncio
import json
import os
import sys

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
    )
    print("All imports successful", file=sys.stderr)
except ImportError as e:
    print(f"Import error: {e}", file=sys.stderr)
    sys.exit(1)

# Initialize the MCP server
server = Server("simple-document-server")
DOCUMENT_CHUNKS = []

@server.list_resources()
async def handle_list_resources():
    """List available document resources"""
    print(f"Listing {len(DOCUMENT_CHUNKS)} resources", file=sys.stderr)
    resources = []
    for chunk in DOCUMENT_CHUNKS:
        resources.append(
            Resource(
                uri=f"document://great_attractor/chunk_{chunk['chunk_id']}",
                name=f"Document Chunk {chunk['chunk_id']}",
                description=f"Section {chunk['chunk_id']} of the Great Attractor research paper",
                mimeType="text/plain"
            )
        )
    return resources

@server.read_resource()
async def handle_read_resource(uri: str):
    """Read content from a specific document resource"""
    # Convert URI to string if it's a Pydantic URL object
    uri_str = str(uri)
    print(f"Reading resource: {uri_str}", file=sys.stderr)
    
    if uri_str.startswith("document://great_attractor/chunk_"):
        try:
            chunk_id = int(uri_str.split("_")[-1])
            print(f"Looking for chunk_id: {chunk_id}", file=sys.stderr)
            
            # Ensure we have the right data structure
            chunks_to_search = DOCUMENT_CHUNKS
            if isinstance(DOCUMENT_CHUNKS, dict) and 'chunks' in DOCUMENT_CHUNKS:
                chunks_to_search = DOCUMENT_CHUNKS['chunks']
            
            for chunk in chunks_to_search:
                if chunk.get("chunk_id") == chunk_id:
                    content = chunk.get("text", "")
                    print(f"Found chunk {chunk_id}, returning {len(content)} characters", file=sys.stderr)
                    return content
            
            print(f"Chunk {chunk_id} not found in {len(chunks_to_search)} available chunks", file=sys.stderr)
            raise ValueError(f"Chunk {chunk_id} not found")
            
        except (ValueError, IndexError) as e:
            print(f"Error parsing chunk_id from {uri_str}: {e}", file=sys.stderr)
            raise ValueError(f"Invalid chunk URI: {uri_str}")
    
    raise ValueError(f"Resource not found: {uri_str}")

@server.list_tools()
async def handle_list_tools():
    """List available tools"""
    return [
        Tool(
            name="search_document",
            description="Search for relevant document chunks",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 3}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """Handle tool calls"""
    print(f"Tool called: {name} with args: {arguments}", file=sys.stderr)
    print(f"Available chunks: {len(DOCUMENT_CHUNKS)}", file=sys.stderr)
    
    if name == "search_document":
        query = arguments.get("query", "")
        max_results = arguments.get("max_results", 3)
        
        print(f"Searching for: {query} with max_results: {max_results}", file=sys.stderr)
        print(f"DOCUMENT_CHUNKS contains: {len(DOCUMENT_CHUNKS)} chunks", file=sys.stderr)
        
        try:
            # Ensure DOCUMENT_CHUNKS is a list
            chunks_to_search = DOCUMENT_CHUNKS
            if isinstance(DOCUMENT_CHUNKS, dict):
                if 'chunks' in DOCUMENT_CHUNKS:
                    chunks_to_search = DOCUMENT_CHUNKS['chunks']
                else:
                    # Convert dict values to list if it's a dict of chunks
                    chunks_to_search = list(DOCUMENT_CHUNKS.values())
            
            if not chunks_to_search:
                print("WARNING: No document chunks available for search!", file=sys.stderr)
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "chunk_ids": [],
                        "total_matches": 0,
                        "error": "No document chunks loaded"
                    })
                )]
            
            print(f"Searching through {len(chunks_to_search)} chunks", file=sys.stderr)
            
            # Simple search - return first few chunks that exist
            chunk_ids = []
            for i, chunk in enumerate(chunks_to_search):
                if i >= max_results:
                    break
                chunk_id = chunk.get("chunk_id", i) if isinstance(chunk, dict) else i
                chunk_ids.append(chunk_id)
            
            result = {
                "chunk_ids": chunk_ids,
                "total_matches": len(chunks_to_search),
                "query": query,
                "debug_chunks_type": str(type(chunks_to_search))
            }
            
            print(f"Search result: {result}", file=sys.stderr)
            
            return [TextContent(
                type="text",
                text=json.dumps(result)
            )]
            
        except Exception as e:
            print(f"Search error: {e}", file=sys.stderr)
            import traceback
            print(f"Full traceback: {traceback.format_exc()}", file=sys.stderr)
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e), "query": query})
            )]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    print("Starting MCP server", file=sys.stderr)
    
    # Load document chunks from environment variable
    chunks_env = os.getenv("DOCUMENT_CHUNKS")
    global DOCUMENT_CHUNKS
    
    if chunks_env:
        try:
            DOCUMENT_CHUNKS = json.loads(chunks_env)
            print(f"Loaded {len(DOCUMENT_CHUNKS)} chunks from environment", file=sys.stderr)
            
            # Debug: print first chunk info
            if DOCUMENT_CHUNKS:
                print(f"DOCUMENT_CHUNKS type: {type(DOCUMENT_CHUNKS)}", file=sys.stderr)
                
                if isinstance(DOCUMENT_CHUNKS, list):
                    first_chunk = DOCUMENT_CHUNKS[0]
                    print(f"First chunk keys: {list(first_chunk.keys())}", file=sys.stderr)
                    print(f"First chunk ID: {first_chunk.get('chunk_id', 'NO_ID')}", file=sys.stderr)
                    print(f"First chunk text preview: {first_chunk.get('text', 'NO_TEXT')[:100]}...", file=sys.stderr)
                elif isinstance(DOCUMENT_CHUNKS, dict):
                    print(f"DOCUMENT_CHUNKS is a dict with keys: {list(DOCUMENT_CHUNKS.keys())}", file=sys.stderr)
                    # Convert dict to list if needed
                    if 'chunks' in DOCUMENT_CHUNKS:
                        DOCUMENT_CHUNKS = DOCUMENT_CHUNKS['chunks']
                        print(f"Extracted chunks list with {len(DOCUMENT_CHUNKS)} items", file=sys.stderr)
                    else:
                        print("DOCUMENT_CHUNKS is a dict but no 'chunks' key found", file=sys.stderr)
                else:
                    print(f"DOCUMENT_CHUNKS is unexpected type: {type(DOCUMENT_CHUNKS)}", file=sys.stderr)
            else:
                print("DOCUMENT_CHUNKS is empty", file=sys.stderr)
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse DOCUMENT_CHUNKS: {e}", file=sys.stderr)
            print(f"Raw DOCUMENT_CHUNKS: {chunks_env[:200]}...", file=sys.stderr)
            sys.exit(1)
    else:
        print("No DOCUMENT_CHUNKS environment variable found", file=sys.stderr)
        print("Available env vars:", [k for k in os.environ.keys() if 'CHUNK' in k.upper()], file=sys.stderr)
    
    # Run the server
    try:
        print("Creating stdio server streams", file=sys.stderr)
        async with stdio_server() as (read_stream, write_stream):
            print("Server streams created, running server", file=sys.stderr)
            
            # Create server capabilities
            capabilities = server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            )
            print(f"Server capabilities created: {type(capabilities)}", file=sys.stderr)
            
            # Initialize and run server
            init_options = InitializationOptions(
                server_name="simple-document-server",
                server_version="1.0.0",
                capabilities=capabilities,
            )
            print("Starting server.run()", file=sys.stderr)
            
            await server.run(read_stream, write_stream, init_options)
            print("Server.run() completed", file=sys.stderr)
            
    except EOFError:
        print("Server received EOF (stdin closed) - this is normal for testing", file=sys.stderr)
    except KeyboardInterrupt:
        print("Server interrupted by user", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        print(f"Error type: {type(e)}", file=sys.stderr)
        import traceback
        print(f"Full traceback: {traceback.format_exc()}", file=sys.stderr)
        raise

if __name__ == "__main__":
    try:
        print("Starting asyncio main loop", file=sys.stderr)
        asyncio.run(main())
        print("Main loop completed normally", file=sys.stderr)
    except KeyboardInterrupt:
        print("Server interrupted by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        print(f"Error type: {type(e)}", file=sys.stderr)
        import traceback
        print(f"Full traceback: {traceback.format_exc()}", file=sys.stderr)
        sys.exit(1)
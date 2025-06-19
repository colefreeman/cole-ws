from mage_ai.data_preparation.shared.secrets import get_secret_value
import pandas as pd
import json
import asyncio
import nest_asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
import anthropic

nest_asyncio.apply()

@transformer
def interact_with_anthropic_via_mcp(data, **kwargs):
    api_key = get_secret_value('CLAUDE_API_KEY')
    
    if not api_key or not data or "chunks" not in data:
        return pd.DataFrame({
            "error": ["Missing API key or chunks"],
            "question": ["Unknown"],
            "answer": ["Cannot process request"],
            "source": ["Error"]
        })
    
    chunks = data["chunks"]
    query = kwargs.get('variables', {}).get('user_question', "What is the Great Attractor?")
    
    async def run_real_mcp():
        # Configure MCP server
        server_params = StdioServerParameters(
            command="python",
            args=["/home/src/cole-ws/mcp_document_server.py"],  # Your actual MCP server
            env={"DOCUMENT_CHUNKS": json.dumps(chunks)}
        )
        
        # Connect to MCP server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Use MCP tools
                search_result = await session.call_tool(
                    "search_document",
                    arguments={"query": query, "max_results": 3}
                )
                
                # Parse results
                tool_content = search_result.content[0].text
                search_data = json.loads(tool_content)
                chunk_ids = search_data["chunk_ids"]
                
                # Read MCP resources
                context_parts = []
                for chunk_id in chunk_ids:
                    resource_uri = f"document://great_attractor/chunk_{chunk_id}"
                    resource = await session.read_resource(resource_uri)
                    context_parts.append(resource.contents[0].text)
                
                return "\n\n---\n\n".join(context_parts)
    
    try:
        context = asyncio.run(run_real_mcp())
        
        # Query Claude with MCP context
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.2,
            system="Answer based only on the provided context.",
            messages=[{
                "role": "user",
                "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{query}"
            }]
        )
        
        return pd.DataFrame({
            "question": [query],
            "answer": [response.content[0].text],
            "source": ["Real MCP Implementation"],
            "mcp_implementation": ["Full MCP protocol with server"]
        })
        
    except Exception as e:
        return pd.DataFrame({
            "error": [str(e)],
            "question": [query],
            "answer": ["MCP processing failed"],
            "source": ["MCP Error"]
        })
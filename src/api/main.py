"""FastAPI backend for AI Assistant."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
from sse_starlette.sse import EventSourceResponse
from src.ai_assistant.core.assistant import get_assistant

# Initialize the assistant
assistant = get_assistant()
assistant._print_welcome = False  # Disable welcome message for API mode

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    # Startup: Initialize the assistant
    await assistant._setup_agent()
    yield
    # Shutdown: Clean up resources
    await assistant.cleanup()

app = FastAPI(
    title="AI Assistant API",
    description="API endpoints for AI Assistant functionality",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AssistantRequest(BaseModel):
    prompt: str
    stream: bool = False

class AssistantResponse(BaseModel):
    response: str

async def stream_response(prompt: str):
    """Stream the assistant's response."""
    if not hasattr(assistant, "agent"):
        await assistant._setup_agent()

    # Add markdown formatting instructions to the prompt
    formatted_prompt = f"""
Please provide your response using proper markdown formatting:
- Use `code` for inline code
- Use ```language\ncode\n``` for code blocks
- Use **bold** for emphasis
- Use - or * for bullet points
- Use 1. 2. etc for numbered lists
- Use > for quotes
- Use ### for subheadings
- Use tables when presenting structured data
- Use [text](url) for links
- Use `diagrams` directory to generate AWS architecture diagrams

Here's the user's question:
{prompt}
"""
    
    # Create HumanMessage with formatted prompt
    messages = [{"role": "user", "content": formatted_prompt}]
    
    async for step in assistant.agent.astream(
        {"messages": messages},
        stream_mode="values",
    ):
        if "messages" in step and step["messages"]:
            last_message = step["messages"][-1]
            # Check if it's an assistant message by checking content
            if last_message.content and last_message.content != formatted_prompt:
                yield {
                    "event": "message",
                    "data": json.dumps({"content": last_message.content})
                }

@app.post("/assistant")
async def process_assistant_request(request: AssistantRequest):
    """Process an AI assistant request."""
    try:
        if request.stream:
            return EventSourceResponse(
                stream_response(request.prompt),
                media_type="text/event-stream"
            )
        
        # Non-streaming response
        response = await assistant.process_input(request.prompt)
        return AssistantResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

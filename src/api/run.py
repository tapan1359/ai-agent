"""Run script for FastAPI server."""
import uvicorn

def run_api():
    """Run the FastAPI server."""
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    run_api()

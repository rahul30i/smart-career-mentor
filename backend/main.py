from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import mentor
import os

app = FastAPI(title="Smart Career Mentor API")

# CORS Setup
origins = [
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CareerRequest(BaseModel):
    role: str

@app.get("/")
def read_root():
    return {"message": "Smart Career Mentor API is running"}

@app.post("/api/generate-guide")
def generate_guide(request: CareerRequest):
    """
    Generates a detailed career guide for the given role.
    Currently uses a sophisticated mock response to demonstrate the UI.
    """
    try:
        # In a real scenario, this would call OpenAI
        # api_key = os.getenv("OPENAI_API_KEY")
        # if api_key:
        #     return mentor.generate_with_llm(request.role, api_key)
        
        # Default to high-quality mock data for demo purposes
        data = mentor.get_mock_data(request.role)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.models.medical_kb import MedicalKnowledgeBase
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Virtual Nursing Assistant")

# Get the absolute path to the app directory
app_dir = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(app_dir, "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(app_dir, "templates"))

# Initialize medical knowledge base
medical_kb = MedicalKnowledgeBase()

class UserInput(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/process")
async def process_message(user_input: UserInput):
    try:
        # Validate input
        if not user_input.message or not user_input.message.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Please provide a message to analyze"}
            )
        
        # Log the incoming message
        logger.info(f"Processing message: {user_input.message}")
        
        # Process the message using medical knowledge base
        response = medical_kb.get_response(user_input.message.strip())
        
        # Log the response
        logger.info(f"Generated response for message")
        
        return {"response": response}
    
    except Exception as e:
        # Log the error
        logger.error(f"Error processing message: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "I encountered an error analyzing your symptoms. Please try again."}
        )

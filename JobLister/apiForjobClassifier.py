from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
from jobClassifier import send_message_to_model

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing; adjust this for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/api/greet")
def greet(req: str):
    # Call the function with the request parameter as-is
    response = send_message_to_model(req)
    
    # Clean up the response
    clean_response = response.replace("\\n", "").replace('\\"', '"')
    json_data = json.loads(clean_response)
    
    # Return the JSON data
    return json_data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

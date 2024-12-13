from fastapi import FastAPI, File, Form, UploadFile
import os
import sys
from ..utils.unzip_music import unzipMusic 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
app = FastAPI()

# Directory where audio and image folders will be created
BASE_DIR = os.path.join(os.getcwd(), "backend")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/upload-database-audio/")
async def handle_database_audio(
    file: UploadFile = File(...), folder_name: str = Form(...)
):
    # Create a folder for audio files
    zip_file_path = os.path.join(BASE_DIR, "src/backend/database_music/uploaded_files", file.filename)
    print(zip_file_path)
    os.makedirs(zip_file_path, exist_ok=True)

    # Save the uploaded file in the audio folder
    file_path = os.path.join(zip_file_path, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    unzipMusic(zip_file_path, folder_name)

    return {"message": f"Audio folder '{folder_name}' created and file uploaded successfully!"}



# Run the FastAPI server with: uvicorn main:app --reload
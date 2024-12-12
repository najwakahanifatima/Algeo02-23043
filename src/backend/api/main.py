from fastapi import FastAPI, File, Form, UploadFile
import os
from ..utils.unzip_music import unzipMusic 

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
    zip_file_path = os.path.join(BASE_DIR, "uploaded_files", file.filename)
    os.makedirs(zip_file_path, exist_ok=True)

    # Save the uploaded file in the audio folder
    file_path = os.path.join(zip_file_path, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    unzipMusic(zip_file_path, folder_name)

    return {"message": f"Audio folder '{folder_name}' created and file uploaded successfully!"}



# Run the FastAPI server with: uvicorn main:app --reload
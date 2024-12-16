from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from image_information_retrieval.image_processing import *
from music_information_retrieval.music_processing import *
import os
import zipfile
import rarfile
import shutil
import json
import numpy as np

BASE_DIR = os.path.join(os.getcwd())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "database"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def clear_directory(subdir: str):
    """Delete all existing files and folders in the given subdirectory."""
    target_dir = os.path.join(UPLOAD_DIR, subdir)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)  # Delete the entire folder and its contents
    os.makedirs(target_dir)  # Recreate the empty directory

def save_and_extract_file(file: UploadFile, subdir: str):
    """Save and extract uploaded file to the server."""
    clear_directory(subdir)
    target_dir = os.path.join(UPLOAD_DIR, subdir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    file_path = os.path.join(target_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Check if the file is a zip file
    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        os.remove(file_path)  # Remove the zip file after extraction

    # Check if the file is a rar file
    elif rarfile.is_rarfile(file_path):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(target_dir)
        os.remove(file_path)  # Remove the rar file after extraction
    return target_dir

@app.post("/upload-database-audio/")
async def upload_database_audio(file: UploadFile = File(...)):
    try:
        path = save_and_extract_file(file, "audio")
        music_name, music_data = process_music_database(path)
        
        response_data = {
            "music_name" : music_name,
            "music_data" : music_data,
        }
                
        json_output_path = os.path.join(BASE_DIR, "database", "audio", "database_music.json")
        
        try:
            with open(json_output_path, "w") as json_file:
                json.dump(response_data, json_file, indent=4)
            print(f"Response data saved to {json_output_path}")
            return JSONResponse(content={"message": "Upload & Load Audio Success!"}, status_code=200)
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return JSONResponse(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload-database-image/")
async def upload_database_image(file: UploadFile = File(...)):
    try:
        path = save_and_extract_file(file, "images")
        projected_data, pixel_avg, pixel_std, image_name, Uk = process_data_image(path)

        response_data = {
            "image_name" : image_name,
            "projected_data": projected_data,
            "pixel_avg" : pixel_avg,
            "pixel_std": pixel_std,
            "uk": Uk,
            "uk": Uk,
        }

        response_data["image_name"] = [list(item) for item in response_data["image_name"]]

        json_output_path = os.path.join(BASE_DIR, "database", "images", "database_image.json")
        
        try:
            with open(json_output_path, "w") as json_file:
                json.dump(response_data, json_file, indent=4)
            print(f"Response data saved to {json_output_path}")
            return JSONResponse(content={"message": "Upload & Load Images Success!"}, status_code=200)
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return JSONResponse(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/upload-mapper/")
async def upload_mapper(file: UploadFile = File(...)):
    try:
        save_and_extract_file(file, "mappers")
        return JSONResponse(content={"message": "Upload Mapper Success!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start-query/")
async def start_query(file: UploadFile = File(...)): #need adjustment in frontend
    try:
        path = save_and_extract_file(file, "query")
        print(path)
        # if (type == "music"):
            
        # elif (type == "image"):
        
        

        return JSONResponse(content={"message": "Query started successfully!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
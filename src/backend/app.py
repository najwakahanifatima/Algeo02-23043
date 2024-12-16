from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from image_information_retrieval.image_processing import *
from music_information_retrieval.music_processing import *
from image_information_retrieval.iir_model import *
from music_information_retrieval.mir_model import *
from typing import List
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

app.mount("/images", StaticFiles(directory="database/image"), name="images")

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

def save_and_extract_multiple_files(files: List[UploadFile], subdir: str):
    extracted_paths = []
    try:
        for file in files:
            extracted_path = save_and_extract_file(file, subdir)
            extracted_paths.append(extracted_path)
        return extracted_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {e}")

@app.post("/upload-database-audio/")
async def upload_database_audio(files: List[UploadFile] = File(...)):
    try:
        # Initialize an array to hold the results for all files
        response_data = {
            "audios": []  # This will store results for each audio file
        }
        print("gagal di 1")

        start_time = datetime.now()
        print("gagal di 2")
        for file in files:
            path = save_and_extract_file(file, "audio")
            
            music_name, music_data = process_music_database(path)

            response_data["audios"].append({
                "music_name": music_name,
                "music_data": music_data,
            })
        print("gagal di 3")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print("gagal di 4")
        json_output_path = os.path.join(BASE_DIR, "database", "audio", "database_music.json")
        with open(json_output_path, "w") as json_file:
            json.dump(response_data, json_file, indent=4)
        print("gagal di 5")
        print(f"Response data saved to {json_output_path}")
        
        return JSONResponse(
                content={
                    "message": "Upload & Load Audio Success!",
                    "duration" : str(duration.total_seconds()),
                    }, 
                status_code=200)
    except Exception as e:
        print(f"Error uploading audios: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    
@app.post("/upload-database-image/")
async def upload_database_image(files: List[UploadFile] = File(...)):
    print(f"Received {len(files)} files")
    try:
        response_data = {
            "images": []  # This will hold the details for each image
        }
        start_time = datetime.now()

        for file in files:
            path = save_and_extract_file(file, "image")
            
            projected_data, pixel_avg, pixel_std, image_name, Uk = process_data_image(path)

            response_data["images"].append({
                "image_name": image_name,
                "projected_data": projected_data,
                "pixel_avg": pixel_avg,
                "pixel_std": pixel_std,
                "Uk": Uk,
            })

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Save results to JSON file if needed
        json_output_path = os.path.join(BASE_DIR, "database", "image", "database_image.json")
        with open(json_output_path, "w") as json_file:
            json.dump(response_data, json_file, indent=4)

        print(f"Response data saved to {json_output_path}")
        
        # Return the response data
        return JSONResponse(
                content={
                    "message": "Upload & Load Image Success!",
                    "duration" : str(duration.total_seconds()),
                    }, 
                status_code=200)
    except Exception as e:
        print(f"Error uploading images: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-mapper/")
async def upload_mapper(file: UploadFile = File(...)):
    try:
        save_and_extract_file(file, "mapper")
        return JSONResponse(content={"message": "Upload Mapper Success!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start-query/{type}/")
async def start_query(type: str, file: UploadFile = File(...)): #need adjustment in frontend
    try:
        path = save_and_extract_file(file, "query")
        query_path = os.path.join(path, file.filename) #get the query file name
        
        if type == "image":
            duration = image_model(query_path)
            return JSONResponse(
                content={
                    "message" : "Album query processed successfully!",
                    "duration" : duration,
                }
            )
        elif type == "audio":
            duration = music_model(query_path)
            return JSONResponse(
                content={
                    "message" : "Audio query processed successfully!",
                    "duration" : duration,
                }
            )
        return JSONResponse(content={"message": "Query not started due to invalid input."}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
IMAGE_DIR = os.path.join(os.getcwd(), "database", "image")

@app.get("/images")
async def get_images():
    try:
        # Get list of image files in the image directory
        image_files = []
        for filename in os.listdir(IMAGE_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_files.append({
                    "name": filename,
                    "url": f"/images/{filename}"  # Serve image via /images/{filename}
                })
        
        # If no images are found
        if not image_files:
            raise HTTPException(status_code=404, detail="No images found")

        return JSONResponse(content=image_files)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

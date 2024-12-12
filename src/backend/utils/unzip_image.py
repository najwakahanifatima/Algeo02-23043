import zipfile
import os

def unzipImage(zip_folder, hasil_folder) :

    # ambil direktori dimana file dijalankan
    script_dir = os.path.dirname(os.path.realpath(__file__))

    zip_file_path = os.path.join(script_dir, zip_folder)

    extract_folder = os.path.join(script_dir, '..', 'database_image', hasil_folder)

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.printdir()

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

        for file in zip_ref.namelist():
            # Check if the file is an image based on its extension
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # Extract the image to the specified folder
                zip_ref.extract(file, extract_folder)
                print(f'{file} has been extracted to {extract_folder}')

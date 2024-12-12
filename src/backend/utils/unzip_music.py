import zipfile
import os

def unzipMusic(zip_folder, hasil_folder) :
    # ambil direktori dimana file dijalankan
    script_dir = os.path.dirname(os.path.realpath(__file__))

    zip_file_path = os.path.join(script_dir, zip_folder)

    extract_folder = os.path.join(script_dir, '..', 'database_music', hasil_folder)

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    audio_extensions = ['mid']

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # List all contents of the ZIP file (optional)
            zip_ref.printdir()

            for file in zip_ref.namelist():
                if any(file.lower().endswith(ext) for ext in audio_extensions): # cek secara case-insensitive
                    zip_ref.extract(file, extract_folder)
                    print(f'{file} has been extracted to {extract_folder}')
    except FileNotFoundError as e:
        print(f"Error: {e}")
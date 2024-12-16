import json

def txt_to_json(txt_file_path, json_file_path):
    try:
        data = {}

        with open(txt_file_path, "r") as txt_file:
            for line in txt_file:
                # abaikan baris kosong
                if ":" in line:
                    key, value = map(str.strip, line.split(":", 1))
                    data[key] = value

        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Converted {txt_file_path} to {json_file_path} successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

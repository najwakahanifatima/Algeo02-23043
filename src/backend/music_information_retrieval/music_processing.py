import numpy as np
import os
from mido import MidiFile
import json

BASE_DIR = os.path.abspath(os.getcwd())

def numpy_to_list(arr):
    return arr.tolist() if isinstance(arr, np.ndarray) else arr

############################################# Ekstraksi Fitur #############################################

def numpy_to_list(arr):
    return arr.tolist() if isinstance(arr, np.ndarray) else arr

def histogram(data, bins, min, max):
    histogram, _ = np.histogram(data, bins=bins, range=(min, max))
    if(np.sum(histogram) != 0):
        histogram = histogram / np.sum(histogram)
    return histogram

def absolute_tone_based(arrMidi):
    bins = 128
    return histogram(arrMidi, bins, 0, 127)

def relative_tone_based(arrMidi):
    if len(arrMidi) < 2:
        raise ValueError("arrMidi must contain at least two notes for relative tone calculation.")
    diffs = [arrMidi[i + 1] - arrMidi[i] for i in range(len(arrMidi) - 1)]
    bins = 255
    return histogram(diffs, bins, -127, 127)

def first_tone_based(arrMidi):
    if not arrMidi:
        raise ValueError("arrMidi must contain at least one note.")
    diffs = [note - arrMidi[0] for note in arrMidi]
    bins = 255
    return histogram(diffs, bins, -127, 127)

############################################# Pemrosesan Musik #############################################

def extract_notes(midi_file_path):
    midi = MidiFile(midi_file_path)
    notes = []
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.channel==0 and msg.velocity > 0: #channel== 0 adalah channel 1
                notes.append(msg.note)
    return notes

# normalisasi note
def normalize_pitch(notes):
    avg_pitch = np.mean(notes)
    std_pitch = np.std(notes)
    if std_pitch == 0:
        return [0 for note in notes]
    normalized_notes = [(note - avg_pitch)/std_pitch for note in notes]
    return normalized_notes

# windowing
def windowing(notes, window_size, step_size):
    windows = []
    for start in range(0, len(notes) - window_size + 1, step_size):
        window = notes[start:start + window_size]
        windows.append(window)
    return windows

############################################# Pemrosesan Database Musik #############################################

def process_music_database(database_music_path):
    musicdata = []
    music_name = []
    
    with os.scandir(database_music_path) as entries:
        for i, entry in enumerate(entries): #adjusted
            if entry.is_file():  # Ensure it's a file
                if entry.name.endswith(".mid"):
                    # print(f"Processing {file_name}...")

                    temp = []
                    music_path = os.path.join(database_music_path, entry.name)
                    notes = extract_notes(music_path)
                    if (notes):
                        normalized_notes = normalize_pitch(notes)
                        windows = windowing(normalized_notes, window_size=20, step_size=4)
                        for window in windows:
                            atb_histogram = absolute_tone_based(window)
                            rtb_histogram = relative_tone_based(window)
                            ftb_histogram = first_tone_based(window)
                            temp.append(numpy_to_list(atb_histogram))
                            temp.append(numpy_to_list(rtb_histogram))
                            temp.append(numpy_to_list(ftb_histogram))
                        music_name.append((i, entry.name))
                        musicdata.append(temp)
                    # else:
                        # print(f"{entry.name}: No note in channel 1 detected.")
    musicdata = numpy_to_list(musicdata)
    return music_name, musicdata

def process_query(file_name):
    data_query = []
    
    if file_name.endswith(".mid"):
        notes = extract_notes(file_name)
        if (notes):
                normalized_notes = normalize_pitch(notes)
                windows = windowing(normalized_notes, window_size=20, step_size=4)
                for window in windows:
                    atb_histogram = absolute_tone_based(window)
                    rtb_histogram = relative_tone_based(window)
                    ftb_histogram = first_tone_based(window)
                    data_query.append(atb_histogram)
                    data_query.append(rtb_histogram)
                    data_query.append(ftb_histogram)

    return data_query

def process_music_query(file_query) :
    #similarity computation using cosinus similarity
    base_dir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, ".." , "database", "audio","database_music.json")
    print(f"Resolved path: {json_path}")
    
    try:
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"The file '{json_path}' was not found.")
        
        # Read the JSON file
        with open(json_path, "r") as json_file:
            database = json.load(json_file)  # Use json.load for reading JSON files
        
        music_name = np.array(database["music_name"])
        music_data = np.array(database["music_data"], dtype=object)
        
        magnitude_query = np.array([]) # index: ATB, RTB, FTB
        query = process_query(file_query)
        ATB_query = np.array(query[0])
        RTB_query = np.array(query[1])
        FTB_query = np.array(query[2])

        cos_sim_result_avg = []
        
        #get data magnitude of tones in query
        magnitude = np.linalg.norm(ATB_query)
        magnitude_query = np.append(magnitude_query, magnitude)
        magnitude = np.linalg.norm(RTB_query)
        magnitude_query = np.append(magnitude_query, magnitude)
        magnitude = np.linalg.norm(FTB_query)
        magnitude_query = np.append(magnitude_query, magnitude)
            
        #compute cos similarity
        for idx_music in range(len(music_data)) :
            temp_cos_sim = []
            for tone_dist in range(3) :
                dot_product = np.dot(query[tone_dist], np.array(music_data[idx_music][tone_dist]))
                norm_query = np.linalg.norm(query[tone_dist])
                norm_music_data = np.linalg.norm(np.array(music_data[idx_music][tone_dist]))
                res_cosine_sim = dot_product / (norm_query * norm_music_data)
                temp_cos_sim.append(res_cosine_sim)
            avg_cosine_sim = np.mean(temp_cos_sim)
            #semakin besar cos_sim, semakin kecil sudut, semakin mirip
            cos_sim_result_avg.append([idx_music, avg_cosine_sim])
            
        sorted_cos_sim = sorted(cos_sim_result_avg, key=lambda x:x[1], reverse=True)
        sorted_cos_sim_indices = [item[0] for item in sorted_cos_sim]
        
        max_cos_sim = sorted_cos_sim[0][1]
            
        mir_result = []
        i = 0
        for index in sorted_cos_sim_indices:
            similarity_percentage = sorted_cos_sim[i][1] / max_cos_sim * 100
            r_similarity_percentage = round(similarity_percentage, 2)
            if  r_similarity_percentage >= 70:
                mir_result.append((music_name[index][1], r_similarity_percentage))
            else:
                break
            i += 1
            
        mir_json = {
            "music": mir_result
        }
        
        mir_json["music"] = [list(item) for item in mir_json["music"]]
        
        json_output_path = os.path.join(BASE_DIR, "database", "query", "query.json")
        
        try:
            with open(json_output_path, "w") as json_file:
                json.dump(mir_json, json_file, indent=4)
            print(f"Response data saved to {json_output_path}")
            # return JSONResponse(content={"message": f"{json_output_path}"}, status_code=200)
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            # return JSONResponse(status_code=500, detail=str(e))
            
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# def process_music_query2(file_query) :
#     #similarity computation using cosinus similarity
#     magnitude_query = np.array([]) # index: ATB, RTB, FTB
#     query = process_query(file_query, "database/audio") #need checking
#     ATB_query = np.array(query[0])
#     RTB_query = np.array(query[1])
#     FTB_query = np.array(query[2])
#     music_name = database_music["music_name"]
#     music_data = process_music_database(database_folder)

#     cos_sim_result_avg = []
    
#     #get data magnitude of tones in query
#     magnitude = np.linalg.norm(ATB_query)
#     magnitude_query = np.append(magnitude_query, magnitude)
#     magnitude = np.linalg.norm(RTB_query)
#     magnitude_query = np.append(magnitude_query, magnitude)
#     magnitude = np.linalg.norm(FTB_query)
#     magnitude_query = np.append(magnitude_query, magnitude)
        
#     #compute cos similarity
#     for idx_music in range(len(music_data)) :
#         temp_cos_sim = []
#         for tone_dist in range(3) :
#             dot_product = np.dot(query[tone_dist], music_data[idx_music][tone_dist])
#             norm_query = np.linalg.norm(query[tone_dist])
#             norm_music_data = np.linalg.norm(music_data[idx_music][tone_dist])
#             res_cosine_sim = dot_product / (norm_query * norm_music_data)
#             temp_cos_sim.append(res_cosine_sim)
#         avg_cosine_sim = np.mean(temp_cos_sim)
#         #semakin besar cos_sim, semakin kecil sudut, semakin mirip
#         cos_sim_result_avg.append([idx_music, avg_cosine_sim])
        
#     sorted_cos_sim = sorted(cos_sim_result_avg, key=lambda x:x[1], reverse=True)
#     sorted_cos_sim_indices = [item[0] for item in sorted_cos_sim]
    
#     max_cos_sim = sorted_cos_sim[0][1]
        
#     mir_result = []
#     i = 0
#     for index in sorted_cos_sim_indices:
#         similarity_percentage = sorted_cos_sim[i][1] / max_cos_sim * 100
#         mir_result.append((music_name[index][1], similarity_percentage))
#         i += 1
    
#     return np.array(mir_result)


# # test
# midi_file_path = "Let_Me_Be_Free.mid"
# notes = extract_notes(midi_file_path)
# normalized_notes = normalize_pitch(notes)
# windows = window(normalized_notes, window_size=20, step_size=4)
# for window in windows:
#     atb_histogram = absolute_tone_based(window)
#     rtb_histogram = relative_tone_based(window)
#     ftb_histogram = first_tone_based(window)
# print(f"ATB Histogram: {atb_histogram}")
# print(f"RTB Histogram: {rtb_histogram}")
# print(f"FTB Histogram: {ftb_histogram}")
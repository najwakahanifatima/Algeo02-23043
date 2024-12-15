from datetime import datetime
from music_processing import process_music_query

start_time = datetime.now()

file_query = "Tico_Tico.mid"
database_folder = "database_music"

mir_result = process_music_query(file_query, database_folder)
print(mir_result)

#time computing
result = sum(range(10**6))
end_time = datetime.now()
duration = end_time - start_time

print(f"Computation took {duration}")
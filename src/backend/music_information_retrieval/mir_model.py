from datetime import datetime
from .music_processing import process_music_query

def music_model(file_query):
    start_time = datetime.now()

    process_music_query(file_query)

    #time computing
    result = sum(range(10**6))
    end_time = datetime.now()
    duration = end_time - start_time

    return str(duration.total_seconds())
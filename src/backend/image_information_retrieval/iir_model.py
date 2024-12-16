from datetime import datetime
from .image_processing import process_image_query

def image_model(file_query):
    start_time = datetime.now()

    process_image_query(file_query)

    #time computing
    result = sum(range(10**6))
    end_time = datetime.now()
    duration = end_time - start_time

    return str(duration.total_seconds())
        
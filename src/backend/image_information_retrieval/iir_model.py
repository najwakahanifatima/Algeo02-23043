from datetime import datetime
from image_processing import process_image_query

start_time = datetime.now()

file_query = "database_image/test/lion1.jpg"
database_folder = "database_image/test"

iir_result = process_image_query(file_query, database_folder)
print(iir_result)

#time computing
result = sum(range(10**6))
end_time = datetime.now()
duration = end_time - start_time

print(f"Computation took {duration}")
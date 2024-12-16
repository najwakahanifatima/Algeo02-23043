import os
import numpy as np
from PIL import Image
from scipy.sparse.linalg import svds
import numpy as np
import json

BASE_DIR = os.path.abspath(os.getcwd())
K_Components = 10  #bisa diubah2 ya wak

def numpy_to_list(arr):
    return arr.tolist() if isinstance(arr, np.ndarray) else arr

def grayscale(filename):
    #convert image to grayscale, resize to 64 x 64, then flatten to be a vector
    image = Image.open(filename).resize((144, 144))
    grayscale_image= image.convert("L")
    grayscale_array = np.array(grayscale_image)
    grayscale_vector = grayscale_array.flatten()
    return grayscale_vector

def standardize(image_arrays):
    #get the standardized data
    image_stack = np.stack(image_arrays, axis=0)
    pixel_avg = np.mean(image_stack, axis=0)
    pixel_std = np.where(image_stack.std(axis=0) == 0, 1, image_stack.std(axis=0))
    return ((image_stack - pixel_avg) / pixel_std).astype(np.float64), numpy_to_list(pixel_avg), numpy_to_list(pixel_std)

def comp_covariance(standardized_data):
    #compute matrix covariance
    return np.cov(standardized_data, rowvar=False, dtype=np.float64)

def comp_svd(covariance_data, k):
    #get eig vectors and values U_K, S, VT from SVD
    Uk, S, VT = svds(covariance_data, k=k)
    return Uk, S, VT

def projection_data(standardized_data, U):
    #get the Z matrix (data projection)
    return numpy_to_list(np.dot(standardized_data, U))

def process_data_image(folder_path):
    image_pixel_data = []
    image_name = []
    
    #read all imaged from folder database
    with os.scandir(folder_path) as entries:
        for i, entry in enumerate(entries): #adjusted
            if entry.is_file():  # Ensure it's a file
                image_path = os.path.join(folder_path, entry.name)
                img_array = grayscale(image_path)
                image_pixel_data.append(img_array)
                image_name.append((i, entry.name))
    
    standardized_data, pixel_avg, pixel_std = standardize(image_pixel_data)
    
    covariance_data = comp_covariance(standardized_data)
    
    # np.random.seed(42)
    Uk, S, VT = comp_svd(covariance_data, k=K_Components)
    
    # Uk = get_Uk(U, K_Components)
    # U, S, VT = np.linalg.svd(covariance_data, full_matrices=False)
    # UK = U[:,:K_Components]
    # row, col = Uk.shape
    # print("row UK: " + str(row))
    # print("col UK: " + str(col))
    
    projected_data = projection_data(standardized_data, Uk)
    
    # explained_variance_ratio = S / S.sum()
    # print("evr: " + str(explained_variance_ratio))

    projected_data = numpy_to_list(projected_data)
    pixel_avg = numpy_to_list(pixel_avg)
    pixel_std = numpy_to_list(pixel_std)
    Uk = numpy_to_list(Uk)
    
    return projected_data, pixel_avg, pixel_std, image_name, numpy_to_list(Uk) #cekkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk

def project_query(query, pixel_avg, pixel_std, Uk):
    return np.dot(((query - pixel_avg)/pixel_std), Uk)

def euc_dist(projected_query, projected_data):
    return [(index, np.linalg.norm(projected_query - value)) for index, value in enumerate(projected_data)]

def process_image_query(file_name):  
    # BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    # folder_path = os.path.join(BASE_DIR, "database", "images", "database_image.json")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, ".." , "database", "image","database_image.json")
    print(f"Resolved path: {json_path}")
    try:
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"The file '{json_path}' was not found.")

        # Read the JSON file
        with open(json_path, "r") as json_file:
            database = json.load(json_file)  # Use json.load for reading JSON files

        # Your logic to process `image_path` and `database` here
        list_projected_data = database["projected_data"]
        list_pixel_avg = database["pixel_avg"]
        list_pixel_std = database["pixel_std"]
        image_name = database["image_name"]
        list_Uk = database["Uk"]

        projected_data = np.array(list_projected_data)
        pixel_avg = np.array(list_pixel_avg)
        pixel_std = np.array(list_pixel_std)
        Uk = np.array(list_Uk)
        # print("z = ", projected_data)
        # print("pixel avg = ", pixel_avg)
        # print("pixel std =", pixel_std)
        # print("image name= ", image_name)
        # print("Uk= ", Uk)
        # print(f"Resolved path: {json_path}")

        #process query pixels
        query_raw = grayscale(file_name)
        projected_query = project_query(query_raw, pixel_avg, pixel_std, Uk)
        projected_query = (projected_query.reshape(-1,1)).T
        #get sorted euclidian distance
        euc_distance = euc_dist(projected_query, projected_data)
        sorted_euc_distance = sorted(euc_distance, key=lambda x: x[1])
        sorted_euc_dist_indices = [item[0] for item in sorted_euc_distance]
        print(f"4 Resolved path: {json_path}")
        max_distance = sorted_euc_distance[len(image_name)-1][1] #get highest euc dist
        
        #append sorted image and similarity percentage result
        iir_result = []
        i = 0
        for index in sorted_euc_dist_indices:
            similarity_percentage = (max_distance - sorted_euc_distance[i][1]) / max_distance * 100
            r_similarity_percentage = round(similarity_percentage, 2)
            if r_similarity_percentage >= 70 :
                iir_result.append((image_name[index][1], r_similarity_percentage))
            i += 1

        print(iir_result)

        iir_json = {
            "image" : iir_result
        }
        
        iir_json["image"] = [list(item) for item in iir_json["image"]]

        json_output_path = os.path.join(BASE_DIR, "src", "backend", "database", "query", "query_image.json")
        directory = os.path.dirname(json_output_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        try:
            with open(json_output_path, "w") as json_file:
                json.dump(iir_json, json_file, indent=4)
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

    

# process_image_query("C:/laptop lala/Algeo02-23043/src/backend/image_information_retrieval/lantik iso.jpg", )

# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
# folder_path = os.path.join(BASE_DIR, "database_image", "test")
# projected_data, pixel_avg, pixel_std, image_name, Uk = process_data_image(folder_path)

# response_data = {
#     "image_name" : image_name,
#     "projected_data": projected_data,
# }

# print(response_data)
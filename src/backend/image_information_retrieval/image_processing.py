import os
import numpy as np
from PIL import Image
from scipy.sparse.linalg import svds
import numpy as np

K_Components = 10  #bisa diubah2 ya wak

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
    return ((image_stack - pixel_avg) / pixel_std).astype(np.float64), pixel_avg, pixel_std

def comp_covariance(standardized_data):
    #compute matrix covariance
    return np.cov(standardized_data, rowvar=False, dtype=np.float64)

def comp_svd(covariance_data, k):
    #get eig vectors and values U_K, S, VT from SVD
    Uk, S, VT = svds(covariance_data, k=k)
    return Uk, S, VT

def projection_data(standardized_data, U):
    #get the Z matrix (data projection)
    return np.dot(standardized_data, U)

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
    
    return projected_data, pixel_avg, pixel_std, image_name, Uk #cekkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk

def project_query(query, pixel_avg, pixel_std, Uk):
    return np.dot(((query - pixel_avg)/pixel_std), Uk)

def euc_dist(projected_query, projected_data):
    return [(index, np.linalg.norm(projected_query - value)) for index, value in enumerate(projected_data)]

def process_image_query(file_name, folder_path):
    #get variables from dataset
    projected_data, pixel_avg, pixel_std, image_name, Uk = process_data_image(folder_path)
    
    #process query pixels
    query_raw = grayscale(file_name)
    projected_query = project_query(query_raw, pixel_avg, pixel_std, Uk)
    projected_query = (projected_query.reshape(-1,1)).T
    
    #get sorted euclidian distance
    euc_distance = euc_dist(projected_query, projected_data)
    sorted_euc_distance = sorted(euc_distance, key=lambda x: x[1])
    sorted_euc_dist_indices = [item[0] for item in sorted_euc_distance]
    
    max_distance = sorted_euc_distance[len(image_name)-1][1] #get highest euc dist
    
    #append sorted image and similarity percentage result
    iir_result = []
    i = 0
    for index in sorted_euc_dist_indices:
        similarity_percentage = (max_distance - sorted_euc_distance[i][1]) / max_distance * 100
        iir_result.append((image_name[index][1], similarity_percentage))
        i += 1
    
    return np.array(iir_result)
import os
import numpy as np
from PIL import Image

def grayscale(filename):
    image = Image.open(filename).resize((64, 64))
    
    img_array = np.array(image)
    
    grayscale_array = (0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]).astype(np.uint8)
    
    # grayscale_image = Image.fromarray(grayscale_array, mode="L")
    
    # grayscale_image.save(f"{filename}_grayscale.jpg")
    
    grayscale_vector = grayscale_array.flatten()
    
    return grayscale_vector

def standardize_images(image_arrays):
    image_stack = np.stack(image_arrays, axis=0)
    pixel_mean = np.mean(image_stack, axis=0)
    # std_dev = np.std(image_stack)
    
    standardized_images = (image_stack - pixel_mean)

    return standardized_images, pixel_mean
'''
def svd(a):
    row, col = a.shape

    a_transpose = a.T
    a_multiplied = np.dot(a_transpose, a)
    nilai_eigen, v = np.linalg.eig(a_multiplied)

    idx = np.argsort(nilai_eigen)[::-1]  
    nilai_eigen = nilai_eigen[idx]
    v = v[:, idx]

    v_satuan = []
    v_transpose = v.T
    for vector in v_transpose :
        vector_satuan = []
        sum = 0
        for el in vector :
            sum += el**2
        besar_vector = sum**(1/2)
        for el in vector :
            temp = el/besar_vector
            vector_satuan.append(temp)
        v_satuan.append(vector_satuan)
    
    v_satuan = np.array(v_satuan).T

    nilai_singular = np.sqrt(np.maximum(nilai_eigen, 0))

    u = []
    for i in range(len(nilai_singular)):
        if nilai_singular[i] > 0:  
            u_column = np.dot(a, v[:, i]) / nilai_singular[i]
        else:
            u_column = np.zeros(row)
        u.append(u_column)
    u = np.array(u).T

    u /= np.linalg.norm(u, axis=0)

    sigma = [[0 for i in range(col)] for j in range(row)]
    for i in range(row) :
        sigma[i][i] = np.sqrt(nilai_eigen[i])
#
    return u, sigma, v_satuan
'''

def matriks_kovarians(n, x):
    # np.save('standarized_images.npy', x)
    # x_numpy = np.load('standarized_images.npy', mmap_mode='r')
    x_numpy = np.array(x)
    # print(x_numpy.shape)
    # print((np.transpose(x_numpy)).shape)
    c = np.dot(np.transpose(x_numpy), x_numpy)/ x_numpy.shape[0]
    # c = (np.dot(x_numpy.T, x_numpy)/n)    
    return c

def proyeksi_data(k, u, standardized) :
    u_k = u[:k, :]

    z = np.dot(standardized, u_k.T)

    return z

import numpy as np

# # Function to perform SVD on a single chunk and return its components
# def svd_chunk(chunk):
#     U, s, Vt = np.linalg.svd(chunk, full_matrices=False)
#     return U, s, Vt

# # Function to perform incremental SVD
# def incremental_svd(data, chunk_size):
#     n_samples, n_features = data.shape
#     U_combined, S_combined, V_combined = None, None, None

#     for i in range(0, n_samples, chunk_size):
#         chunk = data[i:i + chunk_size]
#         U, s, Vt = svd_chunk(chunk)

#         if U_combined is None:
#             U_combined, S_combined, V_combined = U, s, Vt
#         else:
#             U_combined = np.vstack((U_combined, U))
#             S_combined = np.concatenate((S_combined, s))
#             V_combined = np.vstack((V_combined, Vt))

#     return U_combined, S_combined, V_combined


def process_images(folder_path):
    print("gambar")
    image_arrays = []
    image_data_name = []
    i = 0
    
    # Baca semua file gambar di folder
    for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            img_array = grayscale(image_path)
            image_arrays.append(img_array)
            image_data_name.append([i, filename])
            i += 1
    
    print(image_data_name)

    standardized_images, pixel_mean = standardize_images(image_arrays)    
    
    covMatrix = np.cov(standardized_images, rowvar = False)
    # print("covmatrix: " + str(np.shape(covMatrix)))
    # print(covMatrix)
    
    eigVal, eigVec = np.linalg.eig(covMatrix)
    # print("eigvec: " + str(np.shape(eigVec)))
    # print(eigVec)
    # print("eigval: " + str(np.shape(eigVal)))
    # print(eigVal)
    
    indexed_eigval = [(index, value) for index, value in enumerate(eigVal)]
    sorted_indexed_eigval = sorted(indexed_eigval, key=lambda x:x[1], reverse=True)
    
    sorted_indices = [item[0] for item in sorted_indexed_eigval] #index eigvalue yg sudah di sort desc
    
    k = 20
    selected_eigvec = []
    
    for i in range(k):
        selected_eigvec.append(eigVec.T[sorted_indices[i]])
    
    selected_eigVecK = np.array(selected_eigvec).T
    # print("selected eigvec: " + str(selected_eigVecK.shape))
    
    z = np.dot(standardized_images, selected_eigVecK)
    # print("z: " + str(z.shape))
    
    query = grayscale("tayl.jpg")
    pro_query = np.dot((query - pixel_mean), selected_eigVecK)
    # print("pro query: " + str(pro_query.shape))
    
    euc_dist = [(index, np.linalg.norm(pro_query - value)) for index, value in enumerate(z)]
    sorted_euc_dist = sorted(euc_dist, key=lambda x: x[1])
    sorted_euc_dist_indices = [item[0] for item in sorted_euc_dist]
    
    print("euc_dist: " + str(len(euc_dist)))
    print(sorted_euc_dist)
    
    # print("hasil query nomor 1: ")
    # print(image_data_name[sorted_euc_dist_indices[0][1]])
    # print(image_data_name[sorted_euc_dist_indices[1][1]])
    
process_images("../trial_image")
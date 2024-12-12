import os
import numpy as np
from PIL import Image
from scipy.sparse.linalg import svds
from image_similarity import projected_query


def grayscale(filename):
    image = Image.open(filename).resize((64, 64))
        
    grayscale_image= image.convert("L")

    grayscale_array = np.array(grayscale_image)
    
    grayscale_vector = grayscale_array.flatten()
    
    return grayscale_vector

def standardize_images(image_arrays):
    image_stack = np.stack(image_arrays, axis=0)

    pixel_mean = np.mean(image_stack, axis=0)
    pixel_std = np.std(image_stack, axis=0)
    
    standardized_images = (image_stack - pixel_mean) / pixel_std

    return standardized_images, pixel_mean


def matriks_kovarians(n, x):
    x_numpy = np.array(x)
    c = (np.matmul(x_numpy.T, x_numpy)/n)
    return c

def proyeksi_data(k, u, standardized) :
    u_k = u[:, :k]

    row,col = u_k.shape
    print(row)
    print(col)
    print("u_k= ")
    print(u_k)

    z = np.dot(standardized, u_k)

    return z

def process_images(folder_path):
    print("gambar")
    image_arrays = []
    image_name_arrays = []
    
    # Baca semua file gambar di folder
    i = 0
    for filename in sorted(os.listdir(folder_path)):
        image_path = os.path.join(folder_path, filename)
        img_array = grayscale(image_path)
        image_arrays.append(img_array)

        image_name_array = []
        image_name_array.append(i)
        image_name_array.append(filename)
        image_name_arrays.append(image_name_array)
        i += 1

    print(image_name_arrays)

    standardized_images, avg_pixel = standardize_images(image_arrays)
    print("standardized image=")
    row, col = standardized_images.shape
    print(row)
    print(col)
    print(standardized_images)
    print("========================================")
    
    #image_kovarians = matriks_kovarians(len(image_arrays),standardized_images)
    image_kovarians = np.cov(standardized_images, rowvar= False, dtype=np.float64)
    row, col = image_kovarians.shape
    print(row)
    print(col)
    print("kofarian = " )
    print(image_kovarians)
    print("========================================")
    
    k = 5
    #u, s, v = svds(image_kovarians, k=k)
    u, s, v = np.linalg.svd(image_kovarians, full_matrices=False)
    u = u[:, :5]
    row, col = u.shape
    print(row)
    print(col)
    row = s.shape
    print(row)
    row, col = v.shape
    print(row)
    print(col)
    print("u=" )
    print(u)
    print("========================================")
    hasil = proyeksi_data(5, u, standardized_images)
    row, col = hasil.shape
    print(row)
    print(col)
    print(hasil)
    return hasil, avg_pixel, u, image_name_arrays

######################################################

hasil_proses , avg_pixel, u, image_name_arrays = process_images("Human Faces Dataset/test")

print(avg_pixel)

vector_query = grayscale("Human Faces Dataset/test/000003.jpg")
row = vector_query.shape
print(row)
print("vector query= ")
print(vector_query)

u_k = u[:, :5]
row, col = u_k.shape
print(row)
print(col)
print("u_k")
print(u_k)

q = projected_query(vector_query, avg_pixel, u_k)
row = q.shape
print(row)
print("projected query")
print(q)
print("--------------------------------")

q = q.reshape(-1, 1)
newQ = q.T
row = newQ.shape
print(row)
print("projected query")
print(newQ)
print("--------------------------------")

euc_dist = [(index, np.linalg.norm(q - value)) for index, value in enumerate(hasil_proses)]
sorted_euc_dist = sorted(euc_dist, key=lambda x: (x[1], x[0]))
sorted_euc_dist_indices = [item[0] for item in sorted_euc_dist]

row = sorted_euc_dist
print(row)
print("sorted euc dist")
print(sorted_euc_dist)
print("--------------------------------")

print(sorted_euc_dist_indices)
print("--------------------------------")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

'''
hasil = retrieve_img(hasil_proses, q, avg_pixel, u_k)
print("retrieve_img")
print(hasil)

hasilnp = np.array(hasil)
row = hasilnp.shape
print(row)
'''

for el in sorted_euc_dist_indices :
    print(image_name_arrays[el][1])



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
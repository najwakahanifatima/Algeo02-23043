import numpy as np

#test case
'''
query = np.array([[0.5, 1.5, 2.5]]) # query vector (q'): 1 x p
projected_data = np.array([
    [1.1, 2.1],
    [2.0, 3.0],
    [3.0, 4.0]
    ])  # projected data (z): i x k
avg_pixel = np.array([[1.0, 1.0, 1.0]])  # average pixel value: 1 x p
eigen_vector_k = np.array([
    [0.6, 0.8],
    [0.7, 0.5],
    [0.1, 0.2]
    ])  # eigenvector matrix (Uk): p x k
'''
def projected_query(query, avg_pixel, eigen_vector_k) :
    q = np.matmul((query - avg_pixel), eigen_vector_k) #(q: apakah matmul boleh dipake?)
    return q

def euc_dist(z, query, avg_pixel, eigen_vector_k) :
    arr_res = []
    k = eigen_vector_k.shape[1] #get cols, number of k, principal components
    q = projected_query(query, avg_pixel, eigen_vector_k)
    #z = projected_data
    n = z.shape[0] #get rows, number of image
    limit = np.inf
    for j in range(n) :
        d = 0.0
        for i in range(k):
            d += ((q[0][i] - z[j][i]) **2)
        d = np.sqrt(d)
        if d <= limit :
            arr_res.append([j, float(d)]) #j index of img, d euc dist
    return arr_res

def retrieve_img(z, query, avg_pixel, eigen_vector_k) :
    res = euc_dist(z, query, avg_pixel, eigen_vector_k)
    res.sort(key=lambda x:x[1])
    print(res)
    return res
    
#retrieve_img(projected_data, query)
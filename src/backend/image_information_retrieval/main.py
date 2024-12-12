import os
import PIL
from process_image import process_images
from process_image import grayscale
from image_similarity import retrieve_img 
from image_similarity import projected_query

print("Hello world")
hasil_proses , avg_pixel, u = process_images("Human Faces Dataset/test")

vector_query = grayscale("Human Faces Dataset/test/lala1.jpg")
print("vector query= ")
print(vector_query)

u_k = u[:, :10]
print("u_k")
print(u_k)




index = hasil[0][0]
print(index)

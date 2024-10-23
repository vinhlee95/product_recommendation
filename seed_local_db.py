from pinecone.grpc import PineconeGRPC as Pinecone
import os
import pandas as pd

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "products"
product_index = pc.Index(index_name)
print(product_index)


# Load the dataset
product_data = [
  {"id": 1, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "iPhone 13", "price": 799.99, "brand": "Apple", "model": "13", "description": "Latest model with A15 Bionic chip"},
  {"id": 2, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Samsung Galaxy S21", "price": 699.99, "brand": "Samsung", "model": "S21", "description": "Flagship model with Exynos 2100"},
  {"id": 3, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Google Pixel 6", "price": 599.99, "brand": "Google", "model": "6", "description": "Newest Pixel with Google Tensor chip"},
  {"id": 4, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "OnePlus 9", "price": 729.99, "brand": "OnePlus", "model": "9", "description": "High-performance phone with Snapdragon 888"},
  {"id": 5, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Xiaomi Mi 11", "price": 749.99, "brand": "Xiaomi", "model": "Mi 11", "description": "Flagship phone with Snapdragon 888"},
  {"id": 6, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Sony Xperia 1 III", "price": 1199.99, "brand": "Sony", "model": "Xperia 1 III", "description": "Premium phone with 4K display"},
  {"id": 7, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Oppo Find X3 Pro", "price": 1149.99, "brand": "Oppo", "model": "Find X3 Pro", "description": "High-end phone with Snapdragon 888"},
  {"id": 8, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Huawei P50 Pro", "price": 999.99, "brand": "Huawei", "model": "P50 Pro", "description": "Flagship phone with Kirin 9000"},
  {"id": 9, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Asus ROG Phone 5", "price": 999.99, "brand": "Asus", "model": "ROG Phone 5", "description": "Gaming phone with Snapdragon 888"},
  {"id": 10, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Realme GT", "price": 499.99, "brand": "Realme", "model": "GT", "description": "Affordable phone with Snapdragon 888"},
  {"id": 11, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Nokia 8.3 5G", "price": 649.99, "brand": "Nokia", "model": "8.3 5G", "description": "5G phone with Snapdragon 765G"},
  {"id": 12, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Motorola Edge 20 Pro", "price": 699.99, "brand": "Motorola", "model": "Edge 20 Pro", "description": "High-end phone with Snapdragon 870"},
  {"id": 13, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Vivo X60 Pro", "price": 799.99, "brand": "Vivo", "model": "X60 Pro", "description": "Premium phone with Snapdragon 870"},
  {"id": 14, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "ZTE Axon 30 Ultra", "price": 749.99, "brand": "ZTE", "model": "Axon 30 Ultra", "description": "Flagship phone with Snapdragon 888"},
  {"id": 15, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "LG Wing", "price": 999.99, "brand": "LG", "model": "Wing", "description": "Innovative phone with dual screens"},
  {"id": 16, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Apple iPhone SE (2020)", "price": 399.99, "brand": "Apple", "model": "SE (2020)", "description": "Affordable iPhone with A13 Bionic chip"},
  {"id": 17, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Samsung Galaxy A52", "price": 499.99, "brand": "Samsung", "model": "A52", "description": "Mid-range phone with Snapdragon 720G"},
  {"id": 18, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Google Pixel 4a", "price": 349.99, "brand": "Google", "model": "4a", "description": "Budget-friendly phone with Snapdragon 730G"},
  {"id": 19, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "OnePlus Nord 2", "price": 399.99, "brand": "OnePlus", "model": "Nord 2", "description": "Affordable phone with MediaTek Dimensity 1200"},
  {"id": 20, "category": "smartphone", "reviews": 1000, "rating": 4.9, "name": "Xiaomi Redmi Note 10 Pro", "price": 279.99, "brand": "Xiaomi", "model": "Redmi Note 10 Pro", "description": "Budget phone with Snapdragon 732G"}
]


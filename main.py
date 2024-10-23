from openai import OpenAI, embeddings
import pandas as pd
import numpy as np

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Sample product database
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

# Add product data to dataframe
product_data_df = pd.DataFrame(product_data)
# print(product_data_df)

# Create column with combined data
product_data_df['combined'] = product_data_df.apply(lambda row: f"{row['brand']}, {row['name']}, {row['category']}, {row['description']}, {row['rating']}, {row['price']}, {row['reviews']}", axis=1)
# print(product_data_df)

# Create embeddings
def get_embedding(text):
  response = embeddings.create(
    model="text-embedding-ada-002",
    input=[text],
  )

  return response.data[0].embedding

product_data_df['text_embedding'] = product_data_df.combined.apply(lambda x: get_embedding(x))
# print(product_data_df)

# Get similarities for products
# Function to calculate cosine similarity between two vectors
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_top_3_products(question: str):
   # Generate embedding for the user input
  response = embeddings.create(
      model="text-embedding-ada-002",
      input=[question],
  )
  embedded_input = response.data[0].embedding

  # Calculate cosine similarity for each product
  product_data_df['similarity'] = product_data_df.text_embedding.apply(lambda x: cosine_similarity(x, embedded_input))

  # Sort products by similarity in descending order
  sorted_products = product_data_df.sort_values(by='similarity', ascending=False)

  # Select the top 3 most relevant products
  top_3_products = sorted_products.head(1)

  # Prepare the list of top 3 products
  return top_3_products
  

# Create a list to store message objects
message_objects = []
top_3_products = None

while True:
  # Prompt the user for input
  # print("Please tell me what you are looking for? For example your skin condition or budget.")

  question = input(">> ")

  # Add a system message to set the assistant's behavior
  message_objects.append({
     "role": "system", 
     "content": """
        You're a chatbot helping customers with beauty-related questions and providing product recommendations. 
        You should only recommend the product that is recommended by system input and do not invent something on your own.
        The final answer should contain: the brand name, price, rating, reviews.
        If customers have follow-up question, you should stick to the original recommended product, but you don't need to provide price or other characteristics of that product.
        """
    })

  # Add the user's initial message
  message_objects.append({"role": "user", "content": question})

  # Check if the top 3 products have been found
  if top_3_products is None or top_3_products.empty:
    top_3_products = find_top_3_products(question)

    # Add the top 3 product recommendations to message_objects as assistant messages
    for index, row in top_3_products.iterrows():
        brand_dict = {'role': "system", "content": f"This is a recommended product that you will be using in the answer: {row['combined']}"}
        message_objects.append(brand_dict)

  completion = client.chat.completions.create(
    messages=message_objects,
    model="gpt-3.5-turbo"
  )

  message_objects.append({"role": "assistant", "content": completion.choices[0].message.content})

  print(completion.choices[0].message.content)


  

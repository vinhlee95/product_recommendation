from openai import OpenAI, embeddings
import pandas as pd
import numpy as np

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Sample product database
product_data = [{
    "prod_id": 1,
    "prod": "moisturizer",
    "brand":"Aveeno",
    "description": "for dry skin",
    "price": 10,
    "rating": 4.5,
    "reviews": 100
},
{
    "prod_id": 2,
    "prod": "foundation",
    "brand":"Maybelline",
    "description": "medium coverage",
    "price": 20,
    "rating": 4.5,
    "reviews": 100
},
{
    "prod_id": 3,
    "prod": "moisturizer",
    "brand":"CeraVe",
    "description": "for dry skin",
    "price": 30,
    "rating": 4.5,
    "reviews": 100
},
{
    "prod_id": 4,
    "prod": "nail polish",
    "brand":"OPI",
    "description": "raspberry red",
    "price": 40,
    "rating": 4.5,
    "reviews": 100
},
{
    "prod_id": 5,
    "prod": "concealer",
    "brand":"chanel",
    "description": "medium coverage",
    "price": 60,
    "rating": 4.5,
    "reviews": 100
},
{
    "prod_id": 6,
    "prod": "moisturizer",
    "brand":"Ole Henkrisen",
    "description": "for oily skin",
    "price": 15,
    "rating": 4.5,
    "reviews": 100
},
{
    "prod_id": 7,
    "prod": "moisturizer",
    "brand":"CeraVe",
    "description": "for normal to dry skin",
    "price": 50,
    "rating": 4.5,
    "reviews": 100
},
{
    "prod_id": 8,
    "prod": "moisturizer",
    "brand":"First Aid Beauty",
    "description": "for dry skin",
    "price": 30,
    "rating": 4.5,
    "reviews": 100
},{
    "prod_id": 9,
    "prod": "makeup sponge",
    "brand":"Sephora",
    "description": "super-soft, exclusive, latex-free foam",
    "price": 45,
    "rating": 4.5,
    "reviews": 100
}]

# Add product data to dataframe
product_data_df = pd.DataFrame(product_data)
# print(product_data_df)

# Create column with combined data
product_data_df['combined'] = product_data_df.apply(lambda row: f"{row['brand']}, {row['prod']}, {row['description']}, {row['rating']}, {row['price']}, {row['reviews']}", axis=1)
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


  

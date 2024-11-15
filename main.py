from openai import OpenAI
from fetch_product_data import find_products_by_query

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
  

# Create a list to store message objects
message_objects = []
top_products = []

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
  if top_products is None or len(top_products) == 0:
    top_products = find_products_by_query(question=question, top_count=3)

    # Add the top 3 product recommendations to message_objects as assistant messages
    for product in top_products:
        brand_dict = {'role': "system", "content": f"This is 1 of the recommended product that you will be using in the answer: {product}"}
        message_objects.append(brand_dict)

  completion = client.chat.completions.create(
    messages=message_objects,
    model="gpt-3.5-turbo"
  )

  message_objects.append({"role": "assistant", "content": completion.choices[0].message.content})

  print(completion.choices[0].message.content)


  

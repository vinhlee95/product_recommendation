from openai import OpenAI
from fetch_product_data import find_products_by_query

from dotenv import load_dotenv
load_dotenv()

import re

client = OpenAI()
  

# Create a list to store message objects
message_objects = []
criteria = ""

# Have a set of questions to ask the user
questions = [
  {
    "step": 1,
    "type": "brand",
    "question": "What phone brand do you want to have?"
  },
  {
    "step": 2,
    "type": "price",
    "question": "What is your budget?"
  }
]

asked_question_indexes = []
min_price = 0
# Max price is infinity
max_price = float("inf")

def extract_budget_range(input_text: str):
  match = re.search(r'from (\d+) to (\d+)', input_text)
  if match:
    min_price = float(match.group(1))
    max_price = float(match.group(2))
    return min_price, max_price
  else:
      return None, None


def recommend_product() -> str:
  # Add a system message to set the assistant's behavior
  message_objects.append({
    "role": "system", 
    "content": """
      You're a chatbot helping customers with product recommendations. 
      You should only recommend the product that is recommended as assisant message and do not invent something on your own.
      The final answer should contain: the brand name, price, rating, reviews.
    """
  })

  # Add the user's initial message
  message_objects.append({"role": "user", "content": criteria})

  top_products = find_products_by_query(question=criteria, top_count=3)

  # Filter products based on price range
  if min_price != 0 or max_price != float("inf"):
    top_products = [product for product in top_products if min_price <= product["price"] <= max_price]

  for product in top_products:
    print(f"found product: {product["name"]}")

  top_product = top_products[0]

  # Add the top product recommendations to message_objects as assistant messages
  brand_dict = {
    "role": "assistant", 
    "content": f"This is 1 of the recommended product that you will be using in the answer: {top_product}"
  }
  message_objects.append(brand_dict)

  completion = client.chat.completions.create(
    messages=message_objects,
    model="gpt-3.5-turbo"
  )

  return completion.choices[0].message.content or "No recommendation for this. Sorry!"
  
while True:
  if len(asked_question_indexes) == len(questions):
    recommendation_text = recommend_product()
    print(f"Here is my recommendation: {recommendation_text}")
    break

  for question in questions:
    if question["step"] not in asked_question_indexes:
      asked_question_indexes.append(question["step"])
      
      # Ask the question
      print(question["question"])

      if question["type"] == "price":
        min_price, max_price = extract_budget_range(input(">> "))
        break
      
      criteria += input(">> ")
      break
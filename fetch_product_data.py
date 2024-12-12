"""
Fetch product data and their embeddings from Pinecone
"""
from pinecone.grpc import PineconeGRPC as Pinecone
import os
from openai import embeddings
import numpy as np
from typing import TypedDict

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "products"
product_index = pc.Index(index_name)

class Criteria(TypedDict):
  brand: str
  min_price: float
  max_price: float

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Create embeddings
def get_embedding(text):
  response = embeddings.create(
    model="text-embedding-3-small",
    input=[text],
  )

  return response.data[0].embedding

# TODO: better typing from criteria
def find_products_by_query(criteria: dict, top_count: int = 1) -> list[dict]:
  print(f"Searching for products based on question: {criteria}")
  vector = get_embedding(criteria.get("brand"))
  results = product_index.query(
    vector=vector,
    filter={
      "brand": criteria.get("brand", "")
    },
    top_k=top_count,
    include_values=True,
    include_metadata=True
  )

  print(f"Found {len(results['matches'])} matching products")
  
  return [item['metadata'] for item in results['matches']]

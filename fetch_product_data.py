"""
Fetch product data and their embeddings from Pinecone
"""
from pinecone.grpc import PineconeGRPC as Pinecone
import os
from openai import embeddings
import numpy as np

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "products"
product_index = pc.Index(index_name)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Create embeddings
def get_embedding(text):
  response = embeddings.create(
    model="text-embedding-3-small",
    input=[text],
  )

  return response.data[0].embedding

def find_products_by_query(question: str, top_count: int = 1, relevance_threshold: float = 0.4) -> list[dict]:
  print(f"Searching for products based on question: {question}")
  vector = get_embedding(question)
  results = product_index.query(
    vector=vector,
    top_k=top_count,
    include_values=True,
    include_metadata=True
  )

  print(f"Found {len(results['matches'])} matching products")

  # Filter results based on relevance threshold
  # relevant_products = [
  #   item['metadata'] for item in results['matches']
  #   if cosine_similarity(vector, item['values']) >= relevance_threshold
  # ]

  return [item['metadata'] for item in results['matches']]
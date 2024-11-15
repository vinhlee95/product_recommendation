"""
Fetch product data and their embeddings from Pinecone
"""
from pinecone.grpc import PineconeGRPC as Pinecone
import os
from openai import embeddings

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "products"
product_index = pc.Index(index_name)

# Create embeddings
def get_embedding(text):
  response = embeddings.create(
    model="text-embedding-3-small",
    input=[text],
  )

  return response.data[0].embedding

def find_products_by_query(question: str, top_count: int = 1) -> list[dict]:
  vector = get_embedding(question)
  results = product_index.query(
    vector=vector,
    top_k=top_count,
    include_values=True,
    include_metadata=True
  )
  # print(results.get('matches')[0].get('metadata'))

  # Return metadata of the top products
  return [item.get('metadata') for item in results.get('matches')]
from pinecone.grpc import PineconeGRPC as Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "products"

print(pc.list_indexes())

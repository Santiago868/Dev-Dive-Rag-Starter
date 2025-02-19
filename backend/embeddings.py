import os
import pickle
from langchain_community.document_loaders.csv_loader import CSVLoader
import ollama

# Set the path for the CSV file
file_path = './data/knowledge-base.csv' 

# Load documents from the CSV file
loader = CSVLoader(file_path=file_path)
docs = loader.load()

# Compute an embedding for a given text using Ollama's model
def compute_embedding(text: str) -> list:
    """
    Compute an embedding for the provided text.
    """
    return ollama.embeddings(model='nomic-embed-text', prompt=text)

# List to store embeddings for each document
embeddings_list = []

# Loop through each document and compute its embedding Add code here.


# Bundle the documents and their embeddings into a dictionary
precomputed_data = {"docs": docs, "embeddings": embeddings_list}

# Save the data to a pickle file for later use
with open("precomputed_embeddings.pkl", "wb") as f:
    pickle.dump(precomputed_data, f)

print("Precomputation complete. Embeddings saved to precomputed_embeddings.pkl")

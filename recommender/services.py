import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import models
from sentence_transformers import SentenceTransformer
import pickle

# Load and prepare data
def load_data(data):
    return pd.read_csv(data)

def prepare_data(df):
    docx = df['course_title'].tolist()
    payload = df[['course_id', 'course_title', 'subject', 'price']].to_dict('records')
    return docx, payload

def save_vector(vectors, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(vectors, f)

def load_vectors(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def initialize_qdrant(vector_db_path, collection_name, vector_size):
    client = QdrantClient(path=vector_db_path)
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )
    return client

# Encode text using SentenceTransformer
def vectorize_texts(model, texts):
    return model.encode(texts, show_progress_bar=True)

# Upload data to Qdrant
def upload_to_qdrant(client, collection_name, vectors, payload):
    client.upload_collection(collection_name=collection_name, vectors=vectors, payload=payload, ids=None, batch_size=256)

# Search the Qdrant collection
def search_qdrant(client, collection_name, query_vector, limit):
    return client.search(collection_name=collection_name, query_vector=query_vector, limit=limit)
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# .env 로드 (parent dir)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

api_key = os.getenv('GEMINI_API_KEY')
print(f"Using API Key starting with: {api_key[:10]}...")

# 1. gemini-embedding-001 테스트
print("\nTesting models/gemini-embedding-001...")
try:
    embeddings_001 = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001', google_api_key=api_key)
    vector_001 = embeddings_001.embed_query('test')
    print(f"Dimension (001): {len(vector_001)}")
except Exception as e:
    print(f"Error (001): {e}")

# 2. gemini-embedding-2-preview 테스트
print("\nTesting models/gemini-embedding-2-preview...")
try:
    embeddings_2 = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-2-preview', google_api_key=api_key)
    vector_2 = embeddings_2.embed_query('test')
    print(f"Dimension (2-preview): {len(vector_2)}")
except Exception as e:
    print(f"Error (2-preview): {e}")

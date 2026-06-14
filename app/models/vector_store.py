from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import Config

class VectorStore:
    def __init__(self, path):
        """
        Initialize OpenAI Embeddings and configure the local ChromaDB vector store instance.
        """
        # Securely pass the OpenAI API key fetched from the central configuration
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        
        # Kept as 'self.db' to maintain direct compatibility with the modern LCEL LLMService pipeline
        self.db = Chroma(
            persist_directory=path,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents):
        """
        Ingest, tokenize, and commit a list of document chunks into the vector store database.
        """
        self.db.add_documents(documents)
        
    def similarity_search(self, query, k=4):
        """
        Perform a semantic similarity search across the vector index to retrieve the top K context records.
        """
        return self.db.similarity_search(query, k=k)
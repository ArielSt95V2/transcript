import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Union
import openai
from pinecone import Pinecone, ServerlessSpec
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 
pinecone_api_key = os.getenv("PINECONE_API_KEY")

class EmbeddingUtility:
    """
    A utility class for handling text embeddings and vector operations.
    Supports OpenAI embeddings and Pinecone vector database operations.
    """
    
    def __init__(self, 
                 openai_api_key: Optional[str] = openai_api_key,
                 pinecone_api_key: Optional[str] = pinecone_api_key,
                 embedding_model: str = "text-embedding-3-large",
                 index_name: str = "learning-assistant",
                 dimension: int = 3072):
        """
        Initialize the EmbeddingUtility class.
        
        Args:
            openai_api_key: OpenAI API key (defaults to environment variable)
            pinecone_api_key: Pinecone API key (defaults to environment variable)
            embedding_model: OpenAI embedding model to use
            index_name: Name of the Pinecone index
            dimension: Dimension of the embedding vectors
        """
        self.openai_api_key = openai_api_key
        self.pinecone_api_key = pinecone_api_key
        self.embedding_model = embedding_model
        self.index_name = index_name
        self.dimension = dimension
        
        # Initialize OpenAI client
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.openai_client = openai
        else:
            logger.warning("OpenAI API key not found. Embedding functionality will be limited.")
            self.openai_client = None
        
        # Initialize Pinecone client
        if self.pinecone_api_key:
            self.pc = Pinecone(api_key=self.pinecone_api_key)
            self._setup_index()
        else:
            logger.warning("Pinecone API key not found. Vector database functionality will be limited.")
            self.pc = None
            self.index = None
    
    def _setup_index(self):
        """Set up the Pinecone index if it doesn't exist."""
        try:
            if not self.pc.has_index(self.index_name):
                logger.info(f"Creating Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Failed to setup Pinecone index: {e}")
            self.index = None
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Please provide a valid API key.")
        
        try:
            response = self.openai_client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            embeddings = [data.embedding for data in response.data]
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    def embed_single_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string to embed
            
        Returns:
            Embedding vector
        """
        return self.embed_texts([text])[0]
    
    def create_vectors(self, data: List[Dict[str, Any]], 
                      text_field: str = "text", 
                      id_field: str = "id") -> List[Dict[str, Any]]:
        """
        Create vector objects for Pinecone from data with embeddings.
        
        Args:
            data: List of dictionaries containing text and metadata
            text_field: Field name containing the text to embed
            id_field: Field name containing the unique identifier
            
        Returns:
            List of vector objects for Pinecone
        """
        texts = [item[text_field] for item in data]
        embeddings = self.embed_texts(texts)
        
        vectors = []
        for item, embedding in zip(data, embeddings):
            vector = {
                "id": item[id_field],
                "values": embedding,
                "metadata": {k: v for k, v in item.items() if k != text_field}
            }
            # Add text to metadata for reference
            vector["metadata"][text_field] = item[text_field]
            vectors.append(vector)
        
        return vectors
    
    def upsert_vectors(self, vectors: List[Dict[str, Any]], 
                      namespace: str = "default") -> bool:
        """
        Upsert vectors to Pinecone index.
        
        Args:
            vectors: List of vector objects to upsert
            namespace: Pinecone namespace
            
        Returns:
            True if successful, False otherwise
        """
        if not self.index:
            raise ValueError("Pinecone index not initialized. Please provide a valid API key.")
        
        try:
            self.index.upsert(vectors=vectors, namespace=namespace)
            logger.info(f"Upserted {len(vectors)} vectors to namespace '{namespace}'")
            return True
        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            return False
    
    def query_vectors(self, query_text: str, 
                     top_k: int = 5, 
                     namespace: str = "default",
                     include_metadata: bool = True,
                     include_values: bool = False) -> Dict[str, Any]:
        """
        Query the vector database for similar vectors.
        
        Args:
            query_text: Text to query for
            top_k: Number of top results to return
            namespace: Pinecone namespace to query
            include_metadata: Whether to include metadata in results
            include_values: Whether to include vector values in results
            
        Returns:
            Query results from Pinecone
        """
        if not self.index:
            raise ValueError("Pinecone index not initialized. Please provide a valid API key.")
        
        try:
            query_embedding = self.embed_single_text(query_text)
            results = self.index.query(
                namespace=namespace,
                vector=query_embedding,
                top_k=top_k,
                include_values=include_values,
                include_metadata=include_metadata
            )
            logger.info(f"Query returned {len(results.matches)} results")
            return results
        except Exception as e:
            logger.error(f"Failed to query vectors: {e}")
            raise
    
    def batch_process_and_store(self, data: List[Dict[str, Any]], 
                               text_field: str = "text",
                               id_field: str = "id",
                               namespace: str = "default") -> bool:
        """
        Process data, generate embeddings, and store in Pinecone in one operation.
        
        Args:
            data: List of dictionaries containing text and metadata
            text_field: Field name containing the text to embed
            id_field: Field name containing the unique identifier
            namespace: Pinecone namespace to store vectors
            
        Returns:
            True if successful, False otherwise
        """
        try:
            vectors = self.create_vectors(data, text_field, id_field)
            return self.upsert_vectors(vectors, namespace)
        except Exception as e:
            logger.error(f"Failed to batch process and store: {e}")
            return False
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Pinecone models.
        Returns:
            List of available model names
        """
        if not self.pc:
            raise ValueError("Pinecone client not initialized. Please provide a valid API key.")
        
        try:
            models = self.pc.inference.list_models()
            return [model.name for model in models]
        except Exception as e:
            logger.error(f"Failed to get available models: {e}")
            return []
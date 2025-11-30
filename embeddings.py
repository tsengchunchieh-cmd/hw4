"""
EmbeddingGemma Module
Implements custom embeddings using Google's EmbeddingGemma-300m model
with proper prefix formatting for documents and queries.
"""

from langchain.embeddings import HuggingFaceEmbeddings


class EmbeddingGemmaEmbeddings(HuggingFaceEmbeddings):
    """
    Custom embeddings class for Google's EmbeddingGemma-300m model.
    
    Follows Google's recommended prefix format:
    - Documents: 'title: none | text: ...'
    - Queries: 'task: search result | query: ...'
    
    This ensures better semantic alignment between document and query embeddings.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize EmbeddingGemmaEmbeddings with the google/embeddinggemma-300m model.
        
        Args:
            **kwargs: Additional arguments passed to HuggingFaceEmbeddings
        """
        super().__init__(
            model_name="google/embeddinggemma-300m",
            encode_kwargs={"normalize_embeddings": True},
            **kwargs
        )

    def embed_documents(self, texts):
        """
        Embed a list of documents with the proper document prefix format.
        
        Args:
            texts (list): List of document texts to embed
            
        Returns:
            list: List of embeddings for the documents
        """
        # Apply document prefix format as recommended by Google
        prefixed_texts = [f'title: none | text: {text}' for text in texts]
        return super().embed_documents(prefixed_texts)

    def embed_query(self, text):
        """
        Embed a query with the proper query prefix format.
        
        Args:
            text (str): Query text to embed
            
        Returns:
            list: Embedding vector for the query
        """
        # Apply query prefix format as recommended by Google
        prefixed_text = f'task: search result | query: {text}'
        return super().embed_query(prefixed_text)

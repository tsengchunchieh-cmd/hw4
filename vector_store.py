"""
Vector Store Module
Handles document loading, text splitting, and FAISS vector database creation.
"""

import os
import shutil
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader, 
    UnstructuredWordDocumentLoader, 
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from embeddings import EmbeddingGemmaEmbeddings


def create_vector_store(uploaded_files, hf_token: str, temp_dir: str = "uploaded_docs"):
    """
    Create a FAISS vector store from uploaded documents.
    
    Supports .txt, .pdf, and .docx file formats. Documents are split into
    chunks using RecursiveCharacterTextSplitter and then embedded using
    EmbeddingGemma with Google's embedding model.
    
    Args:
        uploaded_files (list): List of uploaded file objects from Streamlit
        hf_token (str): HuggingFace token for model access
        temp_dir (str): Temporary directory for storing uploaded files
        
    Returns:
        FAISS: Vector store object, or None if no documents were processed
        
    Raises:
        ValueError: If no documents can be loaded from the uploaded files
    """
    
    # Create temporary directory for uploaded files
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Save uploaded files to temporary directory
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)
        
        # Load documents from files
        documents = []
        
        for file_path in file_paths:
            file_extension = Path(file_path).suffix.lower()
            
            try:
                if file_extension == ".pdf":
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                    
                elif file_extension == ".docx":
                    loader = UnstructuredWordDocumentLoader(file_path)
                    documents.extend(loader.load())
                    
                elif file_extension == ".txt":
                    loader = TextLoader(file_path, encoding="utf-8")
                    documents.extend(loader.load())
                    
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
                continue
        
        if not documents:
            raise ValueError("未能從上傳的文件中提取任何文本。請確保文件格式正確。")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        
        split_documents = text_splitter.split_documents(documents)
        
        if not split_documents:
            raise ValueError("文本分割後沒有生成有效的文檔塊。")
        
        # Initialize embeddings model
        embeddings = EmbeddingGemmaEmbeddings(
            model_kwargs={"device": "cpu"},
            show_progress=True
        )
        
        # Create FAISS vector store
        vectorstore = FAISS.from_documents(
            documents=split_documents,
            embedding=embeddings
        )
        
        return vectorstore
        
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def save_vectorstore(vectorstore, save_path: str = "faiss_db"):
    """
    Save the FAISS vector store to disk.
    
    Args:
        vectorstore (FAISS): Vector store to save
        save_path (str): Path where to save the vector store
    """
    vectorstore.save_local(save_path)
    print(f"向量資料庫已保存到: {save_path}")


def load_vectorstore(load_path: str = "faiss_db"):
    """
    Load a FAISS vector store from disk.
    
    Args:
        load_path (str): Path to the saved vector store
        
    Returns:
        FAISS: Loaded vector store
    """
    embeddings = EmbeddingGemmaEmbeddings(
        model_kwargs={"device": "cpu"},
        show_progress=False
    )
    vectorstore = FAISS.load_local(
        load_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

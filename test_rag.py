"""
Test Script for RAG Application
Validates the core functionality without requiring a full Streamlit interface.
"""

import sys
import os
from pathlib import Path


def test_embeddings():
    """Test EmbeddingGemma functionality."""
    print("\n🧪 測試 EmbeddingGemma...\n")
    
    try:
        from embeddings import EmbeddingGemmaEmbeddings
        
        print("初始化 EmbeddingGemmaEmbeddings...")
        embeddings = EmbeddingGemmaEmbeddings(
            model_kwargs={"device": "cpu"},
            show_progress=False
        )
        
        # Test document embedding
        test_docs = ["這是測試文件 1", "這是測試文件 2"]
        print(f"嵌入 {len(test_docs)} 個文件...")
        doc_embeddings = embeddings.embed_documents(test_docs)
        
        print(f"✅ 文件嵌入成功 - 維度: {len(doc_embeddings[0])}")
        
        # Test query embedding
        test_query = "這是測試查詢"
        print(f"嵌入查詢: '{test_query}'...")
        query_embedding = embeddings.embed_query(test_query)
        
        print(f"✅ 查詢嵌入成功 - 維度: {len(query_embedding)}")
        
        return True
    
    except Exception as e:
        print(f"❌ EmbeddingGemma 測試失敗: {str(e)}")
        return False


def test_rag_chain():
    """Test RAG chain structure."""
    print("\n🧪 測試 RAG 鏈...\n")
    
    try:
        from rag_chain import RAG_PROMPT_TEMPLATE, query_rag
        
        print("檢查 RAG 提示詞模板...")
        assert "{context}" in RAG_PROMPT_TEMPLATE
        assert "{question}" in RAG_PROMPT_TEMPLATE
        print("✅ RAG 提示詞模板有效")
        
        print("檢查 query_rag 函數...")
        assert callable(query_rag)
        print("✅ query_rag 函數可用")
        
        return True
    
    except Exception as e:
        print(f"❌ RAG 鏈測試失敗: {str(e)}")
        return False


def test_vector_store():
    """Test vector store functions."""
    print("\n🧪 測試向量資料庫模組...\n")
    
    try:
        from vector_store import create_vector_store, save_vectorstore, load_vectorstore
        
        print("檢查向量資料庫函數...")
        assert callable(create_vector_store)
        assert callable(save_vectorstore)
        assert callable(load_vectorstore)
        print("✅ 所有向量資料庫函數可用")
        
        return True
    
    except Exception as e:
        print(f"❌ 向量資料庫模組測試失敗: {str(e)}")
        return False


def test_config():
    """Test configuration module."""
    print("\n🧪 測試配置模組...\n")
    
    try:
        from config import (
            EMBEDDING_MODEL_NAME,
            LLM_MODEL_NAME,
            CHUNK_SIZE,
            RETRIEVER_K,
            get_config_summary
        )
        
        print(f"嵌入模型: {EMBEDDING_MODEL_NAME}")
        print(f"LLM 模型: {LLM_MODEL_NAME}")
        print(f"文本塊大小: {CHUNK_SIZE}")
        print(f"檢索 K 值: {RETRIEVER_K}")
        
        config_summary = get_config_summary()
        print(f"\n✅ 配置載入成功 ({len(config_summary)} 個參數)")
        
        return True
    
    except Exception as e:
        print(f"❌ 配置模組測試失敗: {str(e)}")
        return False


def test_file_structure():
    """Test project file structure."""
    print("\n🧪 測試項目文件結構...\n")
    
    required_files = [
        "streamlit_app.py",
        "embeddings.py",
        "rag_chain.py",
        "vector_store.py",
        "config.py",
        "requirements.txt",
        "README.md",
        ".env.example",
    ]
    
    missing_files = []
    
    for file_name in required_files:
        if os.path.exists(file_name):
            file_size = os.path.getsize(file_name)
            print(f"✅ {file_name} ({file_size} bytes)")
        else:
            print(f"❌ {file_name}")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n⚠️ 缺少文件: {', '.join(missing_files)}")
        return False
    
    return True


def test_api_keys():
    """Test if API keys are configured."""
    print("\n🧪 檢查 API 密鑰配置...\n")
    
    try:
        from config import validate_api_keys, HUGGINGFACE_TOKEN, GOOGLE_API_KEY
        
        is_valid, missing_keys = validate_api_keys()
        
        if HUGGINGFACE_TOKEN:
            print("✅ HuggingFace Token 已配置")
        else:
            print("⚠️ HuggingFace Token 未配置 (需要用於運行應用)")
        
        if GOOGLE_API_KEY:
            print("✅ Google API Key 已配置")
        else:
            print("⚠️ Google API Key 未配置 (需要用於運行應用)")
        
        if missing_keys:
            print(f"\n⚠️ 缺少以下 API Key: {', '.join(missing_keys)}")
            print("請編輯 .env 文件進行配置")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ API 密鑰檢查失敗: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("📚 RAG 文件問答系統 - 測試套件")
    print("=" * 60)
    
    tests = [
        ("文件結構", test_file_structure),
        ("配置模組", test_config),
        ("EmbeddingGemma", test_embeddings),
        ("RAG 鏈", test_rag_chain),
        ("向量資料庫", test_vector_store),
        ("API 密鑰", test_api_keys),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} 測試發生錯誤: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 測試結果摘要")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{status}: {test_name}")
    
    print(f"\n總計: {passed}/{total} 通過")
    
    if passed == total:
        print("\n✅ 所有測試通過！系統已就緒。")
        print("\n運行應用: streamlit run streamlit_app.py")
        return True
    else:
        print(f"\n⚠️ {total - passed} 個測試失敗")
        print("請檢查上述錯誤信息")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

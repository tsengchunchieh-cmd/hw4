"""
Setup Helper Script
Helps with initial configuration and testing of the RAG application.
"""

import os
import sys
from pathlib import Path


def check_dependencies():
    """Check if all required packages are installed."""
    print("🔍 檢查依賴套件...\n")
    
    required_packages = [
        "streamlit",
        "langchain",
        "langchain_community",
        "langchain_google_genai",
        "sentence_transformers",
        "faiss",
        "pypdf",
        "python_docx",
        "unstructured",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 缺少以下套件: {', '.join(missing_packages)}")
        print("\n請運行以下命令進行安裝:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有依賴套件已安裝！")
        return True


def create_env_file():
    """Create .env file from template."""
    print("\n📝 設置環境變數...\n")
    
    if os.path.exists(".env"):
        print("✅ .env 文件已存在")
        return
    
    if os.path.exists(".env.example"):
        print("📋 從 .env.example 創建 .env...")
        with open(".env.example", "r") as src:
            content = src.read()
        
        with open(".env", "w") as dst:
            dst.write(content)
        
        print("✅ .env 文件已創建")
        print("\n請編輯 .env 文件並添加您的 API Key:")
        print("  1. HuggingFace Token")
        print("  2. Google API Key")
    else:
        print("⚠️ .env.example 文件未找到")


def test_imports():
    """Test if all core modules can be imported."""
    print("\n🧪 測試模組導入...\n")
    
    modules_to_test = [
        ("embeddings", "EmbeddingGemmaEmbeddings"),
        ("rag_chain", "query_rag"),
        ("vector_store", "create_vector_store"),
    ]
    
    failed = False
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                print(f"✅ {module_name}.{class_name}")
            else:
                print(f"❌ {module_name}.{class_name} (找不到)")
                failed = True
        except ImportError as e:
            print(f"❌ {module_name} - {str(e)}")
            failed = True
    
    if not failed:
        print("\n✅ 所有模組導入成功！")
    else:
        print("\n⚠️ 某些模組無法導入")
        return False
    
    return True


def create_directories():
    """Create necessary directories."""
    print("\n📁 創建必要的目錄...\n")
    
    directories = [
        "uploaded_docs",
        "faiss_db",
        "logs",
    ]
    
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ {dir_name}")


def main():
    """Run all setup checks and configurations."""
    print("=" * 50)
    print("📚 RAG 文件問答系統 - 設置助手")
    print("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ 請先安裝所有依賴套件")
        return False
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Create .env file
    create_env_file()
    
    # Step 4: Test imports
    if not test_imports():
        print("\n❌ 模組導入失敗")
        return False
    
    # Step 5: Final message
    print("\n" + "=" * 50)
    print("✅ 設置完成！")
    print("=" * 50)
    
    print("\n📋 接下來的步驟:")
    print("1. 編輯 .env 文件並添加您的 API Key")
    print("2. 運行應用: streamlit run streamlit_app.py")
    print("3. 在瀏覽器中打開 http://localhost:8501")
    
    print("\n📚 更多信息請查看 README.md")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

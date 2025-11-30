"""
Streamlit RAG Document QA System
A complete Retrieval-Augmented Generation (RAG) application for document-based question answering.

Features:
- Upload and process .pdf, .txt, and .docx files
- Create vector databases using Google's EmbeddingGemma-300m model
- Ask questions and receive answers based on document content
- View retrieved document chunks for transparency
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from embeddings import EmbeddingGemmaEmbeddings
from rag_chain import query_rag
from vector_store import create_vector_store, save_vectorstore, load_vectorstore


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="📚 RAG 文件問答系統",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 RAG 文件問答系統")
st.markdown("""
基於向量資料庫的文件問答系統，使用 Google 的 EmbeddingGemma 模型和 Gemini 2.5 Flash。
""")


# ============================================================================
# Sidebar Configuration
# ============================================================================

with st.sidebar:
    st.header("⚙️ 配置")
    
    st.markdown("### API 密鑰")
    hf_token = st.text_input(
        "HuggingFace Token (用於 EmbeddingGemma)",
        type="password",
        help="從 HuggingFace 取得: https://huggingface.co/settings/tokens"
    )
    
    llm_api_key = st.text_input(
        "Google API Key (用於 Gemini 2.5 Flash)",
        type="password",
        help="從 Google AI Studio 取得: https://aistudio.google.com/app/apikey"
    )
    
    st.markdown("### 資料庫選項")
    db_mode = st.radio(
        "選擇資料庫模式：",
        options=["建立新資料庫", "載入現有資料庫"],
        help="建立新資料庫或從本地載入已保存的資料庫"
    )


# ============================================================================
# Initialize Session State
# ============================================================================

if 'vectorstore' not in st.session_state:
    st.session_state['vectorstore'] = None

if 'db_created' not in st.session_state:
    st.session_state['db_created'] = False


# ============================================================================
# Main Application Layout
# ============================================================================

# Tab 1: Create Vector Store
tab1, tab2 = st.tabs(["📤 建立資料庫", "❓ 提問"])

with tab1:
    st.header("上傳文件並建立向量資料庫")
    
    if db_mode == "建立新資料庫":
        st.markdown("""
        ### 支持的文件格式
        - **PDF** (.pdf)
        - **Word 文件** (.docx)
        - **純文字** (.txt)
        """)
        
        uploaded_files = st.file_uploader(
            "上傳您的文件",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            help="可同時上傳多個文件"
        )
        
        if uploaded_files:
            st.markdown(f"**已選擇 {len(uploaded_files)} 個文件：**")
            for file in uploaded_files:
                st.write(f"- {file.name} ({file.size} bytes)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔨 建立向量資料庫", use_container_width=True, type="primary"):
                if not uploaded_files:
                    st.error("請先選擇至少一個文件。")
                elif not hf_token:
                    st.error("請輸入 HuggingFace Token。")
                else:
                    with st.spinner("正在處理文件並建立資料庫..."):
                        try:
                            st.session_state['vectorstore'] = create_vector_store(
                                uploaded_files,
                                hf_token
                            )
                            st.session_state['db_created'] = True
                            st.success("✅ 向量資料庫建立成功！")
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ 建立資料庫時出錯：{str(e)}")
        
        with col2:
            if st.button("💾 保存資料庫", use_container_width=True):
                if st.session_state['vectorstore'] is not None:
                    try:
                        save_vectorstore(st.session_state['vectorstore'], "faiss_db")
                        st.success("✅ 資料庫已保存！")
                    except Exception as e:
                        st.error(f"❌ 保存資料庫時出錯：{str(e)}")
                else:
                    st.warning("⚠️ 請先建立向量資料庫。")
    
    else:  # Load existing database
        st.markdown("### 載入已保存的向量資料庫")
        
        if os.path.exists("faiss_db"):
            if st.button("📂 載入 faiss_db 資料庫", use_container_width=True, type="primary"):
                with st.spinner("正在載入資料庫..."):
                    try:
                        st.session_state['vectorstore'] = load_vectorstore("faiss_db")
                        st.session_state['db_created'] = True
                        st.success("✅ 資料庫載入成功！")
                    except Exception as e:
                        st.error(f"❌ 載入資料庫時出錯：{str(e)}")
        else:
            st.info("ℹ️ 未找到已保存的資料庫。請先建立新資料庫。")
    
    # Display database status
    st.markdown("---")
    st.markdown("### 資料庫狀態")
    if st.session_state['db_created'] and st.session_state['vectorstore'] is not None:
        st.success("✅ 資料庫已準備好進行查詢")
    else:
        st.info("ℹ️ 資料庫未準備好，請先建立或載入。")


# Tab 2: Question Answering
with tab2:
    st.header("提問與回答")
    
    if st.session_state['vectorstore'] is not None:
        query = st.text_area(
            "請輸入您的問題：",
            height=100,
            placeholder="例如：這份文件主要討論了什麼？",
            help="輸入任何與上傳文件相關的問題"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit_button = st.button(
                "🚀 取得答案",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            clear_button = st.button(
                "🗑️ 清空",
                use_container_width=True
            )
        
        if clear_button:
            st.rerun()
        
        if submit_button and query.strip():
            if not llm_api_key:
                st.error("❌ 請在側邊欄輸入 Google API Key。")
            else:
                with st.spinner("正在檢索並生成答案..."):
                    try:
                        vectorstore = st.session_state['vectorstore']
                        
                        # Execute RAG query
                        final_answer, retrieved_docs = query_rag(
                            vectorstore,
                            query,
                            llm_api_key
                        )
                        
                        # Display final answer
                        st.markdown("---")
                        st.subheader("🤖 最終答案")
                        st.success(final_answer)
                        
                        # Display retrieved context
                        st.subheader("📚 檢索到的文件片段 (Context)")
                        
                        if retrieved_docs:
                            st.markdown(f"**找到 {len(retrieved_docs)} 個相關片段：**")
                            
                            for i, doc in enumerate(retrieved_docs, 1):
                                source_info = doc.metadata.get('source', '未知文件')
                                
                                with st.expander(
                                    f"📄 片段 {i} (來自: {source_info})",
                                    expanded=(i == 1)
                                ):
                                    st.markdown(doc.page_content)
                        else:
                            st.info("ℹ️ 未檢索到相關文件片段。")
                    
                    except Exception as e:
                        st.error(f"❌ 執行查詢時出錯：{str(e)}")
        
        elif submit_button:
            st.warning("⚠️ 請輸入問題。")
    
    else:
        st.info(
            "ℹ️ 請先在「建立資料庫」標籤中建立或載入向量資料庫。"
        )


# ============================================================================
# Footer
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>
        🚀 由 Streamlit、LangChain、和 Google Gemini 驅動 | 
        📚 使用 EmbeddingGemma-300m 進行向量化
    </small>
</div>
""", unsafe_allow_html=True)

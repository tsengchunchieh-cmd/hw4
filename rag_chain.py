"""
RAG Query Module
Implements the RAG (Retrieval-Augmented Generation) query functionality
using Gemini 2.5 Flash and LangChain.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


# Define RAG prompt template in Traditional Chinese
RAG_PROMPT_TEMPLATE = """
作為一個樂於助人的問答機器人，請根據提供的上下文 (Context) 來回答問題 (Question)。
如果你無法從上下文中找到答案，請誠實地回答「根據提供的資料，我無法回答這個問題。」
請使用繁體中文回答。

Context:
{context}

Question:
{question}
"""


def query_rag(vectorstore, query: str, llm_api_key: str):
    """
    Execute the RAG query pipeline: retrieve relevant documents, 
    format context, and generate an answer using Gemini 2.5 Flash.
    
    Args:
        vectorstore: FAISS vector store containing embedded documents
        query (str): User's question
        llm_api_key (str): Google API key for Gemini access
        
    Returns:
        tuple: (final_answer, retrieved_docs)
            - final_answer (str): Generated answer from the LLM
            - retrieved_docs (list): Retrieved document chunks with metadata
    """
    if not llm_api_key:
        return "錯誤：未提供 Google API Key。", []

    # Initialize Gemini 2.5 Flash LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        google_api_key=llm_api_key
    )

    # Set up retriever with k=4 to fetch top 4 most relevant documents
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    def format_docs(docs):
        """Format retrieved documents into a single context string."""
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    # Build the RAG chain:
    # 1. Retrieve documents matching the query
    # 2. Format them into context
    # 3. Create prompt with context and question
    # 4. Pass through LLM
    # 5. Parse output to string
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        | llm
        | StrOutputParser()
    )

    # Execute the RAG chain to get the final answer
    final_answer = rag_chain.invoke(query)
    
    # Separately invoke retriever to get documents for display
    retrieved_docs = retriever.invoke(query)

    return final_answer, retrieved_docs

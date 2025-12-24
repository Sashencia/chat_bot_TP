# retrieval/retriever.py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_style_retriever():
    # Загружаем гайд
    loader = TextLoader("retrieval/style_guide.md", encoding="utf-8")
    documents = loader.load()
    
    # Делим
    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)
    
    # Эмбеддинги — локальные, без API
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    return vectorstore.as_retriever(search_kwargs={"k": 1})
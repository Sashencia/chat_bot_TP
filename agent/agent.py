from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_simple_chain():
    llm = ChatOllama(
        model="qwen2.5:1.5b-instruct-q4_K_M",
        temperature=0.7,
        num_ctx=4096
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_message}"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}")
    ])
    return prompt | llm | StrOutputParser()
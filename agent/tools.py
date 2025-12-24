# agent/tools.py
# def explain_style_sync() -> str:
#     try:
#         with open("retrieval/style_guide.md", "r", encoding="utf-8") as f:
#             return f.read()
#     except Exception:
#         return "📘 Формальный стиль — на «вы», без эмодзи, строго.\nНеформальный — на «ты», с эмодзи, дружелюбно."

from retrieval.retriever import create_style_retriever

def explain_style_sync() -> str:
    try:
        retriever = create_style_retriever()
        docs = retriever.invoke("что такое формальный и неформальный стиль")
        if docs:
            return docs[0].page_content
        else:
            return "Не удалось найти информацию о стилях."
    except Exception as e:
        return f"Ошибка поиска: {str(e)}"

def summarize_history(history) -> str:
    msgs = history.messages[-6:]  # последние 3 пары
    summary = "Кратко о чём мы говорили:\n"
    for i, msg in enumerate(msgs[-4:], 1):  # последние 4 сообщения
        role = "👤" if msg.type == "human" else "🤖"
        summary += f"{role} {msg.content[:50]}...\n"
    return summary or "Диалог только начался 😊"
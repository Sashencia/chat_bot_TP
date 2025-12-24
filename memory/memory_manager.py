# memory/memory_manager.py
from typing import Dict
from langchain_community.chat_message_histories import ChatMessageHistory

class MemoryManager:
    def __init__(self):
        self.histories: Dict[int, ChatMessageHistory] = {}
        self.styles: Dict[int, str] = {}

    def get_history(self, user_id: int):
        if user_id not in self.histories:
            self.histories[user_id] = ChatMessageHistory()
            self.styles[user_id] = "casual"
        return self.histories[user_id]

    def get_style(self, user_id: int) -> str:
        return self.styles.get(user_id, "casual")

    def set_style(self, user_id: int, style: str):
        self.styles[user_id] = style

    def clear_memory(self, user_id: int):
        if user_id in self.histories:
            self.histories[user_id].clear()
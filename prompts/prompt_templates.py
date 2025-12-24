# prompts/prompt_templates.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_system_prompt(style_name: str) -> str:
    return {
        "formal": (
            "Вы — вежливый и профессиональный ассистент. "
            "Обращайтесь на «вы», используйте полные предложения, "
            "избегайте эмодзи и сленга. Будьте точны и уважительны."
        ),
        "casual": (
            "Ты — дружелюбный и тёплый собеседник. "
            "Обращайся на «ты», используй эмодзи (например, 😊, 🌟), "
            "разговорные фразы и лёгкую иронию. Поддерживай эмоциональную связь."
        )
    }.get(style_name, "casual")

def create_chat_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "{system_message}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
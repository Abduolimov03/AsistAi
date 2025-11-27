from collections import defaultdict

# user_id bo'yicha chat tarixi
user_history = defaultdict(list)

def save_history(user_id: int, role: str, content: str):
    """
    user_id bo'yicha role (user/assistant) va content saqlaydi
    """
    user_history[user_id].append({"role": role, "content": content})

def get_history(user_id: int, limit=10):
    """
    Oxirgi 'limit' ta xabarni qaytaradi
    """
    return user_history[user_id][-limit:]

def clear_history(user_id: int):
    """
    Foydalanuvchi tarixini tozalaydi
    """
    user_history[user_id] = []

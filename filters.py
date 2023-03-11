
def user_filter(user):
    return f'{user.first_name} {user.last_name if user.last_name else ""}'


def chat_filter(chat):
    return chat.title


def filter_(obj) -> str:
    return chat_filter(obj) if hasattr(obj, "title") else user_filter(obj)

async def check(chat_member):
    return chat_member['status'] == 'administrator' or chat_member['status'] == 'creator'

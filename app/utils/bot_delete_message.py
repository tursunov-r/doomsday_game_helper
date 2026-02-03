async def bot_delete_message(state, sent):
    data = await state.get_data()
    bot_messages = data.get("bot_messages", [])
    bot_messages.append(sent.message_id)
    await state.update_data(bot_messages=bot_messages)

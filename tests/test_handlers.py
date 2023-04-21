# from aiogram import types
#
# from tgbot.handlers import user


# async def test_start_command():
#     message = types.Message(text="/start")
#     result = await user.start_or_help_commands(message)
#     assert result.text == "Hello! This is a Telegram bot."
#
#
# async def test_help_command():
#     message = types.Message(text="/help")
#     result = await user.help_command(message)
#     assert "Available commands:" in result.text

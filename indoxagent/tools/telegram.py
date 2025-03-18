from typing import Dict, Any
from indoxagent.tools.toolkit import Toolkit
from telegram import Bot

class TelegramTools(Toolkit):
    """
    TelegramTool sends messages to a Telegram channel.
    """

    def __init__(self, bot_token: str, channel_id: str):
        super().__init__(name="TelegramTool")
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id
        self.register(self.send_message)

    async def send_message(self, message: str) -> str:
        """
        Sends a message to a Telegram channel.

        Args:
            message (str): The message to send.

        Returns:
            str: Confirmation that the message was sent.
        """
        try:
            response = await self.bot.send_message(chat_id=self.channel_id, text=message, parse_mode="Markdown")
            return f"✅ Message sent! Response: {response}"
        except Exception as e:
            return f"❌ Failed to send message: {e}"

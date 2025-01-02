# utils/error_handler.py
class ErrorHandler:
    @staticmethod
    async def handle(ctx: BotContext, error: Exception):
        logger.error(f"Error: {error}")
        await ctx.bot.send_message(
            chat_id=ctx.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_main_menu()
        )

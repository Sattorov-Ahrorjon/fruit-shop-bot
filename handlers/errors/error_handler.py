import logging
from aiogram import Router
from aiogram import exceptions

router = Router()


@router.error()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return:
    """

    if isinstance(exception, exceptions.TelegramUnauthorizedError):
        logging.exception("Exception raised when bot token is invalid.")
        return True

    if isinstance(exception, exceptions.TelegramForbiddenError):
        print("User not found")
        logging.exception('Exception raised when bot is kicked from chat or etc.')
        return True
    if isinstance(exception, exceptions.TelegramServerError):
        logging.exception('Exception raised when Telegram server returns 5xx error.')
        return True

    if isinstance(exception, exceptions.ClientDecodeError):
        logging.exception("Exception raised when client can't decode response. (Malformed response, etc.)")
        return True

    if isinstance(exception, exceptions.DetailedAiogramError):
        logging.exception("Base exception for all aiogram errors with detailed message.")
        return True

    if isinstance(exception, exceptions.TelegramConflictError):
        logging.exception("Exception raised when bot token is already used by another application in polling mode.")
        return True

    if isinstance(exception, exceptions.TelegramNetworkError):
        logging.exception("Base exception for all Telegram network errors.")
        return True

    if isinstance(exception, exceptions.TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, exceptions.TelegramBadRequest):
        logging.exception("Exception raised when request is malformed.")
        return True

    if isinstance(exception, exceptions.UnsupportedKeywordArgument):
        logging.exception("Exception raised when a keyword argument is passed as filter.")
        return True

    if isinstance(exception, exceptions.CallbackAnswerException):
        logging.exception("Exception for callback answer.")
        return True

    if isinstance(exception, exceptions.TelegramNotFound):
        logging.exception("Exception raised when chat, message, user, etc. not found.")
        return True

    if isinstance(exception, exceptions.TelegramEntityTooLarge):
        logging.exception("Exception raised when you are trying to send a file that is too large.")
        return True

    if isinstance(exception, exceptions.RestartingTelegram):
        logging.exception("""Exception raised when Telegram server is restarting.

                            It seems like this error is not used by Telegram anymore,
                            but it's still here for backward compatibility.

                            Currently, you should expect that Telegram can raise RetryAfter (with timeout 5 seconds)
                             error instead of this one."""
                          )
        return True

    logging.exception(f'Update: {update} \n{exception}')

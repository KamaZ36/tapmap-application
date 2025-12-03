from app.bots.user_tg_bot.messages.base import BaseMessage


class DriverNotAuthInUserBotMessage(BaseMessage):
    _text = "Пройдите авторизацию в основном боте!!!"


class UserNotIsDriverMessage(BaseMessage):
    _text = (
        "Вы не являетесь водителем. Если хотите им стать, обратитесь к администратору."
    )


class AtuhSessionNotFoundErrorMessage(BaseMessage):
    _text = (
        "⚠️ Требуется авторизация\n\n"
        "Вы не авторизованы в системе.\n"
        "Пройдите регистрацию в основном боте для водителей, чтобы получить доступ к заказам."
    )

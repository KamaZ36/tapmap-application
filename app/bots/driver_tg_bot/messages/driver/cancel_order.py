from app.bots.driver_tg_bot.messages.base import BaseMessage


class SuccessfulCancelOrderMessage(BaseMessage):
    def __init__(self, reason: str) -> None:
        self.reason = reason

    @property
    def text(self) -> str:
        return f"❌ Ваш заказ отменен с причиной: {self.reason}"

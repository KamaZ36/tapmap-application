from abc import ABC
from typing import Any


class BaseMessage(ABC):
    _text: str
    _reply_markup: Any = None
    _parse_mode: str = "HTML"

    @property
    def text(self) -> str:
        return self._text

    @property
    def reply_markup(
        self,
    ) -> Any:
        return self._reply_markup

    @property
    def parse_mode(self) -> str:
        return self._parse_mode

    def pack(self) -> dict[str, Any]:
        content = {"text": self.text, "parse_mode": self.parse_mode}

        if self.reply_markup:
            content["reply_markup"] = self.reply_markup

        return content

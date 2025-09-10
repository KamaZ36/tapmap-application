from dataclasses import dataclass

from app.domain.exceptions.base import AppException


@dataclass
class CommentTooLong(AppException):
    error_code = "ORDER_COMMENT_TOO_LONG"

    count_symbols: int

    @property
    def message(self) -> str:
        return f"Слишком длинный комментарий: {self.count_symbols} символов."


@dataclass
class CommentEmpty(AppException):
    @property
    def message(self) -> str:
        return "Комментарий не может быть пустым."

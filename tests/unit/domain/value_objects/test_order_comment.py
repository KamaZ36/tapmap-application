import pytest
from app.domain.value_objects.order_comment import OrderComment, CommentCannotEmpty, CommentTooLong


def test_order_comment_valid() -> None:
    comment = OrderComment(text="Нормальный комментарий")
    assert comment.text == "Нормальный комментарий"

def test_order_comment_empty_raises() -> None:
    with pytest.raises(CommentCannotEmpty):
        OrderComment(text="")  # Пустая строка
    
    with pytest.raises(CommentCannotEmpty):
        OrderComment(text="    ")  # Только пробелы

def test_order_comment_error_comment_too_long() -> None:
    long_text = "x" * 501
    with pytest.raises(CommentTooLong):
        OrderComment(text=long_text)
        
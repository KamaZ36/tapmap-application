from dataclasses import dataclass

from app.domain.exceptions.comment import CommentEmpty, CommentTooLong
from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True)
class OrderComment(ValueObject): 
    text: str
    
    def __post_init__(self) -> None: 
        if not self.text.strip(): 
            raise CommentEmpty()
        if len(self.text) > 500: 
            raise CommentTooLong(count_symbols=len(self.text)) 

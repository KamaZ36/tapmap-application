from dataclasses import dataclass


@dataclass
class CreateDraftOrderCommand:
    start_point_address: str | None = None
    start_point_latitude: float | None = None
    start_point_longitude: float | None = None

    end_point_address: str | None = None
    end_point_latitude: float | None = None
    end_point_longitude: float | None = None


@dataclass
class AddCommentToDraftOrderCommand:
    comment: str

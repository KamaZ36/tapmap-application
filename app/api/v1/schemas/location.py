from typing import Self
from pydantic import BaseModel, model_validator


class RouteInfoSchema(BaseModel):
    travel_distance: int
    travel_time: int


class CoordinatesSchema(BaseModel):
    latitude: float
    longitude: float


class PointSchema(BaseModel):
    address: str | None = None
    coordinates: CoordinatesSchema | None = None

from typing import Protocol

class BaseGeocoder(Protocol):
    
    async def get_coordinates(self, address: str) -> dict: ...
    
    async def get_address(self, latitude: float, longitude: float) -> dict: ...

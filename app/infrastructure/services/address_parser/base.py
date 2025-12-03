from asyncio import Protocol

from app.application.dtos.location import ParsedAddressDTO


class BaseAddressParser(Protocol):
    async def parse_address(self, address: str) -> ParsedAddressDTO: ...

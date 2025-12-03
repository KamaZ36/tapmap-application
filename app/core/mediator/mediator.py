from typing import Any

from app.application.commands.base import CR, CT, BaseCommand, CommandHandler
from app.application.queries.base import QR, QT, Query, QueryHandler

from app.core.dependencies import container


class Mediator:
    def __init__(self) -> None:
        self._command_handlers: dict[
            type[BaseCommand], type[CommandHandler[Any, Any]]
        ] = {}
        self._query_handlers: dict[type[Query], type[QueryHandler[Any, Any]]] = {}

    def register_command(
        self, command_type: type[CT], handler: type[CommandHandler[CT, CR]]
    ) -> None:
        self._command_handlers[command_type] = handler

    def register_query(
        self, query_type: type[QT], handler: type[QueryHandler[QT, QR]]
    ) -> None:
        self._query_handlers[query_type] = handler

    async def handle(self, message: BaseCommand | Query) -> Any:
        if isinstance(message, BaseCommand):
            handler_type = self._command_handlers.get(type(message))
        elif isinstance(message, Query):
            handler_type = self._query_handlers.get(type(message))
        else:
            raise ValueError(f"No handler registered for command {type(message)}")

        async with container() as req_container:
            handler = await req_container.get(handler_type)
            return await handler(message)

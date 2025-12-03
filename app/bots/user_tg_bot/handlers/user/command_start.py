from aiogram import Router, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.application.exceptions.order import OrderNotFound
from app.application.commands.user.create_user import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from app.application.queries.order.get_active_for_customer import (
    GetActiveOrderForCustomerQuery,
    GetActiveOrderForCustomerQueryHandler,
)

from app.bots.user_tg_bot.exceptions.auth_session import AuthSessionNotFound
from app.bots.user_tg_bot.messages.user.create_order import (
    AskEndPointForOrderMessage,
    ThereIsAnActiveDraftOrderMessage,
)
from app.bots.user_tg_bot.messages.user.order import OrderPanelMessage
from app.core.dependencies import container
from app.core.mediator import get_mediator
from app.domain.enums.order_status import OrderStatus
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.dtos.auth_session import AuthSession
from app.bots.user_tg_bot.messages.user.register import (
    AskNameForAuthMessage,
    AskPhoneNumberForAuthMessage,
    RegisterSuccessfulMessage,
    ReloadBotMessage,
    SuccessfulAuthMessage,
    WelcomeMessage,
)
from app.bots.user_tg_bot.states.user import (
    RegisterUserStates,
    UserCreateOrderStates,
    UserWithOrderStates,
)
from app.infrastructure.repositories.user.base import BaseUserRepository

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    async with container() as request_container:
        auth_session_repository = await request_container.get(
            BaseTgBotSessionRepository
        )

        auth_session = await auth_session_repository.get_by_tg_id(
            tg_id=message.from_user.id  # type: ignore
        )

    if auth_session is None:
        await state.set_state(RegisterUserStates.get_phone_number)
        await message.answer(**WelcomeMessage().pack())
        await message.answer(**AskPhoneNumberForAuthMessage().pack())
        return

    mediator = get_mediator()

    try:
        query = GetActiveOrderForCustomerQuery(
            customer_id=auth_session.user_id, current_user_id=auth_session.user_id
        )
        order = await mediator.handle(query)

        if order.status == OrderStatus.draft and len(order.points) == 1:
            await message.answer(**ThereIsAnActiveDraftOrderMessage().pack())
            await message.answer(**AskEndPointForOrderMessage(order.id).pack())
            await state.set_state(UserCreateOrderStates.get_end_point)
            return

        order_msg = await message.answer(**OrderPanelMessage(order).pack())
        await state.set_state(UserWithOrderStates.editing_order)
        await state.update_data(
            order_msg_id=order_msg.message_id, order_id=str(order.id)
        )

    except OrderNotFound:
        await message.answer(**ReloadBotMessage().pack())
        await state.clear()
        return


@router.message(RegisterUserStates.get_phone_number, or_f(F.text, F.contact))
async def get_phone_number(message: Message, state: FSMContext) -> None:
    if message.contact is None or message.contact.user_id != message.from_user.id:
        await message.delete()
        await message.answer(**AskPhoneNumberForAuthMessage(is_repeat=True).pack())
        return

    phone_number = PhoneNumber(message.contact.phone_number)

    async with container() as req_container:
        user_repository = await req_container.get(BaseUserRepository)
        user = await user_repository.get_by_phone(phone_number)

        if user is None:
            await message.answer(**AskNameForAuthMessage().pack())
            await state.update_data(phone_number=message.contact.phone_number)  # type: ignore
            await state.set_state(RegisterUserStates.get_name)
            return

        auth_session = AuthSession(
            tg_id=message.from_user.id,
            user_id=user.id,
        )
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        await auth_session_repo.create(auth_session)

    await message.answer(**SuccessfulAuthMessage().pack())
    await state.clear()


@router.message(RegisterUserStates.get_name, F.text)
async def get_name(message: Message, state: FSMContext) -> None:
    user_context = await state.get_data()

    async with container() as req_container:
        register_user_interactor = await req_container.get(CreateUserCommandHandler)
        command = CreateUserCommand(
            phone_number=user_context["phone_number"],
            name=message.text,  # type: ignore
        )
        user = await register_user_interactor(command=command)

        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = AuthSession(tg_id=message.from_user.id, user_id=user.id)

        await auth_session_repository.create(auth_session)

    await message.answer(**RegisterSuccessfulMessage().pack())
    await state.clear()

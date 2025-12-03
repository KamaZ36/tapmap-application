from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter, or_f


router = Router()


@router.message(or_f(F.text, F.voice, F.video_note, F.photo, F.video))
async def clear_any_message_from_user(message: Message) -> None:
    await message.delete()

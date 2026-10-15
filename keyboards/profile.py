from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

router = Router()


@router.message(Command("profile"))
@router.callback_query(F.data.endswith("profile"))
async def cmd_profile(event: Message | CallbackQuery):
    """Что писать в профиле?
    1 Пароль тебе вряд ли понадобится поэтому из соображений безопасности его тут нет. Не жди его здесь увидеть
    2 Дата регистрации аккаунта
    3 Статус активный | неактивный
    4

    Какие кнопки прикреплять?
    1 Изменить статус аккаунта (изменить сообщение и вывести сверху уведомление о смене статуса callback.answer("Статус изменен"))
    2 Оставить отзыв
    """
    await event.answer("Профиль")
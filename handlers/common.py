from aiogram import F, Router
from aiogram.enums import ButtonStyle
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiosqlite import Connection

from database.dnevnik_relations import get_account_status
from keyboards.common_menus import (
    active_account_start_menu,
    inactive_account_start_menu,
)

router = Router()


@router.message(CommandStart(), StateFilter(None))
@router.callback_query(F.data == "back:home", StateFilter(None))
async def cmd_start(event: Message | CallbackQuery, db: Connection):
    is_active = await get_account_status(db=db, tg_id=event.from_user.id) == "active"
    is_message = isinstance(event, Message)
    if is_active:
        text = "Привет, здесь ты можешь отслеживать свои оценки и сравнивать их с оценками других. Помимо обычного просмотра оценок тут есть и другие интересные и полезын фичи, которые ты обязательно должен попробовать\n\nПрямо сейчас ты уже можешь посмотреть сегодняшние оценки или увидеть рейтинг среднего балла всего класса по физике. Выбери, что хочешь из меню ниже\nДля вызова справки /help"
        if is_message:
            await event.answer(text, reply_markup=active_account_start_menu())
        else:
            await event.message.edit_text(
                text, reply_markup=active_account_start_menu()
            )
            await event.answer()
    else:
        text = "Привет, здесь ты можешь отслеживать свои оценки и сравнивать их с оценками других. Помимо обычного просмотра оценок тут есть и другие интересные и полезные фичи, которые ты обязательно должен попробовать\n\nЕсли ты хочешь получить свои оценки и получить доступ к другим функциям, то тебе неоходимо активировать аккаунт /activate"
        if is_message:
            await event.answer(text, reply_markup=inactive_account_start_menu())
        else:
            await event.message.edit_text(
                text, reply_markup=inactive_account_start_menu()
            )
            await event.answer()


@router.message(Command("help"), StateFilter(None))
async def cmd_help(message: Message):
    text = """Инструкции по использованию бота
/start - Запуск бота
/activate - Восстановить дневник
/deactivate - Отвязать дневник
/cancel - Отменить форму
/my_marks - Мои оценки (меню)
/my_marks_all - Все мои оценки
/help - Вызвать данную справку

Связаться со мной — @Xaash_dusty
"""
    await message.answer(text)


@router.message(Command("test"), StateFilter(None))
async def test(m: Message):
    text = (
        "<b>🔴 Главный заголовок (Жирный)</b>\n"
        "<i>Привет! Это демонстрация всех HTML-возможностей.</i>\n\n"
        "📌 <b>Стили текста:</b>\n"
        "• Можно сделать <u>подчеркнутым</u>\n"
        "• Или даже <s>зачеркнутым словом</s>\n"
        "• А важную тайну спрятать в <tg-spoiler>вот такой спойлер</tg-spoiler>\n\n"
        "💻 <b>Код (кликни для копирования):</b>\n"
        "Ваш токен: <code>777555:secret</code>\n"
        "<pre><code class='language-python'>\n"
        "print('Это многострочный код на Python')\n"
        "</code></pre>\n"
        "💬 <b>Цитаты:</b>\n"
        "<blockquote>Обычная статичная цитата</blockquote>\n"
        "<blockquote expandable>Много текста, который по умолчанию свернут в компактный блок для удобства чтения</blockquote>\n\n"
        "🔗 <b>Навигация:</b>\n"
        "Посети наш <a href='https://github.com'>Официальный сайт</a>."
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Оценки", callback_data="marks", style=ButtonStyle.PRIMARY
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Сохранить", callback_data="save", style=ButtonStyle.SUCCESS
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить", callback_data="delete", style=ButtonStyle.DANGER
                ),
            ],
        ]
    )
    await m.answer(text, reply_markup=keyboard)

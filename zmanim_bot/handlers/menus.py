from aiogram.types import Message

from zmanim_bot.keyboards import menus
from zmanim_bot.misc import dp
from zmanim_bot.texts.single import buttons, messages
from zmanim_bot.tracking import track
from zmanim_bot.utils import chat_action


@dp.message_handler(text=[buttons.mm_holidays, buttons.hom_main])
@chat_action('text')
@track('Holidays menu')
async def handle_holidays_menu(msg: Message):
    kb = menus.get_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=buttons.hom_more)
@chat_action('text')
@track('More holidays menu')
async def handle_nore_holidays_menu(msg: Message):
    kb = menus.get_more_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=buttons.mm_fasts)
@chat_action('text')
@track('Fasts menu')
async def handle_fasts_menu(msg: Message):
    kb = menus.get_fast_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(commands=['settings'])
@dp.message_handler(text=buttons.mm_settings)
@chat_action('text')
@track('Settings menu')
async def handle_settings_menu(msg: Message):
    kb = menus.get_settings_menu()
    await msg.reply(messages.init_settings, reply_markup=kb)
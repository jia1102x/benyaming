from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_metrics import track

from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.keyboards.menus import get_cancel_keyboard
from zmanim_bot.misc import bot
from zmanim_bot.service import zmanim_service
from zmanim_bot.texts.single import messages
from zmanim_bot.utils import chat_action


@track('Zmanim')
async def handle_zmanim(msg: Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, 'typing')  # TODO refactor `@chat_action` to work with `@track`
    await zmanim_service.send_zmanim(state=state)


@track('Zmanim geo-variant')
async def handle_update_zmanim(call: CallbackQuery):
    await call.answer()
    coordinates = call.data.split(CallbackPrefixes.update_zmanim)[1]
    lat, lng = map(float, coordinates.split(','))
    await zmanim_service.update_zmanim(lat, lng)


@chat_action()
async def handle_zmanim_by_date_callback(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await zmanim_service.send_zmanim(call=call, state=state)


@chat_action()
@track('Zmanim by date')
async def handle_zmanim_by_date(msg: Message):
    await zmanim_service.init_zmanim_by_date()
    await msg.reply(messages.greg_date_request, reply_markup=get_cancel_keyboard())


@chat_action()
@track('Shabbat')
async def handle_shabbat(_):
    await zmanim_service.get_shabbat()


@track('Shabbat geo-variant')
async def handle_update_shabbat(call: CallbackQuery, state: FSMContext):
    await call.answer()
    coordinates = call.data.split(CallbackPrefixes.update_shabbat)[1]
    lat, lng = map(float, coordinates.split(','))
    await zmanim_service.update_shabbat(lat, lng, state)


@chat_action()
@track('Daf yomi')
async def handle_daf_yomi(_):
    await zmanim_service.get_daf_yomi()


@chat_action()
@track('Rosh chodesh')
async def handle_rosh_chodesh(_):
    await zmanim_service.get_rosh_chodesh()

from asyncio import create_task

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message

from zmanim_bot.admin.report_management import send_report_to_admins
from zmanim_bot.handlers.utils.redirects import (redirect_to_main_menu, redirect_to_settings_menu)
from zmanim_bot.helpers import check_date
from zmanim_bot.keyboards.menus import get_report_keyboard
from zmanim_bot.misc import bot
from zmanim_bot.service import converter_service, settings_service, zmanim_service
from zmanim_bot.states import FeedbackState
from zmanim_bot.texts.single import messages, buttons
from zmanim_bot.utils import chat_action


# REPORTS

@chat_action('text')
async def handle_report(msg: Message, state: FSMContext):
    report = {
        'message': msg.text,
        'message_id': msg.message_id,
        'user_id': msg.from_user.id,
        'media_ids': []
    }
    await state.set_data(report)
    await FeedbackState.next()

    kb = get_report_keyboard()
    await bot.send_message(msg.chat.id, messages.reports_text_received, reply_markup=kb)


@chat_action('text')
async def handle_done_report(_, state: FSMContext):
    report = await state.get_data()
    await state.finish()
    await redirect_to_main_menu(messages.reports_created)
    create_task(send_report_to_admins(report))


@chat_action('text')
async def handle_report_payload(msg: Message, state: FSMContext):
    if msg.content_type != ContentType.PHOTO:
        return await msg.reply(messages.reports_incorrect_media_type)

    report = await state.get_data()
    report['media_ids'].append((msg.photo[-1].file_id, 'photo'))
    await state.set_data(report)

    await msg.reply(messages.reports_media_received)


# CONVERTER #

@chat_action('text')
async def handle_converter_gregorian_date(msg: Message, state: FSMContext):
    resp, kb = converter_service.convert_greg_to_heb(msg.text)
    await state.finish()
    await msg.reply(resp, reply_markup=kb)
    await redirect_to_main_menu()


@chat_action('text')
async def handle_converter_jewish_date(msg: Message, state: FSMContext):
    resp, kb = converter_service.convert_heb_to_greg(msg.text)
    await state.finish()
    await msg.reply(resp, reply_markup=kb)
    await redirect_to_main_menu()


# ZMANIM #

@chat_action('text')
async def handle_zmanim_gregorian_date(msg: Message, state: FSMContext):
    check_date(msg.text)
    await zmanim_service.send_zmanim(date=msg.text, state=state)
    await state.finish()
    await redirect_to_main_menu()


# LOCATIONS #

@chat_action('text')
async def handle_location_name(msg: Message, state: FSMContext):
    state_data = await state.get_data()

    old_name = state_data.get('location_name')
    redirect_target = state_data.get('redirect_target', 'main')
    redirect_message = state_data.get('redirect_message')
    origin_message_id = state_data.get('origin_message_id')
    targets = {
        'main': redirect_to_main_menu,
        'settings': redirect_to_settings_menu
    }
    redirect = targets[redirect_target]

    if msg.text == buttons.done.value:
        await state.finish()
        return await redirect(redirect_message)

    location_kb = await settings_service.update_location_name(new_name=msg.text, old_name=old_name)

    if origin_message_id:
        await bot.edit_message_reply_markup(msg.from_user.id, origin_message_id, reply_markup=location_kb)

    await state.finish()
    await redirect(redirect_message)

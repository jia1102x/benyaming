from asyncio.tasks import create_task

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message

from zmanim_bot.admin.report_management import send_response_to_user
from zmanim_bot.admin.states import AdminReportResponse
from zmanim_bot.handlers.utils.redirects import redirect_to_main_menu
from zmanim_bot.keyboards.menus import get_cancel_keyboard, get_report_keyboard
from zmanim_bot.misc import bot
from zmanim_bot.texts.single import messages


async def handle_report(call: CallbackQuery, state: FSMContext):
    _, msg_id, user_id = call.data.split(':')
    report_data = {
        'message_id': msg_id,
        'user_id': user_id,
        'media_ids': []
    }

    await AdminReportResponse().waiting_for_response_text.set()
    await state.set_data(report_data)

    resp = 'Write your response:'
    kb = get_cancel_keyboard()

    await bot.send_message(call.from_user.id, resp, reply_markup=kb)
    await call.answer()


async def handle_report_response(msg: Message, state: FSMContext):
    response_data = await state.get_data()
    response_data['response'] = msg.text
    await state.set_data(response_data)
    await AdminReportResponse.next()

    resp = 'Attach media (scrinshots or video)'
    kb = get_report_keyboard()
    await msg.reply(resp, reply_markup=kb)


async def handle_done_report(_, state: FSMContext):
    response = await state.get_data()
    await state.finish()
    await redirect_to_main_menu('Succesfully sent')
    create_task(send_response_to_user(response))


async def handle_report_payload(msg: Message, state: FSMContext):
    if msg.content_type not in (ContentType.PHOTO, ContentType.VIDEO):
        return await msg.reply(messages.reports_incorrect_media_type)

    response = await state.get_data()

    if msg.photo:
        response['media_ids'].append((msg.photo[-1].file_id, 'photo'))
    if msg.video:
        response['media_ids'].append((msg.video.file_id, 'video'))

    await state.set_data(response)
    await msg.reply(messages.reports_media_received)


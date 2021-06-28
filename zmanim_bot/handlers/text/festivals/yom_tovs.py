from aiogram.types import Message

from ....misc import dp
from ....texts.single import buttons
from .... import api
from .... import zmanim_api


@dp.message_handler(text=buttons.hom_rosh_hashana)
async def handle_rosh_hashana(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    resp = await zmanim_api.get_generic_yomtov('rosh_hashana', location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_yom_kippur)
async def handle_yom_kippur(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    resp = await zmanim_api.get_generic_yomtov('yom_kippur', location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_succot)
async def handle_succot(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    resp = await zmanim_api.get_generic_yomtov('succot', location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_shmini_atzeret)
async def handle_shmini_atzeret(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    resp = await zmanim_api.get_generic_yomtov('shmini_atzeres', location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_pesach)
async def handle_pesach(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    resp = await zmanim_api.get_generic_yomtov('pesach', location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_shavuot)
async def handle_shavuot(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    resp = await zmanim_api.get_generic_yomtov('shavuot', location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')

from datetime import date, datetime
from typing import Tuple, Optional, List

from aiogram import types

from ..config import LOCATION_NUMBER_LIMIT
from ..exceptions import NoLocationException, NoLanguageException, NonUniqueLocatioinException, \
    MaxLocationLimitException
from ..misc import db_engine
from .models import User, UserInfo, Location, ZmanimSettings

__all__ = [
    'get_or_create_user',
    'get_cl_offset',
    'get_zmanim',
    'get_havdala',
    'get_lang',
    'get_location',
    'set_zmanim',
    'set_cl',
    'set_havdala',
    'set_lang',
    'set_location',
    'get_processor_type',
    'set_processor_type',
    'get_omer_flag',
    'set_omer_flag',
]


def validate_location(location: Location, locations: List[Location]):
    if len(locations) >= LOCATION_NUMBER_LIMIT:
        raise MaxLocationLimitException

    for loc in locations:
        if loc.lat == location.lat and loc.lng == location.lng:
            raise NonUniqueLocatioinException


async def get_or_create_user(tg_user: types.User) -> User:
    user = await db_engine.find_one(User, User.user_id == tg_user.id)

    if not user:
        user = User(
            user_id=tg_user.id,
            personal_info=UserInfo(
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username
            )
        )
        await db_engine.save(user)
    elif user.personal_info.first_name != tg_user.first_name or \
         user.personal_info.last_name != tg_user.last_name or \
         user.personal_info.username != tg_user.username:
        user.personal_info = UserInfo(
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username
            )
        await db_engine.save(user)

    return user


async def get_lang(tg_user: types.User) -> Optional[str]:
    user = await get_or_create_user(tg_user)
    lang = user.language
    if not lang:
        raise NoLanguageException
    return lang


async def set_lang(tg_user: types.User, lang: str):
    user = await get_or_create_user(tg_user)
    user.language = lang
    await db_engine.save(user)


async def get_location(tg_user: types.User) -> Tuple[float, float]:
    user = await get_or_create_user(tg_user)
    location = list(filter(lambda loc: loc.is_active is True, user.location_list))
    if not location:
        raise NoLocationException

    return location[0].lat, location[0].lng


async def set_location(tg_user: types.User, location: Tuple[float, float]):
    location_obj = Location(
        lat=location[0],
        lng=location[1],
        name='main_loc',
        is_active=True
    )

    user = await get_or_create_user(tg_user)
    validate_location(location_obj, user.location_list)

    for i in range(len(user.location_list)):
        user.location_list[i].is_active = False

    user.location_list.append(location_obj)
    await db_engine.save(user)


async def get_cl_offset(tg_user: types.User) -> int:
    user = await get_or_create_user(tg_user)
    return user.cl_offset


async def set_cl(tg_user: types.User, cl: int):
    user = await get_or_create_user(tg_user)
    user.cl_offset = cl
    await db_engine.save(user)


async def get_havdala(tg_user: types.User) -> str:
    user = await get_or_create_user(tg_user)
    return user.havdala_opinion


async def set_havdala(tg_user: types.User, havdala: str):
    user = await get_or_create_user(tg_user)
    user.havdala_opinion = havdala
    await db_engine.save(user)


async def get_zmanim(tg_user: types.User) -> dict:
    user = await get_or_create_user(tg_user)
    return user.zmanim_settings.dict()


async def set_zmanim(tg_user: types.User, zmanim: dict):
    zmanim_obj = ZmanimSettings(**zmanim)
    user = await get_or_create_user(tg_user)
    user.zmanim_settings = zmanim_obj
    await db_engine.save(user)


async def get_processor_type(tg_user: types.User) -> str:
    user = await get_or_create_user(tg_user)
    return user.processor_type


async def set_processor_type(tg_user: types.User, processor_type: str):
    user = await get_or_create_user(tg_user)
    user.processor_type = processor_type
    await db_engine.save(user)


async def get_omer_flag(tg_user: types.User) -> bool:
    user = await get_or_create_user(tg_user)
    return user.omer.is_enabled


async def set_omer_flag(tg_user: types.User, omer_flag: bool):
    user = await get_or_create_user(tg_user)

    today = date.today()
    omer_time = datetime(today.year, today.month, today.day, 20, 0).isoformat()

    user.omer.is_enabled = omer_flag
    user.omer.is_sent_today = False
    user.omer.notification_time = omer_time

    await db_engine.save(user)

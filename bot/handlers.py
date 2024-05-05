import datetime as dt
import json

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters import QueryFilter
from db.query import SampleQuery
from db.exceptions import UnknownGroupType

import logging

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer(
        f"Hello, {message.from_user.username}!" if message.from_user else "Hello!",
    )


@router.message(QueryFilter())
async def query(message: Message, query: SampleQuery):
    try:
        data = json.loads(message.text)
        start_date = dt.datetime.fromisoformat(data["dt_from"])
        end_date = dt.datetime.fromisoformat(data["dt_upto"])
        group_type = data["group_type"]
        result = await query.get_dataset(start_date, end_date, group_type)
        await message.answer(json.dumps(result))
    except UnknownGroupType:
        await message.answer(
            'group_type может быть только следующий: "month", "day", "hour"'
        )
    except Exception as e:
        logging.exception(e)
        await message.answer("Что-то пошло не так!")


@router.message()
async def default(message: Message):
    await message.answer(
        """
        Невалидный запрос. Пример запроса:
        {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}
        """
    )

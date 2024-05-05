import datetime as dt
import json

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters import QueryFilter

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer(
        f"Hello, {message.from_user.username}!" if message.from_user else "Hello!",
    )


@router.message(QueryFilter())
async def query(message: Message):
    try:
        data = json.loads(message.text)
        start_date = dt.datetime.fromisoformat(data["dt_from"])
        end_date = dt.datetime.fromisoformat(data["dt_upto"])
        group_type = data["group_type"]
        await message.answer("DONE {start_date} {end_date} {group_type}")
    except Exception as e:
        await message.answer(
            """
            Допустимо отправлять только следующие запросы:
            {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}
            {"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"}
            {"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}
            """
        )
        return


@router.message()
async def default(message: Message):
    await message.answer(
        """
        Невалидный запрос. Пример запроса:
        {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}
        """
    )

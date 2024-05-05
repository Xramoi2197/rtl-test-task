import json
from json import JSONDecodeError

from aiogram.filters import BaseFilter
from aiogram.types import Message


class QueryFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            data = json.loads(message.text)
        except JSONDecodeError:
            return False
        if "dt_from" in data and "dt_upto" in data and "group_type" in data:
            return True
        return False

import datetime as dt
from enum import Enum
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

import db.exceptions as db_ex


class AggregationTypes(Enum):
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"


class SampleQuery:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self._client = AsyncIOMotorClient(uri)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    async def get_dataset(
        self, start_date: dt.datetime, end_date: dt.datetime, group_type: str
    ) -> Any:
        date_format = self._get_date_format(group_type)
        pipeline = self._get_aggregation_pipeline(start_date, end_date, date_format)
        date_dict = await self._get_all_dates_dict(start_date, end_date, group_type)
        query_results = await self._collection.aggregate(pipeline).to_list(None)
        return await self._convert_results_to_dataset(
            date_dict, query_results, date_format
        )

    @staticmethod
    def _get_date_format(group_type) -> str:
        match group_type:
            case AggregationTypes.HOUR.value:
                return "%Y-%m-%dT%H"
            case AggregationTypes.DAY.value:
                return "%Y-%m-%d"
            case AggregationTypes.MONTH.value:
                return "%Y-%m"
            case _:
                raise db_ex.UnknownGroupType("Unknown aggregation type")

    @staticmethod
    def _get_aggregation_pipeline(
        start_date: dt.datetime, end_date: dt.datetime, date_format: str
    ) -> list[dict[str, Any]]:
        return [
            {"$match": {"dt": {"$gte": start_date, "$lte": end_date}}},
            {
                "$group": {
                    "_id": {"$dateToString": {"format": date_format, "date": "$dt"}},
                    "totalValue": {"$sum": "$value"},
                }
            },
            {"$sort": {"_id": 1}},
        ]

    @staticmethod
    async def _convert_results_to_dataset(
        date_dict: dict[dt.datetime, Any],
        query_results: list[dict[str, Any]],
        date_format: str,
    ) -> dict[str, list[int | str]]:
        for doc in query_results:
            date = dt.datetime.strptime(doc["_id"], date_format)
            if date in date_dict:
                date_dict[date] = doc["totalValue"]

        return {
            "dataset": [s for s in date_dict.values()],
            "labels": [date.isoformat() for date in date_dict.keys()],
        }

    @staticmethod
    async def _get_all_dates_dict(
        start_date: dt.datetime, end_date: dt.datetime, group_type: str
    ) -> dict[dt.datetime, int]:
        result = {}
        current_date = start_date
        match group_type:
            case AggregationTypes.HOUR.value:
                current_date = current_date.replace(minute=0, second=0, microsecond=0)
                while current_date <= end_date:
                    result[current_date] = 0
                    current_date = current_date + dt.timedelta(hours=1)
            case AggregationTypes.DAY.value:
                current_date = current_date.replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                while current_date <= end_date:
                    result[current_date] = 0
                    current_date = current_date + dt.timedelta(days=1)
            case AggregationTypes.MONTH.value:
                while current_date <= end_date:
                    current_date = current_date.replace(
                        day=1, hour=0, minute=0, second=0, microsecond=0
                    )
                    result[current_date] = 0
                    current_date = current_date + dt.timedelta(days=31)
            case _:
                raise db_ex.UnknownGroupType("Unknown aggregation type")
        return result

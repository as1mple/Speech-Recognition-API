import json
import os

from bson import json_util

import pymongo
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.modules.models.data_models import (
    Message,
    ParamsAddData,
    ParamsDropUser,
    AnswerUserInfo,
    ParamsSearchUser,
)


HOST_MONGO = os.getenv("HOST_MONGO")
PORT_MONGO = int(os.getenv("PORT_MONGO"))
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE_NAME = "mydatabase"

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
CREDENTIALS = dict(host=HOST_MONGO, port=PORT_MONGO, username=USERNAME, password=PASSWORD)
DEFAULT_RESPONSES = {
    500: {"description": "Internal Server Error", "model": Message},
}
router = APIRouter()


@router.get("/health", response_model=Message, responses={**DEFAULT_RESPONSES})
async def health() -> Message:
    """Health endpoint."""
    return Message(message="Success.")


@router.get("/get/data", response_model=AnswerUserInfo)
async def get_user_data(
    details: ParamsSearchUser = Depends(ParamsSearchUser),
) -> Message:
    try:
        with pymongo.MongoClient(**CREDENTIALS) as client:
            database = client[DATABASE_NAME]
            collection = database[details.name_collection]

            if not details.user_id:
                query = {"timestamp": {"$gte": details.time_from, "$lt": details.time_to}}

            elif all([details.time_from, details.time_to, details.user_id]):
                query = {
                    "$and": [
                        {"timestamp": {"$gte": details.time_from, "$lt": details.time_to}},
                        {"user_id": details.user_id},
                    ]
                }

            else:
                query = {"user_id": details.user_id}
            result = [event for event in collection.find(query)]
            result_sanitized = json.loads(json_util.dumps(result))

            return AnswerUserInfo(result=result_sanitized)

    except MemoryError as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/add/data", response_model=Message, responses={**DEFAULT_RESPONSES})
async def add_data(params: ParamsAddData) -> Message:
    try:
        with pymongo.MongoClient(**CREDENTIALS) as client:
            database = client[DATABASE_NAME]
            collection = database[params.name_collection]

            event_dict = params.dict()
            event_dict.pop("name_collection")

            collection.insert_one(event_dict)
            return Message(message="Success.")

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/drop/collection", response_model=Message, responses={**DEFAULT_RESPONSES})
async def drop_collection(name_db: str, name_collection: str):
    try:
        with pymongo.MongoClient(**CREDENTIALS) as client:
            database = client[name_db]
            collection = database[name_collection]

            collection.drop()
            return Message(message=f"Success(drop {name_collection} collection)")

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/drop/user", response_model=Message, responses={**DEFAULT_RESPONSES})
async def drop_user(details: ParamsDropUser = Depends(ParamsDropUser)):
    try:
        with pymongo.MongoClient(**CREDENTIALS) as client:
            database = client[DATABASE_NAME]
            collection = database[details.name_collection]

            if details.timestamp:
                collection.delete_one(
                    {
                        "$and": [
                            {"user_id": details.user_id},
                            {"timestamp": details.timestamp},
                        ]
                    }
                )

            else:
                collection.delete_many(
                    {"user_id": details.user_id},
                )
            return Message(message=f"Success(drop object)")

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

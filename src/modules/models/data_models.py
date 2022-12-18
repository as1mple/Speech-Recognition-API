from datetime import datetime
from typing import List, Optional, Dict, Any, Union

from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class ParamsSearchUser(BaseModel):
    user_id: Optional[str]
    time_from: Optional[datetime]
    time_to: Optional[datetime]


class ParamsDropUser(BaseModel):
    user_id: Optional[str]
    timestamp: Optional[datetime]


class ParamsAddData(BaseModel):
    user_id: str
    text: str
    speech_bytes: Union[str, bytes]
    language: str
    timestamp: datetime


class UserData(BaseModel):
    _id: Dict[str, str] = Field(example={"$oid": "636e30fc142ce00732e390bf"})
    user_id: str = Field(example={"$oid": "2372372232323"})
    text: str = Field(example={"text": "example"})
    language: str = Field(example={"language": "uk-UA"})
    speech_bytes: Union[str, bytes] = Field(example={"speech_bytes": "example"})
    timestamp: datetime = Field(example={"timestamp": "2021-04-20T12:00:00Z"})


class AnswerUserInfo(BaseModel):
    result: List

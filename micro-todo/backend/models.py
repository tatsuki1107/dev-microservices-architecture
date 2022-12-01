from pydantic import BaseModel


class User(BaseModel):
    micro_id: str


class Todos(BaseModel):
    todo: str
    date: str


class Micro_id(BaseModel):
    micro_id: str

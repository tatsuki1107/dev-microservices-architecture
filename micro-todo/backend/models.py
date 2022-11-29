from pydantic import BaseModel


class User(BaseModel):
    micro_id: str


class Todos(BaseModel):
    todo: str
    date: str

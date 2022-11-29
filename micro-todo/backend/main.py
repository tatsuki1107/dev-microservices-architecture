from typing import List
from urllib.request import Request
from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from models import User, Todos


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

fake_todo_db = {
    "123": {
        "todos": [
            {"todo": "プログラミング", "date": "2022-11-29"},
            {"todo": "バイト", "date": "2022-11-30"},
            {"todo": "学校", "date": "2022-11-30"}
        ]
    },
    "456": {
        "todos": [
            {"todo": "営業", "date": "2022-11-29"},
            {"todo": "飲み", "date": "2022-11-29"},
            {"todo": "学校", "date": "2022-11-30"}
        ]
    }
}


@app.post("/user", response_model=List[Todos])
def get_user(res: User):
    user_todo = fake_todo_db[res.micro_id]
    todos = user_todo["todos"]
    if not todos:
        return HTTPException(status_code=400, detail="Inactive user")
    return todos


@app.get('/sample_todo')
async def get_todo():
    return {"todo": "go to schoole!"}

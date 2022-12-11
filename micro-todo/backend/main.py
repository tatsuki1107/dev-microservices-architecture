from typing import List
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from models import User, Todos, Micro_id


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


# main-servieとのAPI


@app.post('/user_todo', response_model=Todos)
async def get_todo(req: Micro_id):
    user_todos = fake_todo_db[req.micro_id]
    first_todo = user_todos["todos"][0]
    return first_todo

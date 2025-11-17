# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="TaskFlow MVP")

# 임시 데이터 저장소 (메모리)
# 실제 프로덕션에서는 데이터베이스를 사용해야 합니다
todos_db: List[dict] = []
todo_id_counter = 1

class TodoCreate(BaseModel):
    """TODO 생성 요청 모델"""
    title: str
    description: str = ""

class TodoResponse(BaseModel):
    """TODO 응답 모델"""
    id: int
    title: str
    description: str
    completed: bool = False

@app.get("/")
def read_root():
    """헬스체크 엔드포인트 - 서버가 정상 동작하는지 확인"""
    return {"message": "TaskFlow MVP is running!", "version": "0.1.0"}

@app.get("/todos", response_model=List[TodoResponse])
def get_todos():
    """모든 TODO 조회"""
    return todos_db

@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate):
    """새 TODO 생성"""
    global todo_id_counter

    new_todo = {
        "id": todo_id_counter,
        "title": todo.title,
        "description": todo.description,
        "completed": False
    }

    todos_db.append(new_todo)
    todo_id_counter += 1

    return new_todo

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """특정 TODO 조회"""
    for todo in todos_db:
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(status_code=404, detail="TODO not found")

@app.patch("/todos/{todo_id}/complete")
def complete_todo(todo_id: int):
    """TODO 완료 처리"""
    for todo in todos_db:
        if todo["id"] == todo_id:
            todo["completed"] = True
            return todo

    raise HTTPException(status_code=404, detail="TODO not found")

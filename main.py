from fastapi import FastAPI
from app.api.v1 import tasks, users, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Настройки CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    # Добавьте другие адреса по необходимости
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def welcome() -> dict:
    return {"message": "My taskmanager app"}


app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

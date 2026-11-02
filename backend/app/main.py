import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, logger
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from app.api import api
from app.common.exceptions import (
    BusinessException,
    business_exception_handler,
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.database import Base, engine
from app.models.user import User
from app.models.lab import Lab
from app.models.reservation import Reservation
from fastapi.staticfiles import StaticFiles
from app.config import UPLOAD_DIR
from app.models.equipment import Equipment
from app.services import reservation_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动项目开启异步的扫描任务
    task = asyncio.create_task(reservation_services.run_expire_scan())
    try:
        yield
    finally:
        task.cancel()  # 关闭项目同时取消异步任务
        await asyncio.gather(
            task, return_exceptions=True
        )  # 取消任务不再把cancelerror抛回lifespan


Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端源，不要直接写 ["*"]
    allow_credentials=True,  # 关键：允许前端携带 Authorization token
    allow_methods=["*"],  # 允许所有请求方法 GET POST PUT DELETE OPTIONS
    allow_headers=["*"],  # 允许所有请求头（包含Authorization）
)

app.include_router(api)

app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
# 全局异常兜底，放在最后
app.add_exception_handler(Exception, global_exception_handler)

# 挂载静态资源：/uploads/xxx.jpg → uploads/xxx.jpg
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

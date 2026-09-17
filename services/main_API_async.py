import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse

from api.api_auth import router as auth_router
from api.api_relatives import router as relatives_router
from core.config import logger
from core.exceptions import AppError
from db.rep_connection import DataBaseManagerAsync


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация базы данных при старте приложения."""
    db_url = os.getenv("DATABASE_URL")

    if db_url:
        db = DataBaseManagerAsync(db_url=db_url)
    else:
        test_db_path = Path(__file__).resolve().parent / "test_family_tree.db"
        db = DataBaseManagerAsync(db_url=str(test_db_path))

    await db.create_tables()
    yield


app = FastAPI(docs_url=None, lifespan=lifespan)

# Подключение роутеров
app.include_router(relatives_router)
app.include_router(auth_router)


# Глобальный обработчик кастомных ошибок
@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    """Обработчик кастомных ошибок приложения."""
    logger.error(f"Ошибка приложения: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.get("/")
def read_root():
    """Проверка работоспособности сервера."""
    return {"message": "Привет! Наш сервер генеалогического древа успешно запущен!"}


@app.get("/docs", include_in_schema=False)
def dark_theme_swagger():
    """Тёмная тема для Swagger UI."""
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - Swagger UI",
    )

    dark_css = """
    <style>
        body { background-color: #1b1b1b !important; color: #eeeeee !important; }
        .swagger-ui { filter: invert(88%) hue-rotate(180deg); }
        .swagger-ui .opblock .opblock-summary-path { color: #ffffff !important; }
        .swagger-ui .info .title { color: #ffffff !important; }
    </style>
    """

    html_content = (
        bytes(response.body).decode("utf-8").replace("</head>", f"{dark_css}</head>")
    )
    return HTMLResponse(content=html_content, status_code=response.status_code)

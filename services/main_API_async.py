from contextlib import asynccontextmanager

from api.api_auth import router as auth_router
from api.api_relatives import router
from db.create_db import create_bd_from_path, db_path
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html


@asynccontextmanager
async def lifespan(app: FastAPI):
    """."""
    # Код до yield выполняется ПРИ СТАРТЕ сервера
    await create_bd_from_path(str(db_path)).create_tables()
    yield


app = FastAPI(docs_url=None, lifespan=lifespan)

app.include_router(router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    """."""
    return {"message": "Привет! Наш сервер генеалогического древа успешно запущен!"}


@app.get("/docs", include_in_schema=False)
def dark_themez():
    """Настоящая тёмная тема для Swagger UI без ругани линтера."""
    # 1. Получаем стандартный HTML-ответ от FastAPI
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - Swagger UI",
    )

    # 2. Наш CSS-код, который делает инверсию цветов и мягкий тёмный фон
    dark_css = """
    <style>
        body { background-color: #1b1b1b !important; color: #eeeeee !important; }
        .swagger-ui { filter: invert(88%) hue-rotate(180deg); }
        .swagger-ui .opblock .opblock-summary-path { color: #ffffff !important; }
        .swagger-ui .info .title { color: #ffffff !important; }
    </style>
    """

    # 3. Встраиваем наши стили прямо в тело HTML-страницы (перед закрывающим тегом </head>)
    # Переводим текст ответа в строку, делаем замену и упаковываем обратно в байты
    html_bytes = bytes(response.body)
    html_content = html_bytes.decode("utf-8").replace("</head>", f"{dark_css}</head>")

    # 4. Возвращаем модифицированный ответ
    from fastapi.responses import HTMLResponse

    return HTMLResponse(content=html_content, status_code=response.status_code)

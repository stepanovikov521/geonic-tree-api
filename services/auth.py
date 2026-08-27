from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext

# 1. Настройки безопасности (в реальном проекте берутся из .env)
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME_IN_PRODUCTION"  # Ключ для подписи JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 2. Инициализируем контекст хеширования (используем bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Работа с паролями ---


def hash_password(password: str) -> str:
    """Хеширует чистый пароль с использованием bcrypt и соли."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли введённый пароль соленному хэшу из БД."""
    return pwd_context.verify(plain_password, hashed_password)


# --- Работа с JWT ---


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Генерирует JWT-токен на основе payload данных."""
    to_encode = data.copy()

    # Задаём время жизни токена
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Полезная нагрузка (Payload)
    to_encode.update({"exp": expire})

    # Создаём токен (Header.Payload.Signature)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Декодирует и проверяет подпись JWT-токена."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        # Токен просрочен, подделан или невалиден
        return None

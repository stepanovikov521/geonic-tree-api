from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.dependencies import get_user_repository
from db.rep_user import UserRepository
from models.models_user import User
from schemas.auth import (
    TokenSchema,
    UserLoginSchema,
    UserOutSchema,
    UserRegisterSchema,
)
from services.auth_service import AuthService
from core.exceptions import AppException, EntityNotFoundException, UnauthorizedException

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

# Для Swagger UI кнопки "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_rep: UserRepository = Depends(get_user_repository),
) -> UserOutSchema:
    """Dependency: проверяет JWT и возвращает текущего пользователя."""
    payload = AuthService.decode_token(token)
    if not payload:
        raise UnauthorizedException("Невалидный или просроченный токен")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Токен не содержит ID пользователя")

    user = await user_rep.get_by_id(int(user_id))
    if not user:
        from core.exceptions import EntityNotFoundException

        raise EntityNotFoundException("Пользователь", int(user_id))

    return UserOutSchema.model_validate(user)


@router.post("/register", response_model=UserOutSchema)
async def register(
    user_data: UserRegisterSchema,
    user_rep: UserRepository = Depends(get_user_repository),
):
    """Регистрация нового пользователя."""
    existing_user = await user_rep.get_by_email(user_data.email)
    if existing_user:
        raise AppException("Пользователь с таким email уже существует", status_code=400)

    hashed_pwd = AuthService.hash_password(user_data.password)
    new_user = await user_rep.create_user(
        User(email=user_data.email, hashed_password=hashed_pwd)
    )

    return UserOutSchema.model_validate(new_user)


@router.post("/login", response_model=TokenSchema)
async def login(
    credentials: UserLoginSchema,
    user_rep: UserRepository = Depends(get_user_repository),
):
    """Вход и получение JWT-токена."""
    user = await user_rep.get_by_email(credentials.email)
    if not user or not AuthService.verify_password(
        credentials.password, user.hashed_password
    ):
        raise UnauthorizedException("Неверный email или пароль")

    token = AuthService.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOutSchema)
async def read_current_user(current_user=Depends(get_current_user)):
    """Получение профиля текущего вошедшего пользователя (защищённый эндпоинт)."""
    return current_user

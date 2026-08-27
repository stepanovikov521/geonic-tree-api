from api.dependencies import get_user_repository
from db.rep_user import UserRepository
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.models_user import User
from schemas.auth import (
    TokenSchema,
    UserLoginSchema,
    UserOutSchema,
    UserRegisterSchema,
)
from services.auth_service import AuthService

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или просроченный токен",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не содержит ID пользователя",
        )

    user = await user_rep.get_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    return UserOutSchema.model_validate(user)


@router.post("/register", response_model=UserOutSchema)
async def register(
    user_data: UserRegisterSchema,
    user_rep: UserRepository = Depends(get_user_repository),
):
    """Регистрация нового пользователя."""
    existing_user = await user_rep.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    token = AuthService.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOutSchema)
async def read_current_user(current_user=Depends(get_current_user)):
    """Получение профиля текущего вошедшего пользователя (защищённый эндпоинт)."""
    return current_user

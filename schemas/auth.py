from pydantic import BaseModel, ConfigDict, EmailStr


class UserRegisterSchema(BaseModel):
    """Схема для регистрации нового пользователя."""

    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    """Схема для входа в систему."""

    email: EmailStr
    password: str


class UserOutSchema(BaseModel):
    """Схема отдавчи данных пользователя наружу (без пароля)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class TokenSchema(BaseModel):
    """Схема ответа с JWT-токеном."""

    access_token: str
    token_type: str = "bearer"

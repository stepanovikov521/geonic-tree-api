from fastapi import status


class AppException(Exception):
    """Базовое исключение для бизнес-логики приложения."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class EntityNotFoundException(AppException):
    """Исключение, когда сущность не найдена (404)."""

    def __init__(self, entity_name: str, entity_id: int | str):
        super().__init__(
            message=f"{entity_name} с ID {entity_id} не найден",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UnauthorizedException(AppException):
    """Исключение для ошибок аутентификации (401)."""

    def __init__(self, detail: str = "Несанкционированный доступ"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

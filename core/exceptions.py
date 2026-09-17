from fastapi import status


class AppError(Exception):
    """Базовое исключение для бизнес-логики приложения."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        """Инициализация сообщения и статуса."""
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class EntityNotFoundError(AppError):
    """Исключение, когда сущность не найдена (404)."""

    def __init__(self, entity_name: str, entity_id: int | str):
        """Инициализация сообщения и статуса."""
        super().__init__(
            message=f"{entity_name} с ID {entity_id} не найден",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UnauthorizedError(AppError):
    """Исключение для ошибок аутентификации (401)."""

    def __init__(self, detail: str = "Несанкционированный доступ"):
        """Инициализация сообщения и статусу."""
        super().__init__(
            message=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

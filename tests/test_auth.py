import time

from services.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_security_flow():
    """."""
    print("=== 1. ТЕСТ ХЕШИРОВАНИЯ ПАРОЛЯ ===")
    user_password = "MyStrongPassword123!"

    # Замеряем время вычисления bcrypt
    start_time = time.time()
    hashed = hash_password(user_password)
    calc_time = time.time() - start_time

    print(f"Исходный пароль : {user_password}")
    print(f"Захешированный   : {hashed}")
    print(f"Время расчета   : {calc_time:.4f} секунд (bcrypt специально замедлен!)")

    # Проверка паролей
    is_correct = verify_password("MyStrongPassword123!", hashed)
    is_wrong = verify_password("WrongPassword!", hashed)

    print(f"Проверка верного пароля : {is_correct}")  # Должно быть True
    print(f"Проверка неверного     : {is_wrong}\n")  # Должно быть False

    print("=== 2. ТЕСТ ВЫДАЧИ И ПРОВЕРКИ JWT ===")
    user_payload = {"sub": "user_42", "email": "alex@tree.com", "role": "user"}

    # Генерируем токен
    token = create_access_token(data=user_payload)
    print(f"Сгенерированный JWT:\n{token}\n")

    # Проверяем декодирование валидного токена
    decoded = decode_access_token(token)
    print(f"Декодированные данные из токена:\n{decoded}\n")

    # Симуляция атаки: подделка токена
    print("=== 3. ТЕСТ ПОДДЕЛКИ ТОКЕНА (АТАКА) ===")
    # Разбиваем токен на 3 части по точкам
    header, payload, _ = token.split(".")

    # Подменяем сигнатуру на случайный мусор
    tampered_token = f"{header}.{payload}.fake_signature_12345"
    tampered_result = decode_access_token(tampered_token)

    print(f"Результат проверки поддельного токена: {tampered_result}")
    # Должен вернуть None, так как подпись не совпала!


if __name__ == "__main__":
    test_security_flow()

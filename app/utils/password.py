all_special_symbols = '!@#$%^&*?'


def validate_password(password: str):
    checks = [
        (len(password) >= 8, 'пароль має містити як мінімум 8 символів'),
        (any(ch.isdigit() for ch in password), 'немає цифр'),
        (any(ch.isupper() for ch in password), 'немає великої букви'),
        (any(ch in all_special_symbols for ch in password), 'немає спеціального символа')
    ]
    errors = [msg for ok, msg in checks if not ok]
    for ok, msg in checks:
        if not ok:
            return {
        "valid": not errors,
        "errors": errors
    }






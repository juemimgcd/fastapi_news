import bcrypt


MAX_BCRYPT_PASSWORD_BYTES = 72


def _validate_password_length(password: str):
    if len(password.encode("utf-8")) > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValueError("密码长度不能超过72字节")


# 密码加密
def get_hash_password(password: str):
    _validate_password_length(password)
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


# 密码验证: verify 返回值是布尔型
def verify_password(plain_password, hashed_password):
    try:
        _validate_password_length(plain_password)
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except (ValueError, TypeError):
        return False

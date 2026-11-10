"""Bug fixture: equality incorrectly remains valid. Never use in production."""


def is_expired(expires_at: int, now: int) -> bool:
    return now > expires_at

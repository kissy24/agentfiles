"""Example only: compare integer timestamps on the same time basis."""


def is_expired(expires_at: int, now: int) -> bool:
    """A token expires at its deadline, including the exact boundary."""
    return now >= expires_at

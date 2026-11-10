import unittest

from expiry import is_expired


class ExpiryTests(unittest.TestCase):
    def test_before_expiry(self):
        self.assertFalse(is_expired(expires_at=100, now=99))

    def test_at_expiry(self):
        self.assertTrue(is_expired(expires_at=100, now=100))

    def test_after_expiry(self):
        self.assertTrue(is_expired(expires_at=100, now=101))


if __name__ == "__main__":
    unittest.main()

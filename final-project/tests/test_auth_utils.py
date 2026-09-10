from store_locator.auth import hash_password, verify_password


def test_password_hash_and_verify():
    hashed = hash_password("TestPassword123!")
    assert hashed != "TestPassword123!"
    assert verify_password("TestPassword123!", hashed)

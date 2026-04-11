from main import derive_key

def test_derive_key():
    salt = b"1234567890123456"
    key = derive_key("Senha123!", salt)
    assert len(key) == 32
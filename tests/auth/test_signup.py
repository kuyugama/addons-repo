import time
import base64
from src import util


async def test_default(client, secret_rsa):
    public_bytes = util.cryptography.public_key_to_bytes(secret_rsa.public_key())
    public_base64 = base64.b64encode(public_bytes).decode()

    response = await client.post(
        "/auth/signup",
        json={"nickname": "nickname", "secret": "password", "public_key": public_base64},
    )
    print(response.json())
    assert response.status_code == 200

    assert response.json()["expires"] > time.time()


async def test_invalid_key(client, secret_rsa):
    public_base64 = base64.b64encode(b"dummy public key").decode()

    response = await client.post(
        "/auth/signup",
        json={"nickname": "nickname", "secret": "password", "public_key": public_base64},
    )
    print(response.json())
    assert response.status_code == 400

    assert response.json()["category"] == "auth"
    assert response.json()["code"] == "invalid-key"

import time


async def test_default(client, user, secret):
    response = await client.post("/auth/signin", json={"nickname": user.nickname, "secret": secret})
    print(response.json())
    assert response.status_code == 200

    assert response.json()["expires"] > time.time()


async def test_invalid_secret(client, user, secret):
    response = await client.post(
        "/auth/signin", json={"nickname": user.nickname, "secret": secret + " invalid"}
    )
    print(response.json())
    assert response.status_code == 403

    assert response.json()["category"] == "auth"
    assert response.json()["code"] == "invalid-secret"

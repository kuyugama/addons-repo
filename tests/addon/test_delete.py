import io
import hashlib


async def test_default(client, baked_package, token):
    id_hash = hashlib.sha256(baked_package.get_metadata()["id"].encode()).hexdigest()
    file = io.BytesIO(baked_package.bytes())
    file.seek(0)

    response = await client.post(
        "/addon/upload", files={"file": ("-", file)}, headers={"X-Token": token.secret}
    )
    print(response.json())
    assert response.status_code == 200

    assert response.json()["id"] == id_hash

    response = await client.delete(
        "/addon/{id}".format(id=id_hash), headers={"X-Token": token.secret}
    )
    assert response.status_code == 200
    assert response.json()["id"] == id_hash


async def test_single_version(client, baked_package, token):
    id_hash = hashlib.sha256(baked_package.get_metadata()["id"].encode()).hexdigest()
    file = io.BytesIO(baked_package.bytes())
    file.seek(0)

    response = await client.post(
        "/addon/upload", files={"file": ("-", file)}, headers={"X-Token": token.secret}
    )
    print(response.json())
    assert response.status_code == 200

    assert response.json()["id"] == id_hash

    response = await client.delete(
        "/addon/{id}/{version}".format(id=id_hash, version=baked_package.get_metadata()["version"]),
        headers={"X-Token": token.secret},
    )
    assert response.status_code == 200
    assert response.json()["id"] == id_hash
    assert response.json()["versions"] == []

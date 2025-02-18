import hashlib
import io
import base64
import pybaked
from pybaked import BakedReader
from src import util, constants
from tempfile import NamedTemporaryFile


async def test_default(client, baked_package, token):
    file = io.BytesIO(baked_package.bytes())
    file.seek(0)

    response = await client.post(
        "/addon/upload", files={"file": ("-", file)}, headers={"X-Token": token.secret}
    )
    print(response.json())
    assert response.status_code == 200

    assert (
        response.json()["id"]
        == hashlib.sha256(baked_package.get_metadata()["id"].encode()).hexdigest()
    )


async def test_encrypted(client, baked_package, token, secret_rsa):
    file = io.BytesIO(baked_package.bytes())
    file.seek(0)

    response = await client.post(
        "/addon/upload",
        query_string={"encrypt": True},
        files={"file": ("-", file)},
        headers={"X-Token": token.secret},
    )
    print(response.json())
    assert response.status_code == 200

    version = response.json()["versions"][0]

    assert version["encrypted"] is True
    assert version["secret"] is not None
    assert version["version"] == baked_package.get_metadata()["version"]

    # Check if secret can be decrypted with private key
    secret = util.cryptography.rsa_decrypt(secret_rsa, base64.b64decode(version["secret"]))

    id_hash = hashlib.sha256(baked_package.get_metadata()["id"].encode()).hexdigest()

    assert response.json()["id"] == id_hash

    # Try to decrypt origin file
    response = await client.get(
        "/addon/download/{id}/{version}".format(id=id_hash, version=version["version"]),
    )
    assert response.status_code == 200

    decrypted_content = b""
    with NamedTemporaryFile() as encrypted_file:
        encrypted_file.write(response.content)
        size = encrypted_file.tell()
        encrypted_file.seek(0)

        iv = encrypted_file.read(12)

        decryptor = util.cryptography.aes_cipher(secret, iv).decryptor()

        while batch := encrypted_file.read(constants.misc.ADDON_FILE_BATCH):
            if encrypted_file.tell() == size:
                tag = batch[-16:]
                batch = batch[:-16]
                decrypted_content += decryptor.update(batch) + decryptor.finalize_with_tag(tag)
                continue

            decrypted_content += decryptor.update(batch)

    with NamedTemporaryFile(suffix=pybaked.protocol.EXTENSION) as package_file:
        package_file.write(decrypted_content)
        package_file.seek(0)

        reader = BakedReader(package_file.file.name)

        assert reader.metadata == baked_package.get_metadata()

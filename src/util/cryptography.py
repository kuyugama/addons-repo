import os
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPublicKey,
    RSAPrivateKey,
)


def asymmetric_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


def public_key_from_bytes(key: bytes) -> RSAPublicKey:
    return serialization.load_der_public_key(key)


def public_key_to_bytes(key: RSAPublicKey) -> bytes:
    return key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def rsa_verify(key: RSAPublicKey, signature: bytes, data: bytes) -> bool:
    try:
        key.verify(
            signature,
            data,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def rsa_sign(key: RSAPrivateKey, data: bytes) -> bytes:
    return key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )


def rsa_encrypt(public_key: RSAPublicKey, message: bytes) -> bytes:
    return public_key.encrypt(
        message,
        padding.OAEP(
            padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(private_key: RSAPrivateKey, message: bytes) -> bytes:
    return private_key.decrypt(
        message,
        padding.OAEP(
            padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def symmetric_key() -> bytes:
    return os.urandom(32)


def symmetric_iv() -> bytes:
    return os.urandom(12)


def aes_cipher(key: bytes, iv: bytes) -> Cipher:
    return Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())


def aes_encrypt(key: bytes, iv: bytes, message: bytes) -> bytes:
    encryptor = aes_cipher(key, iv).encryptor()

    return encryptor.update(message) + encryptor.finalize()


def aes_decrypt(key: bytes, iv: bytes, message: bytes) -> bytes:
    decryptor = aes_cipher(key, iv).decryptor()

    return decryptor.update(message) + decryptor.finalize()

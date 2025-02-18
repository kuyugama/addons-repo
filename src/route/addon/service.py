import os
import time
import secrets
import pybaked
import hashlib
from pathlib import Path
from base64 import b64encode
from fastapi import UploadFile
from src import util, constants
from src.models import Addon, User, AddonVersion
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, ScalarResult
from addon_system.addon.meta import BakedAddonMeta
from cryptography.hazmat.primitives.ciphers import AEADEncryptionContext


def addon_options():
    return (joinedload(Addon.owner),)


def addon_with_versions():
    return addon_options() + (joinedload(Addon.versions),)


async def count_addons(session: AsyncSession) -> int:
    return await session.scalar(select(func.count(Addon.id)))


async def list_addons(session: AsyncSession, offset: int, limit: int) -> ScalarResult[Addon]:
    return await session.scalars(
        select(Addon).offset(offset).limit(limit).options(*addon_options())
    )


async def get_addon(session: AsyncSession, addon_id: str) -> Addon:
    return await session.scalar(
        select(Addon).filter_by(addon_id=addon_id).options(*addon_with_versions())
    )


async def upload_addon(
    session: AsyncSession, owner: User, file: UploadFile, encrypt: bool = False
) -> Addon:
    metadata = BakedAddonMeta(Path(file.filename))

    root_dir = Path(util.settings.uploads.addons.dir)
    root_dir.mkdir(parents=True, exist_ok=True)

    owner_hash = hashlib.sha256(owner.nickname.encode()).hexdigest()

    name = "{stamp}_{hash}_{seed}{extension}".format(
        stamp=int(time.time()),
        hash=owner_hash[:16],
        seed=secrets.token_hex(16),
        extension=pybaked.protocol.EXTENSION,
    )

    addon_path = root_dir / name

    secret = None
    if encrypt:
        secret = util.cryptography.symmetric_key()

    with addon_path.open("wb") as f:
        iv = util.cryptography.symmetric_iv()
        encryptor: None | AEADEncryptionContext = None
        if encrypt:
            encryptor = util.cryptography.aes_cipher(secret, iv).encryptor()
            f.write(iv)

        while batch := await file.read(constants.misc.ADDON_FILE_BATCH):
            if encryptor:
                f.write(encryptor.update(batch))
                continue

            f.write(batch)

        if encryptor:
            f.write(encryptor.finalize())
            f.write(encryptor.tag)

    addon_id = hashlib.sha256(metadata.id.encode()).hexdigest()

    addon = await get_addon(session, addon_id)

    if not addon:
        addon = Addon(
            addon_id=hashlib.sha256(metadata.id.encode()).hexdigest(),
            owner=owner,
            name=metadata.name,
            authors=metadata.authors,
            description=metadata.description,
            depends=metadata.depends,
        )
        session.add(addon)

    version = AddonVersion(
        addon=addon,
        version=metadata.version,
        path=str(addon_path),
        encrypted=encrypt,
        secret=b64encode(owner.encrypt(secret)).decode("utf-8") if encrypt else None,
    )

    session.add(version)

    await session.commit()

    return addon


async def delete_addon(session: AsyncSession, addon: Addon):
    await session.delete(addon)
    for version in addon.versions:
        await session.delete(version)
        os.remove(version.path)

    await session.commit()
    return addon


async def delete_addon_version(session: AsyncSession, addon: Addon, version: str):
    for version_ in addon.versions.copy():
        if version_.version == version:
            addon.versions.remove(version_)
            await session.delete(version_)
            os.remove(version_.path)

    await session.commit()

    return addon

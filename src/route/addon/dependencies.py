import hashlib
from pathlib import Path

import pybaked

from src import util, constants
from src.models import Addon, User
from tempfile import NamedTemporaryFile
from src.route.addon import service, errors
from fastapi import Depends, UploadFile, File
from src.route.dependencies import require_user
from src.session_holder import acquire_session
from sqlalchemy.ext.asyncio import AsyncSession
from addon_system.errors import AddonMetaInvalid
from addon_system.addon.meta import BakedAddonMeta


@util.fastapi.api_errors(errors.not_found)
async def require_addon(id_: str, session: AsyncSession = Depends(acquire_session)) -> Addon:
    addon = await service.get_addon(session, id_)

    if addon is None:
        raise errors.not_found

    return addon


@util.fastapi.api_errors(
    errors.invalid_package, errors.invalid_package, errors.already_exists, errors.invalid_file
)
async def validate_addon_upload(
    file: UploadFile = File(media_type="python/baked"),
    requester: User = Depends(require_user),
    session: AsyncSession = Depends(acquire_session),
) -> UploadFile:
    newfile = NamedTemporaryFile("wb+", suffix=pybaked.protocol.EXTENSION)
    file.filename = newfile.name
    while batch := await file.read(constants.misc.ADDON_FILE_BATCH):
        newfile.write(batch)

    newfile.seek(0)

    file.file.close()
    file.file = newfile  # noqa

    try:
        meta = BakedAddonMeta(Path(file.filename))

        addon = await service.get_addon(session, hashlib.sha256(meta.id.encode()).hexdigest())

        if addon is not None:
            if addon.owner_id != requester.id:
                raise errors.not_owner

            for version in addon.versions:
                if version.version == meta.version:
                    raise errors.already_exists
    except ValueError:
        raise errors.invalid_package
    except AddonMetaInvalid:
        raise errors.invalid_meta

    return file


@util.fastapi.api_errors(errors.not_owner)
async def validate_addon_owner(
    addon: Addon = Depends(require_addon),
    user: User = Depends(require_user),
):
    if addon.owner_id != user.id:
        raise errors.not_owner

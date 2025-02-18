import pybaked
from starlette.responses import FileResponse

from src import schema, util
from src.models import Addon, User
from src.route.addon import service, errors
from fastapi import APIRouter, Depends, UploadFile

from src.route.addon.dependencies import require_addon, validate_addon_upload, validate_addon_owner
from src.session_holder import acquire_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.route.dependencies import require_offset_and_limit, require_user

router = APIRouter(prefix="/addon")


@router.get(
    "/",
    summary="List addons available",
    response_model=schema.Paginated[schema.Addon],
    operation_id="list_addons",
)
async def list_addons(
    pagination: tuple[int, int] = Depends(require_offset_and_limit),
    session: AsyncSession = Depends(acquire_session),
):
    offset, limit = pagination

    total = await service.count_addons(session)
    items = await service.list_addons(session, offset, limit)

    return util.paginated_response(items.all(), total, offset, limit)


@router.get(
    "/download/{id_}/{version}",
    summary="Download addon",
    response_class=FileResponse,
    operation_id="download_addon",
)
async def download_addon(version: str, addon: Addon = Depends(require_addon)):
    for version_ in addon.versions:
        if version_.version == version:
            return FileResponse(
                version_.path,
                media_type="python/baked",
                filename=addon.name + pybaked.protocol.EXTENSION,
            )

    return errors.version_not_found.response


@router.get(
    "/{id_}",
    summary="Get addon by ID",
    response_model=schema.AddonWithVersions,
    operation_id="get_addon",
)
async def get_addon(addon: Addon = Depends(require_addon)):
    return addon


@router.post(
    "/upload",
    summary="Upload addon",
    response_model=schema.AddonWithVersions,
    operation_id="upload_addon",
)
async def upload_addon(
    file: UploadFile = Depends(validate_addon_upload),
    encrypt: bool = False,
    owner: User = Depends(require_user),
    session: AsyncSession = Depends(acquire_session),
):
    return await service.upload_addon(session, owner, file, encrypt)


@router.delete(
    "/{id_}/{version}",
    summary="Delete addon version",
    response_model=schema.AddonWithVersions,
    dependencies=[Depends(validate_addon_owner)],
    operation_id="delete_addon_version",
)
async def delete_addon_version(
    version: str,
    addon: Addon = Depends(require_addon),
    session: AsyncSession = Depends(acquire_session),
):
    return await service.delete_addon_version(session, addon, version)


@router.delete(
    "/{id_}",
    summary="Delete addon",
    dependencies=[Depends(validate_addon_owner)],
    response_model=schema.Addon,
    operation_id="delete_addon",
)
async def delete_addon(
    addon: Addon = Depends(require_addon), session: AsyncSession = Depends(acquire_session)
):
    return await service.delete_addon(session, addon)

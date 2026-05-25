from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.role_schema import (
    RoleCreate,
    RoleUpdate
)

from app.services.role_service import (
    get_roles,
    create_role,
    update_role,
    delete_role
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.get("/")
def get_all_roles(
    db: Session = Depends(get_db)
):

    """
    Get all roles API.
    """

    return get_roles(db)


@router.post("/")
def create_new_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):

    """
    Create role API.
    """

    return create_role(
        db,
        role
    )


@router.put("/{role_id}")
def update_existing_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db)
):

    """
    Update role API.
    """

    return update_role(
        db,
        role_id,
        role
    )


@router.delete("/{role_id}")
def delete_existing_role(
    role_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete role API.
    """

    return delete_role(
        db,
        role_id
    )
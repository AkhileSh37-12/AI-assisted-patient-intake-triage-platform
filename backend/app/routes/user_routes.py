from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate
)

from app.services.user_service import (
    get_users,
    create_user,
    update_user,
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_all_users(
    db: Session = Depends(get_db)
):

    """
    Get all users API.
    """

    return get_users(db)


@router.post("/")
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    """
    Create user API.
    """

    return create_user(
        db,
        user
    )


@router.put("/{user_id}")
def update_existing_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):

    """
    Update user API.
    """

    return update_user(
        db,
        user_id,
        user
    )


@router.delete("/{user_id}")
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete user API.
    """

    return delete_user(
        db,
        user_id
    )
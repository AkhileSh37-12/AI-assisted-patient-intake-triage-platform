from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User


def get_users(
    db: Session
):

    return db.query(User).all()


def create_user(
    db: Session,
    user
):

    new_user = User(
        **user.model_dump()
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_data": new_user
    }


def update_user(
    db: Session,
    user_id: int,
    updated_user
):

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    for key, value in updated_user.model_dump().items():

        setattr(user, key, value)

    db.commit()

    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user_data": user
    }


def delete_user(
    db: Session,
    user_id: int
):

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted successfully"
    }
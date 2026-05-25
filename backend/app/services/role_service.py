from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.role import Role


def get_roles(
    db: Session
):

    return db.query(Role).all()


def create_role(
    db: Session,
    role
):

    new_role = Role(
        **role.model_dump()
    )

    db.add(new_role)

    db.commit()

    db.refresh(new_role)

    return {
        "message": "Role created successfully",
        "role_data": new_role
    }


def update_role(
    db: Session,
    role_id: int,
    updated_role
):

    role = db.query(Role).filter(
        Role.role_id == role_id
    ).first()

    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    for key, value in updated_role.model_dump().items():

        setattr(role, key, value)

    db.commit()

    db.refresh(role)

    return {
        "message": "Role updated successfully",
        "role_data": role
    }


def delete_role(
    db: Session,
    role_id: int
):

    role = db.query(Role).filter(
        Role.role_id == role_id
    ).first()

    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    db.delete(role)

    db.commit()

    return {
        "message": "Role deleted successfully"
    }
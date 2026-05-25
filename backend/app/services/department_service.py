from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.department import Department


def get_departments(
    db: Session
):

    return db.query(Department).all()


def create_department(
    db: Session,
    department
):

    new_department = Department(
        **department.model_dump()
    )

    db.add(new_department)

    db.commit()

    db.refresh(new_department)

    return {
        "message": "Department created successfully",
        "department_data": new_department
    }


def update_department(
    db: Session,
    department_id: int,
    updated_department
):

    department = db.query(Department).filter(
        Department.department_id == department_id
    ).first()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    for key, value in updated_department.model_dump().items():

        setattr(department, key, value)

    db.commit()

    db.refresh(department)

    return {
        "message": "Department updated successfully",
        "department_data": department
    }


def delete_department(
    db: Session,
    department_id: int
):

    department = db.query(Department).filter(
        Department.department_id == department_id
    ).first()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)

    db.commit()

    return {
        "message": "Department deleted successfully"
    }
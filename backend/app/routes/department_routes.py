from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.department_schema import (
    DepartmentCreate,
    DepartmentUpdate
)

from app.services.department_service import (
    get_departments,
    create_department,
    update_department,
    delete_department
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.get("/")
def get_all_departments(
    db: Session = Depends(get_db)
):

    """
    Get all departments API.
    """

    return get_departments(db)


@router.post("/")
def create_new_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):

    """
    Create department API.
    """

    return create_department(
        db,
        department
    )


@router.put("/{department_id}")
def update_existing_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db)
):

    """
    Update department API.
    """

    return update_department(
        db,
        department_id,
        department
    )


@router.delete("/{department_id}")
def delete_existing_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete department API.
    """

    return delete_department(
        db,
        department_id
    )
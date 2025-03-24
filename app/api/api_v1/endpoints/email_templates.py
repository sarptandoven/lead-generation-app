from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.EmailTemplate])
def read_email_templates(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve email templates.
    """
    templates = crud.email_template.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return templates

@router.post("/", response_model=schemas.EmailTemplate)
def create_email_template(
    *,
    db: Session = Depends(deps.get_db),
    template_in: schemas.EmailTemplateCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new email template.
    """
    template = crud.email_template.create_with_user(
        db=db, obj_in=template_in, user_id=current_user.id
    )
    return template

@router.put("/{template_id}", response_model=schemas.EmailTemplate)
def update_email_template(
    *,
    db: Session = Depends(deps.get_db),
    template_id: int,
    template_in: schemas.EmailTemplateUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an email template.
    """
    template = crud.email_template.get(db=db, id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Email template not found")
    if template.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    template = crud.email_template.update(
        db=db, db_obj=template, obj_in=template_in
    )
    return template

@router.get("/{template_id}", response_model=schemas.EmailTemplate)
def read_email_template(
    *,
    db: Session = Depends(deps.get_db),
    template_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get email template by ID.
    """
    template = crud.email_template.get(db=db, id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Email template not found")
    if template.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return template

@router.delete("/{template_id}", response_model=schemas.EmailTemplate)
def delete_email_template(
    *,
    db: Session = Depends(deps.get_db),
    template_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete email template.
    """
    template = crud.email_template.get(db=db, id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Email template not found")
    if template.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    template = crud.email_template.remove(db=db, id=template_id)
    return template 
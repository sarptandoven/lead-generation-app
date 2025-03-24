from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.services import web_scraper

router = APIRouter()

@router.get("/", response_model=List[schemas.Lead])
def read_leads(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve leads.
    """
    leads = crud.lead.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit, status=status
    )
    return leads

@router.post("/", response_model=schemas.Lead)
def create_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_in: schemas.LeadCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new lead.
    """
    lead = crud.lead.create_with_user(db=db, obj_in=lead_in, user_id=current_user.id)
    return lead

@router.post("/scrape", response_model=schemas.Lead)
async def scrape_lead(
    *,
    db: Session = Depends(deps.get_db),
    linkedin_url: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Scrape lead data from LinkedIn profile URL.
    """
    try:
        lead_data = await web_scraper.scrape_profile(linkedin_url)
        lead_in = schemas.LeadCreate(
            linkedin_url=linkedin_url,
            full_name=lead_data.get("full_name"),
            company=lead_data.get("company"),
            position=lead_data.get("position"),
            email=lead_data.get("email"),
            data=lead_data
        )
        lead = crud.lead.create_with_user(db=db, obj_in=lead_in, user_id=current_user.id)
        return lead
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.put("/{lead_id}", response_model=schemas.Lead)
def update_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_id: int,
    lead_in: schemas.LeadUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a lead.
    """
    lead = crud.lead.get(db=db, id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if lead.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    lead = crud.lead.update(db=db, db_obj=lead, obj_in=lead_in)
    return lead

@router.get("/{lead_id}", response_model=schemas.Lead)
def read_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get lead by ID.
    """
    lead = crud.lead.get(db=db, id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if lead.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return lead

@router.delete("/{lead_id}", response_model=schemas.Lead)
def delete_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete lead.
    """
    lead = crud.lead.get(db=db, id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    if lead.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    lead = crud.lead.remove(db=db, id=lead_id)
    return lead 
from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate

class CRUDLead(CRUDBase[Lead, LeadCreate, LeadUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: LeadCreate, user_id: int
    ) -> Lead:
        obj_in_data = obj_in.dict()
        db_obj = Lead(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100, status: Optional[str] = None
    ) -> List[Lead]:
        query = db.query(self.model).filter(Lead.user_id == user_id)
        if status:
            query = query.filter(Lead.status == status)
        return query.offset(skip).limit(limit).all()

lead = CRUDLead(Lead) 
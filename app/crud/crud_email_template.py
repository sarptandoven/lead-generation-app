from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.email_template import EmailTemplate
from app.schemas.email_template import EmailTemplateCreate, EmailTemplateUpdate

class CRUDEmailTemplate(CRUDBase[EmailTemplate, EmailTemplateCreate, EmailTemplateUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: EmailTemplateCreate, user_id: int
    ) -> EmailTemplate:
        obj_in_data = obj_in.dict()
        db_obj = EmailTemplate(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[EmailTemplate]:
        return (
            db.query(self.model)
            .filter(EmailTemplate.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

email_template = CRUDEmailTemplate(EmailTemplate) 
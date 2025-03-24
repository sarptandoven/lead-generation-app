# Import all the models, so that Base has them before being imported by Alembic
from app.db.base_class import Base
from app.models.user import User
from app.models.lead import Lead
from app.models.email_template import EmailTemplate 
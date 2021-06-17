import logging
from typing import Dict, List, Optional

from hawk_db import retreat
from hawk_db.company import Company, CompanyAdmin
from hawk_db.retreat import Retreat
from hawk_db.user import User

from .base_manager import BaseManager

logger = logging.getLogger(__name__)


class UserManager(BaseManager):
    pass


class CompanyManager(BaseManager):
    def get_company(self, user: User) -> Optional[Company]:
        """Get company user is admin of
        This method makes the assumption a user should only be the admin of one company
        """
        company_admins = (
            self.session.query(CompanyAdmin)
            .filter(CompanyAdmin.admin_id == user.id)
            .all()
        )
        companies = list(
            map(
                lambda emp: self.session.query(Company).get(emp.company_id),
                company_admins,
            )
        )
        if companies:
            return companies[0]

    def create_company(
        self, name: Optional[str] = None, admins: List[User] = []
    ) -> Company:
        """
        Create a new company
        Optionally, include users to add as admins to the new company
        """
        new_company = Company()
        new_company.name = name
        for admin in admins:
            new_company_admin = CompanyAdmin()
            new_company_admin.company_id = new_company.id
            new_company_admin.admin_id = admin.id
            self.session.add(new_company_admin)
        self.session.add(new_company)
        self.session.flush()
        return new_company

    def create_employee(
        self, first_name: str, last_name: str, email: Optional[str], city: Optional[str]
    ):
        pass


class RetreatManager(BaseManager):
    def get_retreats(self, company: Company) -> List[Retreat]:
        return list(
            self.session.query(Retreat).filter(Retreat.company_id == company.id).all()
        )

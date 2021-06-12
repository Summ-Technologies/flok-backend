import logging
from typing import Dict, List, Optional

from hawk_db.company import Company, CompanyAdmin
from hawk_db.user import User

from .base_manager import BaseManager

logger = logging.getLogger(__name__)


class UserManager(BaseManager):
    pass


class CompanyManager(BaseManager):
    def get_companies(self, user: User, is_admin: bool = False) -> List[Company]:
        """
        Return all companies user is an employee of.
        Optionally, if is_admin is set, only return companies user has admin access to.
        """
        if is_admin:
            employee_records = (
                self.session.query(CompanyAdmin)
                .filter(CompanyAdmin.admin_id == user.id)
                .all()
            )
            return list(
                map(
                    lambda emp: self.session.query(Company).get(emp.company_id),
                    employee_records,
                )
            )
        else:
            return []

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

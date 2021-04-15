import logging
from typing import Dict, List, Optional

from hawk_db.company import Company, CompanyAdmin, CompanyEmployee
from hawk_db.retreat import (
    Retreat,
    RetreatEmployeeLocationItem,
    RetreatEmployeeLocationSubmission,
)
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
        else:
            employee_records = (
                self.session.query(CompanyEmployee)
                .filter(CompanyEmployee.user_id == user.id)
                .all()
            )
        return list(
            map(
                lambda emp: self.session.query(Company).get(emp.company_id),
                employee_records,
            )
        )

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
            new_company_admin.company = new_company
            new_company_admin.admin = admin
            self.session.add(new_company_admin)
        self.session.add(new_company)
        self.session.flush()
        return new_company


class RetreatManager(BaseManager):
    def get_retreat(self, id: int) -> Optional[Retreat]:
        """
        Returns retreat for given id, if exists.
        """
        return self.session.query(Retreat).get(id)

    def get_retreats(self, company: Company) -> List[Retreat]:
        """
        Return all retreats for company
        """
        return list(
            self.session.query(Retreat).filter(Retreat.company_id == company.id).all()
        )

    def create_retreat(self, company: Company, name: Optional[str] = None) -> Retreat:
        """
        Create a new retreat
        """
        new_retreat = Retreat()
        new_retreat.company_id = company.id
        new_retreat.data = {}
        new_retreat.name = name
        self.session.add(new_retreat)
        self.session.flush()
        return new_retreat

    def add_employee_location_submission(
        self, retreat: Retreat, submission: Dict
    ) -> RetreatEmployeeLocationSubmission:
        """Add new employee location submission record"""
        new_submission = RetreatEmployeeLocationSubmission()
        new_submission.extra_info = submission.get("extra_info")
        new_submission.retreat_id = retreat.id
        self.session.add(new_submission)
        for location_item in submission.get("location_items", []):
            new_location = RetreatEmployeeLocationItem()
            new_location.employee_count = location_item["employee_count"]
            new_location.google_place_id = location_item["google_place_id"]
            new_location.main_text = location_item["main_text"]
            new_location.secondary_text = location_item["secondary_text"]
            new_submission.location_items.append(new_location)
        self.session.flush()
        return new_submission

    def get_employee_location_submission(
        self,
        retreat: Retreat,
    ) -> Optional[RetreatEmployeeLocationSubmission]:
        """Gets latest employee location submission, if one exists"""
        if retreat.employee_location_submissions:
            return retreat.employee_location_submissions[0]

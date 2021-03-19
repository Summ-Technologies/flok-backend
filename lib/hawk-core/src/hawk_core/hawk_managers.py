import logging
from typing import List, Optional

from hawk_db.company import Company, CompanyAdmin, CompanyEmployee
from hawk_db.retreat import Retreat, RetreatItem, RetreatItemState, RetreatToItem
from hawk_db.user import User
from hawk_models.retreat import TEMPLATES
from sqlalchemy.orm.exc import NoResultFound

from .base_manager import BaseManager
from .exceptions import HawkException

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
    def get_retreats(self, company: Company) -> List[Retreat]:
        """
        Return all retreats for company
        """
        return list(
            self.session.query(Retreat).filter(Retreat.company_id == company.id).all()
        )

    def create_retreat(
        self, company: Company, name: Optional[str] = None, template: str = "V1.0"
    ) -> Retreat:
        """
        Create a new retreat
        """
        new_retreat = Retreat()
        new_retreat.company_id = company.id
        new_retreat.data = {}
        new_retreat.name = name
        self.session.add(new_retreat)
        self.session.flush()
        template_item_uids = TEMPLATES.get(template)
        if not template_item_uids:
            raise HawkException(message=f"Invalid retreat template id: {template}")
        for order, uid in enumerate(template_item_uids):
            try:
                retreat_item = (
                    self.session.query(RetreatItem).filter(RetreatItem.uid == uid).one()
                )
                retreat_to_item = RetreatToItem()
                retreat_to_item.retreat_item_id = retreat_item.id
                retreat_to_item.retreat_id = new_retreat.id
                retreat_to_item.order = order
                retreat_to_item.state = RetreatItemState.TODO
                self.session.add(retreat_to_item)
                self.session.flush()
            except NoResultFound:
                raise HawkException(message=f"Missing retreat item with uid: {uid}")
        return new_retreat

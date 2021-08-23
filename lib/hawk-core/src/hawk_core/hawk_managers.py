import logging
from typing import Optional, Tuple

from hawk_db.lodging import LodgingProposalRequest, RFPLiteResponse
from marshmallow.fields import List
from sqlalchemy.sql.sqltypes import Date

from .base_manager import BaseManager

logger = logging.getLogger(__name__)


class UserManager(BaseManager):
    pass


class LodgingManager(BaseManager):
    def create_lodging_proposal_request(
        self,
        email: str,
        company_name: str,
        number_attendees: Optional[int],
        number_attendees_upper: Optional[int],
        number_attendees_lower: Optional[int],
        flexible_dates: bool,
        occupancy_types: Optional[List],
        meeting_spaces: Optional[List],
        number_nights: Optional[int],
        preferred_months: Optional[List],
        preferred_start_dow: Optional[List],
        start_date: Optional[Date],
        end_date: Optional[Date],
    ) -> LodgingProposalRequest:
        new_request = LodgingProposalRequest()
        new_request.email = email
        new_request.company_name = company_name
        new_request.number_attendees = number_attendees
        new_request.number_attendees_range_lower = number_attendees_lower
        new_request.number_attendees_range_upper = number_attendees_upper
        new_request.flexible_dates = flexible_dates
        new_request.occupancy_types = occupancy_types
        new_request.meeting_spaces = meeting_spaces
        new_request.number_nights = number_nights
        new_request.preferred_months = preferred_months
        new_request.preferred_start_dow = preferred_start_dow
        new_request.start_date = start_date
        new_request.end_date = end_date
        self.session.add(new_request)
        self.session.flush()
        return new_request

    def get_lodging_proposal_request(self, id: int):
        return self.session.query(LodgingProposalRequest).get(id)

    def create_rfp_lite_response(
        self,
        lodging_proposal_request_id: int,
        hotel: str,
        avail_response: bool,
        dates: Optional[any] = None,
    ) -> RFPLiteResponse:
        new_rfp_lite_response = RFPLiteResponse()
        new_rfp_lite_response.lodging_proposal_request_id = lodging_proposal_request_id
        new_rfp_lite_response.hotel_name = hotel
        new_rfp_lite_response.availability_response = avail_response
        new_rfp_lite_response.dates = dates
        self.session.add(new_rfp_lite_response)
        self.session.flush()
        return new_rfp_lite_response

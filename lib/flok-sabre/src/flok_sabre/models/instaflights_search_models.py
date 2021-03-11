from __future__ import annotations

from typing import List

from lib.flok_sabre.models.common import PageModel


class InstaflightsSearchResponse(object):
    def __init__(
        self,
        ReturnDateTime: str,
        DepartureDateTime: str,
        DestinationLocation: str,
        OriginLocation: str,
        PricedItineraries: List[PricedItineraryModel],
        Page: PageModel,
        Links: dict,
    ):
        pass


class PricedItineraryModel(object):
    def __init__(
        self,
        SequenceNumber: int,
        TicketingInfo: dict,
        TPA_Extensions: dict,
        AirItineraryPricingInfo: dict,
        AirItinerary: dict,
    ):
        pass


class TicketingInfoModel(object):
    pass

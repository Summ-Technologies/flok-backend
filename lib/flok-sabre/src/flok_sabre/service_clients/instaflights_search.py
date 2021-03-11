from typing import Optional

from .client import SabreClient


class InstaFlightsSearch(object):
    sabre_client: SabreClient

    def __init__(self, sabre_client: SabreClient):
        self.sabre_client = sabre_client

    def v1_shop_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        **kwargs
    ):
        """
        Args:
            origin (required, str): 3-letter IATA code of the origin airport or multi-airport city (MAC) code.
            destination (required, str): 3-letter IATA code of the destination airport or multi-airport city (MAC) code code.
            departuredate (required, str): Date of departing flight in the time zone of the origin airport.
                Only one value is accepted.
                Maximum value: current date + 192 (days).
            returndate (str): Date of returning flight in the time zone of the destination airport.
                Only one value is accepted.
                Maximum value: departuredate + 16 (days) length of stay.
        Kwargs:
            includedcarriers (str): 2-letter IATA airline code of one or more airline. companies.
            excludedcarriers (str): 2-letter IATA airline code of one or more airline. companies.
            outboundflightstops (int): The maximum quantity of flight connections on all outbound flight segments on an outbound itinerary.
                When using this parameter, a connecting flight is a flight with a change of plane.
            inboundflightstops (int): The maximum quantity of flight connections on all inbound flight segments on an inbound itinerary.
                When using this parameter, a connecting flight is a flight with a change of plane.
            includedconnectpoints (str): IATA airport code of connection points that must appear on both the inbound and outbound flight legs on a roundtrip or one-way itinerary with connecting flights.
                The response includes itineraries with all included connection points on both the outbound and inbound flight legs.
                Itineraries with other connections points are notexcluded from the response. Therefore, the response may include itineraries with connection points that you do not specify.
                When using this parameter, a connection is defined as a flight with a change of plane.
                Valid values: 1–3 IATA airport codes, separated with commas.
            excludedconnectpoints (str): IATA airport code of connection points that must not appear on either an inbound, an outbound, or both connecting flights on a roundtrip or one-way itinerary
                The response excludes itineraries when the excluded connection points appear anywhere, on either the inbound, outbound, or both flight legs.
                When using this parameter, a connection is defined as a flight with a change of plane.
                Valid values: 1–3 IATA airport codes, separated with commas.
            outboundstopduration (int): The sum of the total waiting time for all connections on an outbound itinerary
                This applies only to connecting flights that require a change of planes. It does not apply to flights with stops, without a change of plane.
            inboundstopduration (int): The sum of the total waiting time for all connections on an inbound itinerary
                This applies only to connecting flights that require a change of plane. It does not apply to flights with stops, without a change of plane.
            outbounddeparturewindow (str): Time range during which a first outbound flight segment can depart on the departure date
                The first outbound flight segment is always the first departing flight from an origin airport.
                Searches for itineraries that depart during this time range
                The departure window is in the time zone of the origin airport.
                Format: HHMMHHMM
                Valid values in 24-hour notation:
                HH = 00–23
                MM = 00–59
            inbounddeparturewindow (str): Time range during which a first inbound flight segment can depart on the return date
                The first inbound flight segment is always the first flight on a return trip.
                Searches only for itineraries that depart during this time range
                The departure window is in the time zone of the departure airport.
                Format: HHMMHHMM
                Valid values in 24-hour notation:
                HH = 00–23
                MM = 00–59
            outboundarrivalwindow (str): Time range during which a last outbound flight segment can arrive, after the departure date
                The last outbound flight segment is the last flight from a departure airport to a destination.
                Searches only for itineraries that arrive during this time range
                The arrival window is in the time zone of the destination airport.
                Format: HHMMHHMM
                Valid values in 24-hour notation:
                HH = 00–23
                MM = 00–59
            inboundarrivalwindow (str): Time range during which a last inbound flight segment can arrive on the return date
                The last inbound flight segment is the last flight on a return flight.
                Searches only for itineraries that arrive during this time range
                The arrival window is in the time zone of the arrival airport.
                Format: HHMMHHMM
                Valid values in 24-hour notation:
                HH = 00–23
                MM = 00–59
            onlineitinerariesonly (str): An indicator to base the response on online or interline itineraries
                The indicator is applied to all flight legs and flight segments on inbound and outbound itineraries.
                By default, the API assumes a value of `N`, so it is not necessary to include this parameter to get both itinerary types.
            eticketsonly (str): Indicator to return itineraries based on ticket types.
                By default, the API assumes a value of `N` and retrieves itineraries with all ticket types. Therefore, if you want itineraries with all ticket types, you can omit this parameter.
                The ticket type is returned in the `PricedItineraries.TicketingInfo.TicketType` field.
            minfare (int): Minimum total itinerary fare.
                The API retrieves itineraries with a total itinerary fare that is greater than or equal to `minfare` in  `ItinTotalFare.TotalFare.Amount`.
            maxfare (int): Maximum total itinerary fare
                The API retrieves itineraries with a total itinerary fare that is less than or equal to `maxfare` in `ItinTotalFare.TotalFare.Amount`.
                When both `minfare` and `maxfare` are present in the request, the API retrieves itineraries with total itinerary fares that are greater than or equal to `minfare`, and less than or equal to `maxfare`.
            limit (int): The number of itineraries to retrieve per request.
            offset (int): The starting position in the list of all itineraries that meet the query criteria.
            sortby (str): Primary sort object in the response.
            order (str): Sorting order for the `sortby` primary object.
                You can use order without sortby – In this case, the API uses the default value for  sortby.
            sortby2 (str): Secondary sort object in the response.
            order2 (str): Sorting order for the `sortby2` secondary sort object.
                If you use `sortby2`, then you can omit `order2`.
            pointofsalecountry (str): 2-letter ISO 3166 country code.
                Retrieves data specific to a given point of sale country.
            passengercount (int): Limits the response to only those options with enough seats available to support the passenger count.
            view (str): The response view definition.
                Only one value accepted.
            enabletagging (bool): Returns a TagID for each itinerary and stores in the Sabre cache.
        """
        params = {
            "origin": origin,
            "destination": destination,
            "departuredate": departure_date,
        }
        if return_date:
            params.update({"returndate": return_date})
        params.update(kwargs)
        shop_flights_response = self.sabre_client.get("v1/shop/flights", params=params)
        return shop_flights_response.json()

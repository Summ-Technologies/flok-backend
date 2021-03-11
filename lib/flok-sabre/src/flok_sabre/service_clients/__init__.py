import os

from flok_sabre.service_clients.instaflights_search import InstaFlightsSearch

from .client import SabreClient

sabre_client = SabreClient(
    os.environ["SABRE_CLIENT_ID"], os.environ["SABRE_CLIENT_SECRET"]
)

instaflights_search_client = InstaFlightsSearch(sabre_client)

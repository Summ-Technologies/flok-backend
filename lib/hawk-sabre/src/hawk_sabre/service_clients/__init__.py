import os

from .client import SabreClient
from .instaflights_search import InstaFlightsSearch

sabre_client = SabreClient(
    os.environ["SABRE_CLIENT_ID"], os.environ["SABRE_CLIENT_SECRET"]
)

instaflights_search_client = InstaFlightsSearch(sabre_client)

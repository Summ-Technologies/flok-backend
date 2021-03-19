import os

from hawk_db import retreat
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def setup_db_session(db_uri: str) -> Session:
    db_engine = create_engine(db_uri)
    Session = sessionmaker(bind=db_engine)
    session = Session()
    return session


session = setup_db_session(os.environ["SQLALCHEMY_DATABASE_URI"])


def create_item(**kwargs):
    item = retreat.RetreatItem()
    item.title = kwargs.get("title")
    item.subtitle = kwargs.get("subtitle")
    item.type = kwargs.get("type")
    item.uid = kwargs.get("uid")
    item.data = {}
    session.add(item)
    print(item)


for i in [
    {
        "title": "Flok onboarding call",
        "type": retreat.RetreatItemType.INTAKE_CALL,
        "uid": f"{retreat.RetreatItemType.INTAKE_CALL}-V1.0",
    },
    {
        "title": "Enter employee locations",
        "type": retreat.RetreatItemType.EMPLOYEE_LOCATIONS,
        "uid": f"{retreat.RetreatItemType.EMPLOYEE_LOCATIONS}-V1.0",
    },
    {
        "title": "Receive proposals (free)",
        "type": retreat.RetreatItemType.INITIAL_PROPOSALS,
        "uid": f"{retreat.RetreatItemType.INITIAL_PROPOSALS}-V1.0",
    },
    {
        "title": "Choose (or confirm) your destination",
        "type": retreat.RetreatItemType.DESTINATION_SELECTION,
        "uid": f"{retreat.RetreatItemType.DESTINATION_SELECTION}-V1.0",
    },
    {
        "title": "Flok helps you plan your retreat",
        "subtitle": """Curated & vetted venues
We coordinate flights
Ground transportation
Retreat best practices
Itinerary and activity consultation
Help with local COVID guidelines
Add ons: office supplies, swag, event planner""",
        "type": retreat.RetreatItemType.POST_PAYMENT,
        "uid": f"{retreat.RetreatItemType.POST_PAYMENT}-V1.0",
    },
]:
    create_item(**i)

session.commit()

from summ_rabbitmq.message_types import BaseMessage
from summ_rabbitmq.queue import SimpleQueue


#### New user
class NewFlightEmailReceiptMessage(BaseMessage):
    fields = []

    def __init__(self):
        pass


NEW_FLIGHT_EMAIL_RECEIPT_QUEUE = SimpleQueue(
    "NEW_FLIGHT_EMAIL_RECEIPT", message_type=NewFlightEmailReceiptMessage
)

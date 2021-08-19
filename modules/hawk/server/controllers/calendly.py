import logging

from flask import request
from flask_restful import Resource
from hawk_core.hawk_managers import LodgingManager
from summ_web import responses

from .. import app, db

logger = logging.getLogger(__name__)

lodging_manager: LodgingManager = LodgingManager(db.session, app.config)


class CalendlyWebhookController(Resource):
    def post(self):
        """Handles calendly invites created"""
        post_data = request.get_json(force=True, silent=True)
        if post_data and post_data.get("event") == "invitee.created":
            payload = post_data.get("payload", {})
            tracking = payload.get("tracking", {})
            utm_campaign = tracking.get("utm_campaign")
            try:
                utm_content = int(tracking.get("utm_content"))
            except ValueError:
                utm_content = None
            if utm_campaign == "intake_call" and utm_content != None:
                rfp_record = lodging_manager.get_lodging_proposal_request(
                    int(utm_content)
                )
                if rfp_record:
                    rfp_record.intake_call_calendly_event = payload
                    lodging_manager.commit_changes()
                    return responses.success(
                        {"message": "Updated calendly intake call info"}, 200
                    )
                else:
                    logger.info(
                        "utm_content: %s didn't match any rfp record. payload: %s",
                        utm_content,
                        str(payload),
                    )
            else:
                logger.info("invalid tracking info for payload: %s", str(payload))
        else:
            logger.info(
                "Missing post_data or unhandled event type. post_data: %s",
                str(post_data),
            )
        return responses.success({"message": "Ack, invitee not saved to rfp."}, 202)

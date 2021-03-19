from sqlalchemy.orm import Session


class BaseManager(object):

    session: Session = None
    config: dict = None

    def __init__(self, session: Session, config: dict = {}):
        self.session = session
        self.validate_config(config)
        self.config = config

    def validate_config(self, config: dict):
        """Validate config object has required values, throws exception if valid"""
        pass

    def commit_changes(self):
        self.session.commit()

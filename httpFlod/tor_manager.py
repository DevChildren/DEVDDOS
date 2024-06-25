# tor_manager.py

from .tor_connector import get_tor_session, new_tor_identity

class TorManager:
    def __init__(self):
        pass

    def get_tor_session(self):
        return get_tor_session()

    def change_identity(self):
        return new_tor_identity()

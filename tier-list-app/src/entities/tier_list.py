import uuid


class TierList:
    def __init__(self, name, tierlist_id=None):
        self.name = name
        self.id = tierlist_id or str(uuid.uuid4())

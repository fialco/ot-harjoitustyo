import uuid


class TierList:
    def __init__(self, tierlist_id, name):
        self.id = tierlist_id or str(uuid.uuid4())
        self.name = name

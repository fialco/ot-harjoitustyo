import uuid


class Item:
    def __init__(self, name, image_path, tierlist_id=None):
        self.name = name
        self.image_path = image_path
        self.tierlist_id = tierlist_id or str(uuid.uuid4())

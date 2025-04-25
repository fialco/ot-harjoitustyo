import uuid


class TierList:
    """Class, which represents an individual tier list.

    Attributes:
        name: String of the tier list name.
        tierlist_id: Integer of the tier list id.
    """

    def __init__(self, name, tierlist_id=None):
        """Class constructor. Creates a new tier list.

        Args:
            name: String of the tier list name.
            tierlist_id:
                Optional, by default a generated uuid.
                Integer of the tier list id.
        """

        self.name = name
        self.id = tierlist_id or uuid.uuid4().int

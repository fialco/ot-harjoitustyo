class Tier:
    """Class, which represents an individual tier of a tier list.

    Attributes:
        tierlist_id: Integer of the tier list id.
        name: String of the tier name.
        rank: Integer of the tier rank (0 highest rank, 1 second highest etc.)
    """

    def __init__(self, tierlist_id, name, rank):
        """Class constructor. Creates a new tier.

        Args:
            tierlist_id: Integer of the tier list id.
            name: String of the tier name.
            rank: Integer of the tier rank.
        """

        self.tierlist_id = tierlist_id
        self.name = name
        self.rank = rank

class Item:
    """Class, which represents an individual item of a tier list.

    Attributes:
        tierlist_id: Integer of the tier list id.
        image_path: Integer of the tier list id.
    """

    def __init__(self, tierlist_id, image_path):
        """Class constructor. Creates a new item.

        Args:
            tierlist_id: Integer of the tier list id.
            image_path:
                String of a relative path to an image in data/images/ directory.
                E.g. '/data/images/example.jpg'.
        """

        self.tierlist_id = tierlist_id
        self.image_path = image_path

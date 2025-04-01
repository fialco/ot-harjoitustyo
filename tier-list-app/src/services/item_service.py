from entities.image_item import ImageItem
from repositories.image_repository import ImageRepository

class ItemService:
    def __init__(self):
        # For now used just for ids
        # Proper storage later
        self._items = []

    def add_item(self, image_path, x, y):
        """Adds a new image item."""
        image = ImageRepository.load_image(image_path)
        item_id = f"item_{len(self._items)}"
        image_item = ImageItem(image, item_id, x, y)

        self._items.append(image_item)

        return image_item

    def snap_item_to_tier(self, item, tier_positions, event_y):
        """Snap the item to the closest tier."""

        # Idea for finding the shortest distance from
        # https://medium.com/@zzysjtu/python-min-function-a-deep-dive-f72cbd771872
        closest_tier = min(tier_positions, key=lambda y: abs(event_y - y))
        item.update_position(item.x, closest_tier)

        return item

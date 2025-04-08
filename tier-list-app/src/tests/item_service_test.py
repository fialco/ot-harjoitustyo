import unittest
from services.item_service import ItemService
from entities.image_item import ImageItem


class TestItemService(unittest.TestCase):
    def setUp(self):
        self.service = ItemService()
        self.tier_positions = [50, 150, 250]
        self.item = ImageItem('image.jpg', 12, 100, 100)

    def test_snap_item_to_nearest_tier_when_dropped(self):
        snapped_item = self.service.snap_item_to_tier(
            self.item, self.tier_positions, 120)

        self.assertEqual(snapped_item.y, 150)

import unittest
from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier
from services.tier_list_service import TierListService


#very much W.I.P!
class FakeTierListRepository:
    def __init__(self, tier_lists=None):
        self.tier_lists = tier_lists or []
        self.lastrowid = 0

    def find_all_tier_lists(self):
        return self.tier_lists

    def find_tier_list(self, tierlist_id):
        pass

    def find_items_by_tier_list(self, tierlist_id):
        pass

    def find_tiers_by_tier_list(self, tierlist_id):
        pass

    def create_tier_list(self, tierlist):
        self.tier_lists.append(tierlist)
        self.lastrowid += 1
        tierlist.id = self.lastrowid
        return tierlist

    def create_items(self, items):
        pass

    def create_tiers(self, tiers):
        pass

    def delete_all(self):
        pass

    def delete_tier_list(self, tierlist_id):
        self.tier_lists = [tier_list for tier_list in self.tier_lists if tier_list.id != tierlist_id]

class FakeImageRepository:
    @staticmethod
    def load_image(file_path):
        pass

    @staticmethod
    def get_base_dir_path():
        pass

    @staticmethod
    def check_image_paths(image_paths):
        return image_paths


class TestTierListService(unittest.TestCase):
    def setUp(self):
        self.service = TierListService(
            FakeTierListRepository(),
            FakeImageRepository()
        )

        self.tier_list_name_a = 'TV-shows'
        self.tier_list_name_b = 'Board games'
        self.tier_list_name_c = 'Supercars'

        self.image_paths = ['img_1.jpg', 'img_2.jpg', 'img_3.jpg', 'img_4.jpg']

        self.default_tiers = {0: 'S', 1: 'A', 2: 'B', 3: 'C', 4: 'D'}

    def test_create_tier_list_template(self):
        self.service.create_tier_list_template(
            self.tier_list_name_b,
            self.default_tiers,
            self.image_paths
        )

        lists = self.service.get_tier_lists()
        self.assertEqual(len(lists), 1)
        self.assertEqual(lists[0].name, self.tier_list_name_b)

    def test_delete_tier_list(self):
        self.service.create_tier_list_template(
            self.tier_list_name_a,
            self.default_tiers,
            self.image_paths
        )

        lists = self.service.get_tier_lists()
        self.assertEqual(len(lists), 1)

        self.service.delete_tier_list(1)

        lists = self.service.get_tier_lists()
        self.assertEqual(len(lists), 0)


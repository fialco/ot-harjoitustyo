import unittest
from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier
from services.tier_list_service import TierListService


class FakeTierListRepository:
    def __init__(self, tier_lists=None, items=None, tiers=None):
        self.tier_lists = tier_lists or []
        self.items = items or []
        self.tiers = tiers or []
        self.lastrowid = 0

    def find_all_tier_lists(self):
        return self.tier_lists

    def find_tier_list(self, tierlist_id):
        return next((tier_list for tier_list in self.tier_lists if tier_list.id == tierlist_id), None)

    def find_items_by_tier_list(self, tierlist_id):
        return [item for item in self.items if item.tierlist_id == tierlist_id]

    def find_tiers_by_tier_list(self, tierlist_id):
        return [tier for tier in self.tiers if tier.tierlist_id == tierlist_id]

    def create_tier_list(self, tierlist):
        self.tier_lists.append(tierlist)
        self.lastrowid += 1
        tierlist.id = self.lastrowid
        return tierlist

    def create_items(self, items):
        self.items.extend(items)

    def create_tiers(self, tiers):
        self.tiers.extend(tiers)

    def delete_all(self):
        self.tier_lists = []
        self.items = []
        self.tiers = []

    def delete_tier_list(self, tierlist_id):
        self.tier_lists = [
            tier_list for tier_list in self.tier_lists if tier_list.id != tierlist_id]


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

    def create_tier_list_template(self):
        self.board_games_tier_list = self.service.create_tier_list_template(
            self.tier_list_name_b,
            self.default_tiers,
            self.image_paths
        )

    def test_create_tier_list_template(self):
        self.service.create_tier_list_template(
            self.tier_list_name_a,
            self.default_tiers,
            self.image_paths
        )

        lists = self.service.get_tier_lists()
        self.assertEqual(len(lists), 1)
        self.assertEqual(lists[0].name, self.tier_list_name_a)

    def test_delete_tier_list(self):
        self.create_tier_list_template()

        lists = self.service.get_tier_lists()
        self.assertEqual(len(lists), 1)

        self.service.delete_tier_list(1)

        lists = self.service.get_tier_lists()
        self.assertEqual(len(lists), 0)

    def test_get_specific_tier_list(self):
        self.create_tier_list_template()

        self.service.create_tier_list_template(
            self.tier_list_name_a,
            self.default_tiers,
            self.image_paths
        )

        self.service.create_tier_list_template(
            self.tier_list_name_c,
            self.default_tiers,
            self.image_paths
        )

        tier_list = self.service.get_tier_list(2)

        self.assertEqual(tier_list.name, 'TV-shows')

    def test_get_items_of_specific_tier_list(self):
        self.create_tier_list_template()

        self.service.create_tier_list_template(
            self.tier_list_name_a,
            self.default_tiers,
            ['img_1.jpg', 'testing.jpg', 'img_3.jpg', 'img_4.jpg']
        )

        self.service.create_tier_list_template(
            self.tier_list_name_c,
            self.default_tiers,
            self.image_paths
        )

        items = self.service.get_items_of_tier_list(2)

        self.assertEqual(items[0].tierlist_id, 2)
        self.assertEqual(items[1].image_path, 'testing.jpg')

    def test_get_tiers_of_specific_tier_list(self):
        self.create_tier_list_template()

        self.service.create_tier_list_template(
            self.tier_list_name_a,
            self.default_tiers,
            self.image_paths
        )

        self.service.create_tier_list_template(
            self.tier_list_name_c,
            {0: 'Best', 1: 'good', 2: 'ok', 3: 'mid', 4: 'dog'},
            self.image_paths
        )

        tiers = self.service.get_tiers_of_tier_list(3)

        self.assertEqual(tiers[0].tierlist_id, 3)
        self.assertEqual(tiers[3].name, 'mid')
        self.assertEqual(tiers[3].rank, 3)
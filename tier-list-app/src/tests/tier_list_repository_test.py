import unittest
from repositories.tier_list_repository import tier_list_repository
from entities.tier_list import TierList
from entities.item import Item

class TestTierListRepository(unittest.TestCase):
    def setUp(self):
        tier_list_repository.delete_tier_lists()
        tier_list_repository.delete_items()

        self.tier_list_music = TierList(1, 'Music genres')
        self.tier_list_tv = TierList(2, 'TV-shows')

        self.item_rock = Item('Rock', 'rock.png', 1)
        self.item_pop = Item('Pop', 'pop.png', 1)

    def test_create(self):
        tier_list_repository.create_tier_list(self.tier_list_music)
        tier_lists = tier_list_repository.find_all_tier_lists()

        self.assertEqual(len(tier_lists), 1)
        self.assertEqual(tier_lists[0].name, self.tier_list_music.name)

    def test_find_specific_tier_list(self):
        tier_list_repository.create_tier_list(self.tier_list_music)
        tier_list_repository.create_tier_list(self.tier_list_tv)

        tier_list = tier_list_repository.find_tier_list(1)

        self.assertEqual(tier_list.name, self.tier_list_music.name)


    def test_find_all_tier_lists(self):
        tier_list_repository.create_tier_list(self.tier_list_music)
        tier_list_repository.create_tier_list(self.tier_list_tv)
        tier_lists = tier_list_repository.find_all_tier_lists()

        self.assertEqual(len(tier_lists), 2)
        self.assertEqual(tier_lists[0].name, self.tier_list_music.name)
        self.assertEqual(tier_lists[1].name, self.tier_list_tv.name)

    def test_find_items_by_tier_list(self):
        tier_list_repository.create_tier_list(self.tier_list_music)

        tier_list_repository.create_item(self.item_rock)
        tier_list_repository.create_item(self.item_pop)

        items = tier_list_repository.find_items_by_tier_list(1)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, self.item_rock.name)
        self.assertEqual(items[1].name, self.item_pop.name)
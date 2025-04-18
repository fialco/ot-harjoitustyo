import unittest
from repositories.tier_list_repository import tier_list_repository
from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier


class TestTierListRepository(unittest.TestCase):
    def setUp(self):
        tier_list_repository.delete_tier_lists()
        tier_list_repository.delete_items()
        tier_list_repository.delete_tiers()

        self.tier_list_music = TierList('Music genres', 1)
        self.tier_list_tv = TierList('TV-shows', 2)

        self.item_rock = Item(1, 'rock.png')
        self.item_pop = Item(1, 'pop.png')

        self.item_simpsons = Item(2, 'simpsons.png')
        self.item_house = Item(2, 'house.png')

        self.tier_5 = Tier(2, "5", 0)
        self.tier_4 = Tier(2, "4", 1)
        self.tier_3 = Tier(2, "3", 2)
        self.tier_2 = Tier(2, "2", 3)
        self.tier_1 = Tier(2, "1", 4)
        self.tier_0 = Tier(2, "0", 5)

    def test_create_tier_list(self):
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

        tier_list_repository.create_items([self.item_rock, self.item_pop])

        items = tier_list_repository.find_items_by_tier_list(1)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].image_path, self.item_rock.image_path)
        self.assertEqual(items[1].image_path, self.item_pop.image_path)

    def test_find_tiers_by_tier_list(self):
        tier_list_repository.create_tier_list(self.tier_list_tv)

        tier_list_repository.create_items(
            [self.item_simpsons, self.item_house])

        tier_list_repository.create_tiers([self.tier_5,
                                          self.tier_4,
                                          self.tier_3,
                                          self.tier_2,
                                          self.tier_1,
                                          self.tier_0])

        tiers = tier_list_repository.find_tiers_by_tier_list(2)
        self.assertEqual(len(tiers), 6)
        self.assertEqual(tiers[0].name, self.tier_5.name)
        self.assertEqual(tiers[2].rank, self.tier_3.rank)

import unittest
from repositories.tier_list_repository import tier_list_repository
from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier


class TestTierListRepository(unittest.TestCase):
    def setUp(self):
        tier_list_repository.delete_all()

        self.tier_list_music = TierList('Music genres', 1)
        self.tier_list_tv = TierList('TV-shows', 2)

        self.item_rock = Item(1, 'rock.png')
        self.item_pop = Item(1, 'pop.png')

        self.item_simpsons = Item(2, 'simpsons.png')
        self.item_house = Item(2, 'house.png')

        self.tier_5_music = Tier(1, "5", 0)
        self.tier_4_music = Tier(1, "4", 1)
        self.tier_3_music = Tier(1, "3", 2)
        self.tier_2_music = Tier(1, "2", 3)
        self.tier_1_music = Tier(1, "1", 4)
        self.tier_0_music = Tier(1, "0", 5)

        self.tier_5_tv = Tier(2, "Best", 0)
        self.tier_4_tv = Tier(2, "Great", 1)
        self.tier_3_tv = Tier(2, "Good", 2)
        self.tier_2_tv = Tier(2, "Mid", 3)
        self.tier_1_tv = Tier(2, "Eeh", 4)
        self.tier_0_tv = Tier(2, "Garbage", 5)

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

        tier_list_repository.create_tiers([self.tier_5_tv,
                                          self.tier_4_tv,
                                          self.tier_3_tv,
                                          self.tier_2_tv,
                                          self.tier_1_tv,
                                          self.tier_0_tv])

        tiers = tier_list_repository.find_tiers_by_tier_list(2)
        self.assertEqual(len(tiers), 6)
        self.assertEqual(tiers[0].name, self.tier_5_tv.name)
        self.assertEqual(tiers[2].rank, self.tier_3_tv.rank)

    def test_delete_specific_tier_list(self):
        tier_list_repository.create_tier_list(self.tier_list_tv)

        tier_list_repository.create_items(
            [self.item_simpsons, self.item_house])

        tier_list_repository.create_tiers([self.tier_5_tv,
                                          self.tier_4_tv,
                                          self.tier_3_tv,
                                          self.tier_2_tv,
                                          self.tier_1_tv,
                                          self.tier_0_tv])

        tier_list_repository.create_tier_list(self.tier_list_music)

        tier_list_repository.create_items(
            [self.item_pop, self.item_rock])

        tier_list_repository.create_tiers([self.tier_5_music,
                                          self.tier_4_music,
                                          self.tier_3_music,
                                          self.tier_2_music,
                                          self.tier_1_music,
                                          self.tier_0_music])

        tier_lists = tier_list_repository.find_all_tier_lists()
        items = tier_list_repository.find_items_by_tier_list(1)
        tiers = tier_list_repository.find_tiers_by_tier_list(1)

        self.assertEqual(len(tier_lists), 2)
        self.assertEqual(len(items), 2)
        self.assertEqual(len(tiers), 6)

        self.assertEqual(tier_lists[0].name, self.tier_list_tv.name)

        tier_list_repository.delete_tier_list(1)

        tier_lists = tier_list_repository.find_all_tier_lists()
        items = tier_list_repository.find_items_by_tier_list(1)
        tiers = tier_list_repository.find_tiers_by_tier_list(1)

        self.assertEqual(len(tier_lists), 1)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(tiers), 0)
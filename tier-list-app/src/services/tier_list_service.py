from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier

from repositories.tier_list_repository import (
    tier_list_repository as default_tier_list_repository
)

from repositories.image_repository import (
    ImageRepository as default_image_repository
)


class InvalidCredentialsError(Exception):
    pass


class UsernameExistsError(Exception):
    pass


class TierListService:
    def __init__(
        self,
        tier_list_repository=default_tier_list_repository,
        image_repository=default_image_repository
    ):

        self.tier_list_repository = tier_list_repository
        self.image_repository = image_repository

    def get_tier_lists(self):
        return self.tier_list_repository.find_all_tier_lists()

    def get_tier_list(self, tierlist_id):
        return self.tier_list_repository.find_tier_list(tierlist_id)

    def get_items_of_tier_list(self, tierlist_id):
        return self.tier_list_repository.find_items_by_tier_list(tierlist_id)

    def get_tiers_of_tier_list(self, tierlist_id):
        return self.tier_list_repository.find_tiers_by_tier_list(tierlist_id)

    def get_base_dir_path(self):
        return self.image_repository.get_base_dir_path()

    def create_tier_list_template(self, name, tier_data, item_paths):
        tier_list = self.tier_list_repository.create_tier_list(TierList(name))

        item_paths = self.image_repository.check_image_paths(item_paths)

        items = [Item(tier_list.id, path) for path in item_paths]
        self.tier_list_repository.create_items(items)

        tiers = [Tier(tier_list.id, name, rank)
                 for rank, name in tier_data.items()]
        self.tier_list_repository.create_tiers(tiers)


tier_list_service = TierListService()

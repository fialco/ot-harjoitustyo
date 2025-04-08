# from entities.tier_list import TierList

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

    def get_base_dir_path(self):
        return self.image_repository.get_base_dir_path()


tier_list_service = TierListService()

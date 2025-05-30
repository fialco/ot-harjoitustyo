from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier

from repositories.tier_list_repository import (
    tier_list_repository as default_tier_list_repository
)

from repositories.image_repository import (
    image_repository as default_image_repository
)


class InvalidCredentialsError(Exception):
    pass


class UsernameExistsError(Exception):
    pass


class TierListService:
    """Class, which handles application logic."""

    def __init__(
        self,
        tier_list_repository=default_tier_list_repository,
        image_repository=default_image_repository
    ):
        """Class constructor. Creates service for application logic.

        Args:
            tier_list_repository:
                Optional, by default TierListRepository-object.
                Object, which has methods equivalent to TierListRepository-object.
            image_repository:
                Optional, by default ImageRepository-object.
                Object, which has methods equivalent to ImageRepository-object.
        """

        self.tier_list_repository = tier_list_repository
        self.image_repository = image_repository

    def get_tier_lists(self):
        """Return all tier lists.

        Returns:
            List containing TierList-objects of every tier list.
        """

        return self.tier_list_repository.find_all_tier_lists()

    def get_tier_list(self, tierlist_id):
        """Return a specific tier list.

        Args:
            tierlist_id: Integer of the tier lists id.

        Returns:
            Tier list in TierList-object form.
        """

        return self.tier_list_repository.find_tier_list(tierlist_id)

    def get_items_of_tier_list(self, tierlist_id):
        """Return items of specific to a tier list.

        Args:
            tierlist_id: Integer of the tier lists id.

        Returns:
            List containing Item-objects of every item of a tier list.
        """

        return self.tier_list_repository.find_items_by_tier_list(tierlist_id)

    def get_tiers_of_tier_list(self, tierlist_id):
        """Return tiers of specific to a tier list.

        Args:
            tierlist_id: Integer of the tier lists id.

        Returns:
            List containing Tier-objects of every tier of a tier list.
        """

        return self.tier_list_repository.find_tiers_by_tier_list(tierlist_id)

    def get_base_dir_path(self):
        """Return absolute path to base directory.
        E.g. '/home/user/ot-harjoitustyo/tier-list-app'.

        Returns:
            String of an absolute path to base directory.
        """

        return self.image_repository.get_base_dir_path()

    def get_image(self, image_path):
        """Return a resized image.

        Args:
            image_path: Absolute path to image.

        Returns:
            A PhotoImage-object.
        """

        return self.image_repository.load_image(image_path)

    def text_to_image(self, text):
        """Return a image of an text.

        Args:
            text: Value to be made an image.

        Returns:
            A PhotoImage-object.
        """

        return self.image_repository.text_to_image(text)

    def create_tier_list_template(self, name, tier_data, image_paths):
        """Creates a new tier list template.
        Item paths are checked and if they're not in /data/images,
        then copies of images are made there and that path is used.

        Args:
            name: String of the tier list name.
            tier_data: Dictionary of tiers of tier list.
            image_paths: List of image path strings.

        """

        tier_list = self.tier_list_repository.create_tier_list(TierList(name))

        image_paths = self.image_repository.check_image_paths(image_paths)

        items = [Item(tier_list.id, path) for path in image_paths]
        self.tier_list_repository.create_items(items)

        tiers = [Tier(tier_list.id, name, rank)
                 for rank, name in tier_data.items()]
        self.tier_list_repository.create_tiers(tiers)

    def delete_tier_list(self, tierlist_id):
        """Deletes a tier list and related tiers and items from DB.

        Args:
            tierlist_id: Integer of the tier lists id.
        """

        self.tier_list_repository.delete_tier_list(tierlist_id)

    def take_canvas_screenshot(self, canvas, tier_end):
        """Creates a screenshot of the whole tier list.
        Image is given a random name and saved to data/screenshots/.

        Args:
            canvas:
                TkInter canvas-object.
            tier_end:
                y coordinate for end of tiers
        """

        return self.image_repository.take_canvas_screenshot(canvas, tier_end)


tier_list_service = TierListService()

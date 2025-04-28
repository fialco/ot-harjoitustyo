from database_connection import get_database_connection
from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier


def get_tier_list_by_row(row):
    return TierList(row["name"], row["id"]) if row else None


def get_items_by_row(row):
    return Item(row["tierlist_id"], row["image_path"]) if row else None


def get_tiers_by_row(row):
    return Tier(row["tierlist_id"], row["name"], row["rank"]) if row else None


class TierListRepository:
    """Class, which handles database operations.
    """

    def __init__(self, connection):
        """Class constructor.

        Args:
            connection: Object for database connection.
        """

        self._connection = connection

    def find_all_tier_lists(self):
        """Return all tier lists.

        Returns:
            List containing TierList-objects of every tier list.
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM tierlists")

        rows = cursor.fetchall()

        return list(map(get_tier_list_by_row, rows))

    def find_tier_list(self, tierlist_id):
        """Return a specific tier list.

        Args:
            tierlist_id: Integer of the tier lists id.

        Returns:
            Tier list in TierList-object form.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, name FROM tierlists WHERE id = ?", (tierlist_id,))

        row = cursor.fetchone()

        return get_tier_list_by_row(row)

    def find_items_by_tier_list(self, tierlist_id):
        """Return items of specific to a tier list.

        Args:
            tierlist_id: Integer of the tier lists id.

        Returns:
            List containing Item-objects of every item of a tier list.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM items WHERE tierlist_id = ?", (tierlist_id,))

        rows = cursor.fetchall()

        return list(map(get_items_by_row, rows))

    def find_tiers_by_tier_list(self, tierlist_id):
        """Return tiers of specific to a tier list.

        Args:
            tierlist_id: Integer of the tier lists id.

        Returns:
            List containing Tier-objects of every tier of a tier list.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM tiers WHERE tierlist_id = ?", (tierlist_id,))

        rows = cursor.fetchall()

        return list(map(get_tiers_by_row, rows))

    def create_tier_list(self, tierlist):
        """Creates a new tier list.

        Args:
            tierlist: Tier list to be saved as a TierList-object.

        Returns:
            Saved tier list as a TierList-object.

        """

        cursor = self._connection.cursor()

        cursor.execute(
            "insert into tierlists (name) values (?)",
            (tierlist.name,)
        )

        tierlist.id = cursor.lastrowid

        self._connection.commit()

        return tierlist

    def create_items(self, items):
        """Creates items of a tier list.

        Args:
            items: List of items to be saved as Item-objects.

        Returns:
            Saved items as a list of Item-objects.

        """

        cursor = self._connection.cursor()

        for item in items:
            cursor.execute(
                "insert into items (tierlist_id, image_path) values (?, ?)",
                (item.tierlist_id,
                 item.image_path,)
            )

        self._connection.commit()

        return items

    def create_tiers(self, tiers):
        """Creates tiers of a tier list.

        Args:
            tiers: List of iters to be saved as Iter-objects.

        Returns:
            Saved iters as a list of Tier-objects.

        """

        cursor = self._connection.cursor()

        for tier in tiers:
            cursor.execute(
                "insert into tiers (tierlist_id, name, rank) values (?, ?, ?)",
                (tier.tierlist_id,
                 tier.name,
                 tier.rank,)
            )

        self._connection.commit()

        return tiers

    def delete_all(self):
        """Delete all from tables
        """

        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM tierlists")
        cursor.execute("DELETE FROM items")
        cursor.execute("DELETE FROM tiers")

        self._connection.commit()

    def delete_tier_list(self, tierlist_id):
        """Deletes a tier list and related tiers and items from DB.

        Args:
            tierlist_id: Integer of the tier lists id.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "DELETE FROM items WHERE tierlist_id = ?", (tierlist_id,))
        cursor.execute(
            "DELETE FROM tiers WHERE tierlist_id = ?", (tierlist_id,))
        cursor.execute("DELETE FROM tierlists WHERE id = ?", (tierlist_id,))

        self._connection.commit()


tier_list_repository = TierListRepository(get_database_connection())

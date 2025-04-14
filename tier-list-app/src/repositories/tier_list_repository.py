from database_connection import get_database_connection
from entities.tier_list import TierList
from entities.item import Item
from entities.tier import Tier

def get_tier_list_by_row(row):
    return TierList(row["id"], row["name"]) if row else None

def get_items_by_row(row):
    return Item(row["tierlist_id"], row["image_path"]) if row else None

def get_tiers_by_row(row):
    return Tier(row["tierlist_id"], row["name"], row["rank"]) if row else None

class TierListRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all_tier_lists(self):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM tierlists")

        rows = cursor.fetchall()

        return list(map(get_tier_list_by_row, rows))

    def find_tier_list(self, tierlist_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, name FROM tierlists WHERE id = ?", (tierlist_id,))

        row = cursor.fetchone()

        return get_tier_list_by_row(row)

    def find_items_by_tier_list(self, tierlist_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM items WHERE tierlist_id = ?", (tierlist_id,))

        rows = cursor.fetchall()

        return list(map(get_items_by_row, rows))

    def find_tiers_by_tier_list(self, tierlist_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM tiers WHERE tierlist_id = ?", (tierlist_id,))

        rows = cursor.fetchall()

        return list(map(get_tiers_by_row, rows))

    # These are used only for testing for now until functionality added properly to app
    def delete_tier_lists(self):
        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM tierlists")

        self._connection.commit()

    def delete_items(self):
        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM items")

        self._connection.commit()

    def create_tier_list(self, tierlist):
        cursor = self._connection.cursor()

        cursor.execute(
            "insert into tierlists (name) values (?)",
            (tierlist.name,)
        )

        self._connection.commit()

        return tierlist

    def create_item(self, item):
        cursor = self._connection.cursor()

        cursor.execute(
            "insert into items (tierlist_id, image_path) values (?, ?)",
            (item.tierlist_id,
             item.image_path,)
        )

        self._connection.commit()

        return item


tier_list_repository = TierListRepository(get_database_connection())

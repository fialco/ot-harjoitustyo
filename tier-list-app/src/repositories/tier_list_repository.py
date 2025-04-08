from entities.tier_list import TierList
from entities.item import Item
from database_connection import get_database_connection


def get_tier_list_by_row(row):
    return TierList(row["id"], row["name"]) if row else None


def get_items_by_row(row):
    return Item(row["name"], row["image_path"], row["tierlist_id"]) if row else None


class TierListRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM tierlists")

        rows = cursor.fetchall()

        return list(map(get_tier_list_by_row, rows))

    def find_tier_list(self, tierlist_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, name FROM tierlists WHERE id = ?", (tierlist_id))

        row = cursor.fetchone()

        return get_tier_list_by_row(row)

    def find_items_by_tier_list(self, tierlist_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM items WHERE tierlist_id = ?", (tierlist_id,))

        rows = cursor.fetchall()

        return list(map(get_items_by_row, rows))


tier_list_repository = TierListRepository(get_database_connection())

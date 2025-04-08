from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS tierlists;
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS items;
    """)

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE tierlists (
            id INTEGER PRIMARY KEY,
            name text NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE items (
            id INTEGER PRIMARY KEY,
            tierlist_id INTEGER,
            name text NOT NULL,
            image_path TEXT,
            FOREIGN KEY (tierlist_id) REFERENCES tierlists(id)
        );
    """)

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()

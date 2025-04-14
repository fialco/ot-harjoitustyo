from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS tierlists;
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS items;
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS tiers;
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
            image_path TEXT,
            FOREIGN KEY (tierlist_id) REFERENCES tierlists(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE tiers (
            id INTEGER PRIMARY KEY,
            tierlist_id INTEGER,
            name TEXT,
            rank INTEGER,
            FOREIGN KEY (tierlist_id) REFERENCES tierlists(id)
        );
    """)

    connection.commit()


def insert_data(connection):
    cursor = connection.cursor()

    #Tier lists
    cursor.execute("""
        INSERT INTO tierlists (name)
        VALUES ("Programming Languages");
    """)

    cursor.execute("""
        INSERT INTO tierlists (name)
        VALUES ("Movie genres");
    """)

    #Items
    cursor.execute("""
        INSERT INTO items (tierlist_id, image_path)
        VALUES (1, "/data/images/Python-logo.png");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, image_path)
        VALUES (1, "/data/images/ISO_C++_Logo.svg.png");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, image_path)
        VALUES (1, "/data/images/Javascript_Logo.png");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, image_path)
        VALUES (2, "/data/images/comedy.jpg");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, image_path)
        VALUES (2, "/data/images/drama.jpg");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, image_path)
        VALUES (2, "/data/images/horror.jpg");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, image_path)
        VALUES (2, "/data/images/action.jpg");
    """)

    #Tiers
    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (1, "S", 0);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (1, "A", 1);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (1, "B", 2);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (1, "C", 3);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (1, "D", 4);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (2, "5", 0);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (2, "4", 1);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (2, "3", 2);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (2, "2", 3);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (2, "1", 4);
    """)

    cursor.execute("""
        INSERT INTO tiers (tierlist_id, name, rank)
        VALUES (2, "0", 5);
    """)

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)

    insert_data(connection)


if __name__ == "__main__":
    initialize_database()

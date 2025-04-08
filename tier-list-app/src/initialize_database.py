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


def insert_data(connection):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tierlists (name)
        VALUES ("Programming Languages");
    """)

    cursor.execute("""
        INSERT INTO tierlists (name)
        VALUES ("Movie genres");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, name, image_path)
        VALUES (1, "Python", "/data/images/Python-logo.png");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, name, image_path)
        VALUES (1, "C++", "/data/images/ISO_C++_Logo.svg.png");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, name, image_path)
        VALUES (1, "JavaScript", "/data/images/Javascript_Logo.png");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, name, image_path)
        VALUES (2, "Comedy", "/data/images/comedy.jpg");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, name, image_path)
        VALUES (2, "Drama", "/data/images/drama.jpg");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, name, image_path)
        VALUES (2, "Horror", "/data/images/horror.jpg");
    """)

    cursor.execute("""
        INSERT INTO items (tierlist_id, name, image_path)
        VALUES (2, "Action", "/data/images/action.jpg");
    """)

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)

    insert_data(connection)


if __name__ == "__main__":
    initialize_database()

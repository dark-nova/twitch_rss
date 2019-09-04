import sqlite3

import pendulum


def create():
    """Creates the database.

    Returns:
        None

    """
    conn = sqlite3.connect('rss.db')
    c = conn.cursor()
    c.execute(
        """create table entries
        (title text, year integer, month integer, day integer)"""
        )
    conn.commit()
    conn.close()
    return


def check_if_entry_exists(title: str):
    """Checks if an entry is already in the database.

    Args:
        title (str): the entry's URL

    Returns:
        bool: True if the entry exists; False if it doesn't

    """
    conn = sqlite3.connect('rss.db')
    c = conn.cursor()
    try:
        c.execute(
            """select * from entries where title = ?""",
            (title,)
            )
        records = c.fetchall()
        return len(records) > 0
    except sqlite3.OperationalError as e:
        print(f'Exception {e} caught. Recreating database.')
        c.execute('drop table if exists entries')
        conn.commit()
        conn.close()
        create()
        return False


def add_entry(title: str, datetime: pendulum.datetime):
    """Adds an entry to the database.

    Args:
        title (str): the entry's URL
        datetime (pendulum.datetime): the date of the entry

    Returns:
        None

    """
    datetime = datetime.in_tz('UTC')
    conn = sqlite3.connect('rss.db')
    c = conn.cursor()
    c.execute(
        """insert into entries values
        (?, ?, ?, ?)""",
        (title, datetime.year, datetime.month, datetime.day)
        )
    conn.commit()
    conn.close()
    return


def get_entry_time(title: str):
    """Gets the time for an entry.

    Args:
        title (str): the entry's URL

    Returns:
        pendulum.datetime.Datetime: an appropriate datetime

    Raises:
        Exception: if the table was corrupt

    """
    conn = sqlite3.connect('rss.db')
    c = conn.cursor()
    try:
        c.execute(
            """select * from entries where title = ?""",
            (title,)
            )
        record = c.fetchone()
        return pendulum.datetime(*record[1:], tz = 'UTC')
    except sqlite3.OperationalError as e:
        print(f'Exception {e} caught. Recreating database.')
        c.execute('drop table if exists entries')
        conn.commit()
        conn.close()
        create()
        raise Exception('Table recreated')


def purge_old():
    conn = sqlite3.connect('rss.db')
    c = conn.cursor()
    c.execute(
        """delete from entries where title not in
        (select title from entries order by year desc, month desc, day desc
        limit 20)
        """
        )
    conn.commit()
    conn.close()
    return


if __name__ == '__main__':
    create()

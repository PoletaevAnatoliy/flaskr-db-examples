import sqlite3

import click
from flask import current_app
from flask import g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_user_by_id(id_):
    return get_db().execute("""
        SELECT * FROM user WHERE id = ?;
    """, (id_,)).fetchone()


def get_user_by_username(username):
    return get_db().execute("""
        SELECT * FROM user WHERE username = ?;
    """, (username,)).fetchone()


class UserAlreadyExists(Exception):
    pass


def register_user(username, password):
    db = get_db()
    try:
        db.execute("""
            INSERT INTO user (username, password) VALUES (?, ?);
        """, (username, password))
        db.commit()
    except db.IntegrityError:
        raise UserAlreadyExists()


def get_all_posts():
    return get_db().execute("""
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        ORDER BY created DESC;
    """).fetchall()


def get_post_by_id(id_):
    return get_db().execute("""
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.id = ?;
    """, (id_,)).fetchone()


def add_post(title, body, author_id):
    db = get_db()
    db.execute("""
        INSERT INTO post (title, body, author_id) VALUES (?, ?, ?);
    """, (title, body, author_id))
    db.commit()


def update_post(id_, title, body):
    db = get_db()
    db.execute("""
        UPDATE post SET title = ?, body = ? WHERE id = ?;
    """, (title, body, id_))
    db.commit()


def delete_post(id_):
    db = get_db()
    db.execute("""
        DELETE FROM post WHERE id = ?;
    """, (id_,))
    db.commit()

from flaskr.db import get_db


class User:

    def __init__(self, id_, username, password_hash):
        self._id = id_
        self._username = username
        self._password_hash = password_hash

    @staticmethod
    def register(username, password_hash):
        db = get_db()
        try:
            db.execute("""
                INSERT INTO user (username, password) VALUES (?, ?);
            """, (username, password_hash))
            db.commit()
        except db.IntegrityError:
            raise UserAlreadyExists()
        return User.with_username(username)

    def username(self):
        return self._username

    def password_hash(self):
        return self._password_hash

    def id(self):
        return self._id

    @staticmethod
    def with_id(id_):
        data = get_db().execute("""
            SELECT id, username, password FROM user WHERE id = ?;
        """, (id_,)).fetchone()
        return User(data["id"], data["username"], data["password"])

    @staticmethod
    def with_username(username):
        data = get_db().execute("""
            SELECT id, username, password FROM user WHERE username = ?;
        """, (username,)).fetchone()
        if data is None:
            return None
        return User(data["id"], data["username"], data["password"])


class UserAlreadyExists(Exception):
    pass


class Post:

    def __init__(self, id_, title, body, author, created):
        self._id = id_
        self._title = title
        self._body = body
        self._author = author
        self._created = created

    @staticmethod
    def create(title, body, author):
        db = get_db()
        db.execute("""
            INSERT INTO post (title, body, author_id) VALUES (?, ?, ?);
        """, (title, body, author.id()))
        db.commit()

    def update(self, title, body):
        db = get_db()
        db.execute("""
            UPDATE post SET title = ?, body = ? WHERE id = ?;
        """, (title, body, self.id()))
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("""
            DELETE FROM post WHERE id = ?;
        """, (self.id(),))
        db.commit()

    def id(self):
        return self._id

    def title(self):
        return self._title

    def body(self):
        return self._body

    def author(self):
        return self._author

    def created(self):
        return self._created

    @staticmethod
    def all():
        posts = get_db().execute("""
            SELECT id, title, body, created, author_id
            FROM post ORDER BY created DESC;
        """).fetchall()
        return [Post(p["id"], p["title"], p["body"],
                     User.with_id(p["author_id"]), p["created"])
                for p in posts]

    @staticmethod
    def with_id(id_):
        data = get_db().execute("""
            SELECT id, title, body, created, author_id
            FROM post WHERE id = ?
        """, (id_,)).fetchone()
        if data is None:
            return None
        return Post(data["id"], data["title"], data["body"],
                    User.with_id(data["author_id"]), data["created"])

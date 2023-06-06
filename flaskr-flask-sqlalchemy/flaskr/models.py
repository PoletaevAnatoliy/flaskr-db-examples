from flaskr import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", back_populates="author")

    def __init__(self, username=None, password_hash=None):
        self.username = username
        self.password_hash = password_hash


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(265))
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User", back_populates="posts")

    def __init__(self, title=None, body=None, author=None):
        self.title = title
        self.body = body
        self.author_id = author.id

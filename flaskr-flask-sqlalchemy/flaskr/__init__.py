import os

import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db():
    db.create_all()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.config['DATABASE']}"

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    from flaskr import models

    app.cli.add_command(init_db_command)

    with app.app_context():
        init_db()

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # apply the blueprints to the app
    from flaskr import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database")


from flaskr import db


def test_get_close_db(app):
    with app.app_context():
        connection = db.session.connection().connection
        assert connection is db.session.connection().connection

    assert connection.driver_connection is None


def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskr.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called

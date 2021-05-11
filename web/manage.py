from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()
cli = FlaskGroup(app)


@cli.command("load_dummy_db")
def load_dummy_db():
    pass
    # db.drop_all()
    # db.create_all()
    # db.session.commit()


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()

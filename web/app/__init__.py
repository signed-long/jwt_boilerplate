from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
from flask_bcrypt import Bcrypt
from app.config import config_options
import os
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
# mail = Mail()


def create_app():

    app = Flask(__name__)
    app.config.from_object(config_options[os.environ.get('FLASK_ENV')])

    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    # mail.init_app(app)

    from app.bp_auth.routes import bp_auth
    from app.bp_errors.handlers import bp_errors

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_errors)

    return app

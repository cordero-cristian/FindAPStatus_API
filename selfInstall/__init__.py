import logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from selfInstall.config import getConfig

from RuckusFunctions import sdkRND_API

apiND = sdkRND_API.clsSdkRndAPI()
logging.getLogger("paramiko").setLevel(logging.WARNING)

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def createApp(configName):
    app = Flask("self-install-api")
    app.config.from_object(getConfig(configName))

    from selfInstall.api import apiBp
    app.register_blueprint(apiBp)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app

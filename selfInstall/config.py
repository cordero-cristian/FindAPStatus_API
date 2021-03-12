import os
from pathlib import Path


here = Path(__file__).parent
sqliteDev = "sqlite:///" + str(here / "selfInstallApiDev.db")
sqliteProd = "sqlite:///" + str(here / "selfInstallApiProd.db")


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY",)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", sqliteDev)


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", sqliteProd)
    PRESERVE_CONTEXT_ON_EXCEPTION = True


envConfigDict = dict(development=DevelopmentConfig)


def getConfig(configName):
    return envConfigDict.get(configName, ProductionConfig)

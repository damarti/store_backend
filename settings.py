import os
from os.path import join, dirname
from dotenv import load_dotenv

# Database
_DOTENV_PATH = join(dirname(__file__), ".env")
load_dotenv(_DOTENV_PATH)

DEV_SQL_DB_NAME = os.environ.get("DEV_SQL_DB_NAME")
DEV_SQL_USER = os.environ.get("DEV_SQL_USER")
DEV_SQL_PASS = os.environ.get("DEV_SQL_PASS")
DEV_SQL_HOST = os.environ.get("DEV_SQL_HOST")

dev_mysql_uri = "mysql://{}:{}@{}/{}".format(
    DEV_SQL_USER,
    DEV_SQL_PASS,
    DEV_SQL_HOST,
    DEV_SQL_DB_NAME
)

GRAPHQL_ENDPOINT = os.environ["GRAPHQL_ENDPOINT"]
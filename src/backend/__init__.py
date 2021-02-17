SECRET="change me"

from datetime import timedelta
import secrets
from flask_sqlalchemy import SQLAlchemy


EXPIRATION_AFTER= timedelta(days=7)
db = SQLAlchemy()

SECRET="change me"



from datetime import timedelta
import secrets
from flask_sqlalchemy import SQLAlchemy


EXPIRATION_AFTER= timedelta(days=7)
db = SQLAlchemy()

try:
	from .models import * #(db, Product, Order,User,Image)
	from .functions import *
	from .auth import *
	from .app import *
	from .test import *
except:
	from models import (db, Product, Order,User,Image)
	from functions import *
	from auth import *
	from app import *


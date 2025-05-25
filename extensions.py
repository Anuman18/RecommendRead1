# extensions.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Custom base class
class Base(DeclarativeBase):
    pass

# Export the database object
db = SQLAlchemy(model_class=Base)

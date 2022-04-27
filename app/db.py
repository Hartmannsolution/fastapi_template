from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL, # connect_args={"check_same_thread": False} # only for sqllite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # The base class to be extended by all future entity classes / Models.


# import os

# from sqlalchemy import (
#     Column,
#     DateTime,
#     Integer,
#     MetaData, # For creating the database schema.
#     String,
#     Table,
#     create_engine
# )
# from sqlalchemy.sql import func

# from databases import Database

# DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)

# # SQLAlchemy
# engine = create_engine(DATABASE_URL)
# metadata = MetaData()
# notes = Table(
#     "notes",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("title", String(50)),
#     Column("description", String(50)),
#     Column("created_date", DateTime, default=func.now(), nullable=False),
# )

# # databases query builder
# database = Database(DATABASE_URL)


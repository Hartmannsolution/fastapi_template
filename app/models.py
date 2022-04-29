# Models where the entity classes lives. These are sqlalchemy models (not to confuse with pydantic models in schema.py). These are used in the facade class and are created in the main.py class with: models.Base.metadata.create_all(bind=engine)
from sqlalchemy import (
Boolean,
Column,
ForeignKey,
Integer,
String,
Table, # Used only in ManyToMany associations
)
from sqlalchemy.orm import relationship, Session # Used only for showing commit rollback example
# used for creating OneToMany with foreign keys
from .db import Base                    # imported from sqlalchemy is the class for all entities to inherit

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    
    def __repr__(self): # just for testing purpose
        return f'User({self.id},{self.email})'
    

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

# OneToMany Uni-directional: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child") # One Parent to Many Children

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(
        Integer, 
        ForeignKey('parent.id')
        ) # Child has the foreigneky to Parent id

# OneToMany Bi-directional: 
class Parent2(Base):
    __tablename__ = 'parent2'
    id = Column(Integer, primary_key=True)
    children = relationship(
        "Child2", back_populates="parent2",
        cascade="all, delete",
        passive_deletes=True
    ) # Now we have bi-directional and cascade delete.

class Child2(Base):
    __tablename__ = 'child2'
    id = Column(Integer, primary_key=True)
    parent2_id = Column(Integer, ForeignKey('parent2.id')) # We can see that Child is the owning side here
    parent2 = relationship("Parent2", back_populates="children")

# MANY TO MANY
association_table = Table('association', Base.metadata,
    Column('parent3_id', ForeignKey('parent3.id')),
    Column('child3_id', ForeignKey('child3.id'))
)

class Parent3(Base):
    __tablename__ = 'parent3'
    id = Column(Integer, primary_key=True)
    children = relationship("Child3",
                    secondary=association_table)

class Child3(Base):
    __tablename__ = 'child3'
    id = Column(Integer, primary_key=True)

# def commit_entities(engine, *args):
#     # create session and add objects
#     with Session(engine) as session:
#         with session.begin():
#             for obj in args:
#                 session.add(obj)
#         # inner context calls session.commit(), if there were no exceptions
#     # outer context calls session.close()



if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://dev:ax2@db:5432/app', echo=True)
    Base.metadata.drop_all(engine) # remove all tables
    # or drop single table: User.__table__.drop()
    Base.metadata.create_all(engine)

    # commit_entities(engine, Child3(),Parent3())


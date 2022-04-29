from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

if __name__ == "__main__":
    engine = create_engine(
        "postgresql://dev:ax2@db:5432/app", # connect_args={"check_same_thread": False} # only for sqllite
    )
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)() # create a database session, that can be closed after use. For use of session pool - see: main.get_db() with yield and finally block.
    result = get_users(db = db, skip=1, limit=2)
    print(result)
    result = get_user_by_email(db=db, email="nextmail")
    print(result)
    result = create_user_item(db = db, item=schemas.ItemCreate(title="new title",description="descriiiiiiiiiiiiption"), user_id=3)
    print(result)
    result = get_items(db,0,2)
    print(result)
    db.close()
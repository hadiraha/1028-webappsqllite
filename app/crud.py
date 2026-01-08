from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password

def create_user(db: Session, data: schemas.UserCreate):
    hashed = hash_password(data.password)
    user = models.User(username=data.username, hashed_password=hashed, role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_companies(db: Session):
    return db.query(models.Company).all()

def create_company(db: Session, data: schemas.CompanyCreate):
    clean = {k: (None if v in ["", None] or str(v) == "nan" else v)
             for k, v in data.dict().items()}
    item = models.Company(**clean)
    db.add(item)
    return item

def update_company(db: Session, id: int, data: schemas.CompanyCreate):
    obj = db.query(models.Company).filter(models.Company.id==id).first()
    for key, value in data.dict().items():
        setattr(obj, key, value)
    db.commit()
    return obj

def delete_company(db: Session, id: int):
    obj = db.query(models.Company).filter(models.Company.id==id).first()
    db.delete(obj)
    db.commit()
from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company
from app.auth import get_current_user
from app.crud import create_company
from app.schemas import CompanyCreate
import pandas as pd
import math
import os
from app.utils import base_path


router = APIRouter()

UPLOAD_DIR = os.path.join(base_path(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# def token_required(Authorization: str = Header(None), db: Session = Depends(get_db)):
#     if Authorization is None:
#         raise HTTPException(status_code=401, detail="Missing token")
#     token = Authorization.replace("Bearer ", "")
#     user = get_current_user(token, db)
#     return user


def clean_value(v):
    return None if (v is None or (isinstance(v, float) and math.isnan(v))) else v

@router.get("/")
def get_list(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Company).all()

@router.get("/")
def get_list(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Company).all()



@router.post("/")
def add_company(data: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    obj = Company(**data)
    db.add(obj)
    db.commit()
    return {"status": "created"}


# -----------------------------------------------------
# UPLOAD EXCEL AND INSERT INTO DB
# -----------------------------------------------------
@router.post("/upload")
async def upload_excel(
        file: UploadFile = File(...),
        user=Depends(get_current_user),
        db: Session = Depends(get_db),
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_excel(file_path)
    df = df.where(pd.notnull(df), None)

    for _, row in df.iterrows():
        row_dict = {k: None if pd.isna(v) else v for k,v in row.items()}
        create_company(db, CompanyCreate(**row_dict))
    db.commit()
    return {"status": "ok", "imported_rows": len(df)}
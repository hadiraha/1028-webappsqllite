from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
import os
import math

from app.database import get_db
from app.models import Company
from app.auth import get_current_user
from app.crud import create_company, delete_all_companies
from app.schemas import CompanyCreate
from app.utils import base_path


router = APIRouter()

UPLOAD_DIR = os.path.join(base_path(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------------------------------
# HELPERS
# -----------------------------------------------------
def clean_value(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


# -----------------------------------------------------
# GET ALL COMPANIES
# -----------------------------------------------------
@router.get("/")
def get_companies(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Company).all()


# -----------------------------------------------------
# DELETE ALL COMPANIES (BUTTON ACTION)
# -----------------------------------------------------
@router.delete("/delete-all")
def delete_all_endpoint(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_all_companies(db)
    return {"status": "ok", "message": "All companies deleted"}


# -----------------------------------------------------
# ADD SINGLE COMPANY (OPTIONAL)
# -----------------------------------------------------
@router.post("/")
def add_company(
    data: dict,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = Company(**data)
    db.add(obj)
    db.commit()
    return {"status": "created"}


# -----------------------------------------------------
# UPLOAD EXCEL (REPLACE ALL DATA)
# -----------------------------------------------------
@router.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # delete existing data FIRST
    delete_all_companies(db)

    # read excel
    df = pd.read_excel(file_path)
    df = df.where(pd.notnull(df), None)

    # insert new data
    for _, row in df.iterrows():
        row_dict = {}

        for k, v in row.items():
            if pd.isna(v):
                row_dict[k] = None
            elif k == "file_number":
                row_dict[k] = str(v)   # FORCE STRING
            else:
                row_dict[k] = v

        create_company(db, CompanyCreate(**row_dict))
    db.commit()

    return {
        "status": "ok",
        "mode": "replace_all",
        "imported_rows": len(df),
    }
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.database import Base, engine, SessionLocal
from app.models import User
from app.auth import hash_password
from app.utils import base_path
import os

# ----------------------------------------
# DB init
# ----------------------------------------
Base.metadata.create_all(bind=engine)

def create_first_admin():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                hashed_password=hash_password("123456"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("Default admin created")
    finally:
        db.close()

create_first_admin()

# ----------------------------------------
app = FastAPI(title="Project System API")

STATIC_DIR = os.path.join(base_path(), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes_users import router as users_router
from app.routes_companies import router as companies_router

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(companies_router, prefix="/companies", tags=["Companies"])

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/static/login.html")
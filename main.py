from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from .models import BankCheck

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Bank Check API Running"}

@app.post("/save")
def save_check(data: dict, db: Session = Depends(get_db)):

    new_check = BankCheck(
        bank_name=data.get("Bank_Name"),
        account_name=data.get("Account_Name"),
        account_number=data.get("Account_Number"),
        amount=data.get("Amount"),
        date=data.get("Date")
    )

    db.add(new_check)
    db.commit()
    db.refresh(new_check)

    return {"message": "Data Saved Successfully"}
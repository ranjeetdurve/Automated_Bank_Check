from sqlalchemy import Column, Integer, String, Float
from .database import Base

class BankCheck(Base):
    __tablename__ = "bank_checks"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String)
    account_name = Column(String)
    account_number = Column(String)
    amount = Column(Float)
    date = Column(String)
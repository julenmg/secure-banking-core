from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="accounts")

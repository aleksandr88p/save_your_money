from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)

    purchases = relationship("Purchase", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    currency = Column(String, nullable=True)  # Теперь currency может быть NULL
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="purchases")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="transactions")

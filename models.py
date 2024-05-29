from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    allow_email = Column(Boolean, default=True)
    allow_phone = Column(Boolean, default=True)

    contacts = relationship("Contact", back_populates="managed_by")
    accounts = relationship("Network_Account", back_populates="managed_by")


class Network_Account(Base):
    __tablename__ = "network_accounts"

    id = Column(Integer, primary_key=True)
    account_name = Column(String)
    last_update = Column(Date)
    network_id = Column(Integer, ForeignKey("networks.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    managed_by = relationship("User", back_populates="accounts")
    network = relationship("Network")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email_address = Column(String, unique=True, index=True)
    phone_number = Column(String)
    allow_email = Column(Boolean, default=False)
    allow_phone = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    managed_by = relationship("User", back_populates="contacts")


class Network(Base):
    __tablename__ = "networks"

    id = Column(Integer, primary_key=True)
    network_name = Column(String, unique=True)
    days_to_deactivate = Column(Integer)
    link = Column(String)
    actions = Column(String)

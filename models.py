from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

import database

class Roles(database.Base):
    __tablename__ = "roles"
    users = relationship("Task", back_populates="users")

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    permissions = Column(String, nullable=False)


class User(database.Base):
    __tablename__ = "users"
    profiles = relationship("Task", back_populates="profiles")

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class UserProfile(database.Base):
    __tablename__ = "profiles"
    roles = relationship("Task", back_populates="roles")

    id = Column(Integer, primary_key=True, index=True)
    fist_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    permissions = Column(String, nullable=False)
    profile_description = Column(String)



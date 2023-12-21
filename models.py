from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

import database

# class Roles(database.Base):
#     __tablename__ = "roles"
#     owner = relationship("User", back_populates="role")
#
#     id = Column(Integer, primary_key=True, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     name = Column(String, nullable=False)
#     permissions = Column(String, nullable=False)


class User(database.Base):
    __tablename__ = "users"

    profile = relationship("UserProfile", back_populates="owner")
    # role = relationship("Roles", back_populates="owner")

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class UserProfile(database.Base):
    __tablename__ = "profiles"
    owner = relationship("User", back_populates="profile")

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    fist_name = Column(String, index=True)
    last_name = Column(String, index=True)
    permissions = Column(String, index=True)
    # profile_description = Column(String, index=True)
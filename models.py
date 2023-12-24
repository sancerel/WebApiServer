from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import database


class User(database.Base):
    __tablename__ = "users"
    profiles = relationship("Profile", back_populates="owner")
    roles = relationship("Role", back_populates="owner")

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False)
    email = Column(String, index=True)
    password = Column(String, index=True)



class Profile(database.Base):
    __tablename__ = "profiles"
    owner = relationship("User", back_populates="profiles")

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    profile_description = Column(String, index=True)


class Role(database.Base):
    __tablename__ = "roles"
    owner = relationship("User", back_populates="roles")

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    permissions = Column(String, index=True)

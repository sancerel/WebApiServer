from pydantic import BaseModel


class EmptyProfile(BaseModel):
    first_name: str
    last_name: str
    profile_description: str | None = None


class ProfileCreate(EmptyProfile):
    pass


class Profile(EmptyProfile):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class EmptyRole(BaseModel):
    name: str
    permissions: str


class RoleCreate(EmptyRole):
    pass


class Role(EmptyRole):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    profiles: list[Profile] = []
    role: list[Role] = []

    class Config:
        from_attributes = True


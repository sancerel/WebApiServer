from pydantic import BaseModel


class EmptyProfile(BaseModel):
    first_name: str
    last_name: str
    profile_description: str | None = None


class ProfileCreate(EmptyProfile):
    pass


class UserProfile(EmptyProfile):
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
    profile: list[UserProfile] = []

    class Config:
        from_attributes = True


# class RoleBase(BaseModel):
#     id: int
#     role_id: int
#
#     class Config:
#         from_attributes = True
#
#
# class CreateRole(RoleBase):
#     nane: str
#     permissions: str

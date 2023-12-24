from sqlalchemy.orm import Session
import models, schemas


# Create
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(password=user.password, username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_profile(db: Session, profile: schemas.ProfileCreate, user_id: int):
    try:
        db_profile = models.Profile(**profile.model_dump(), owner_id=user_id)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except:
        print('Can\'t add profile')
        return


def create_user_role(db: Session, role: schemas.RoleCreate, user_id: int):
    try:
        db_role = models.Role(**role.model_dump(), owner_id=user_id)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    except:
        print('Can\'t add role')
        return


# Read
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def get_profiles(db: Session):
    return db.query(models.Profile).all()


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_roles(db: Session):
    return db.query(models.Role).all()


# Update
def update_profile_by_id(db: Session, profile_id: str, profile: schemas.ProfileCreate):
    profile_upd = get_profile(db=db, profile_id=int(profile_id))

    profile_upd.first_name = profile.first_name
    profile_upd.last_name = profile.last_name
    profile_upd.profile_description = profile.profile_description
    db.add(profile_upd)
    db.commit()
    db.refresh(profile_upd)
    return


def update_role_by_id(db: Session, role_id: str, role: schemas.RoleCreate):
    role_upd = get_role(db=db, role_id=int(role_id))

    role_upd.name = role.name
    role_upd.permissions = role.permissions
    db.add(role_upd)
    db.commit()
    db.refresh(role_upd)
    return


# Delete
def delete_profile_by_id(db: Session, profile_id: str):
    profile = get_profile(db=db, profile_id=int(profile_id))
    db.delete(profile)
    db.commit()
    return


def delete_role_by_id(db: Session, role_id: str):
    role = get_role(db=db, role_id=int(role_id))
    db.delete(role)
    db.commit()
    return


def delete_user_by_id(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    profiles = db.query(models.Profile).filter(models.Profile.owner_id == int(user_id)).first()
    roles = db.query(models.Role).filter(models.Role.owner_id == int(user_id)).first()
    db.delete(user)
    db.commit()
    db.delete(profiles)
    db.commit()
    db.delete(roles)
    db.commit()
    return

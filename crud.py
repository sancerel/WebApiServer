from sqlalchemy.orm import Session

import models, schemas


# Create
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password, user_name=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# firstname=profile.first_name, lastname=profile.last_name,
#                                      profile_description=profile.profiledescription
def create_user_profile(db: Session, profile: schemas.ProfileCreate, user_id: int):
    try:
        db_item = models.UserProfile(**profile.model_dump(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except:
        print('Can\'t add profile')
        return


# Read
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_profile(db: Session, profile_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.id == profile_id).first()


def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserProfile).all()


# Update
def update_profile_by_id(db: Session, profile_id: str, profile: schemas.ProfileCreate):
    profile_current = get_profile(db=db, profile_id=int(profile_id))

    profile_current.fist_name = profile.fist_name
    profile_current.last_name = profile.last_name
    profile_current.profile_description = profile.profile_description
    db.add(profile_current)
    db.commit()
    db.refresh(profile_current)
    return


# Delete
def delete_profile_by_id(db: Session, profile_id: str):
    profile = get_profile(db=db, profile_id=int(profile_id))
    db.delete(profile)
    db.commit()
    return

from typing import Annotated

import uvicorn
from fastapi import FastAPI, Header, Request, Response, HTTPException
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware
import models
import database
import schemas
import crud

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="WebApiService"
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/user/create')
async def create_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    try:
        crud.create_user(db=db, user=user)
        response.status_code = status.HTTP_200_OK

    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response

@app.get("/pofiless/fetch/all")
def read_profiles(request:Request, db: Session = Depends(get_db)):
    return db.query(models.UserProfile).all()


@app.post('/profiles/add/{user_id}')
async def create_profile(user_id: str, profile: schemas.ProfileCreate, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    try:
        crud.create_user_profile(db=db, profile=profile, user_id=user_id)
        response.status_code = status.HTTP_200_OK
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
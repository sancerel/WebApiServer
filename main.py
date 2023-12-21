from typing import Annotated
from fastapi import FastAPI, Header, Request, Response, HTTPException
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

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
        user = crud.create_user(db=db, user=user)
        response.status_code = status.HTTP_200_OK

    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response

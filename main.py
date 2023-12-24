from fastapi import Depends, FastAPI, Response, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect, WebSocket

import database
import crud, models, schemas


database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


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

#read
@app.get("/profiles/take/all")
def read_profiles(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Profile).all()

@app.get("/role/take/all")
def read_role(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Role).all()

#create
@app.post("/profiles/add/{user_id}")
async def create_profile(user_id: str, profile: schemas.ProfileCreate, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    try:
        crud.create_user_profile(db=db, profile=profile, user_id=user_id)
        response.status_code = status.HTTP_200_OK
        await send_notification("Профиль создан")
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


@app.post("/roles/add/{user_id}")
async def create_role(user_id: str, role: schemas.RoleCreate, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    try:
        crud.create_user_role(db=db, role=role, user_id=user_id)
        response.status_code = status.HTTP_200_OK
        await send_notification("Роль создана")
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


@app.post('/users/create')
async def create_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    try:
        crud.create_user(db=db, user=user)
        response.status_code = status.HTTP_200_OK
        await send_notification("Пользователь создан")
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response



#delete
@app.delete("/profiles/delete/{profile_id}")
async def delete_profile(profile_id: str, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    try:
        crud.delete_profile_by_id(db=db, profile_id=profile_id)
        response.status_code = status.HTTP_200_OK
        await send_notification("Профиль удалён")
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


@app.delete("/roles/delete/{role_id}")
async def delete_role(role_id: str, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    try:
        crud.delete_role_by_id(db=db, role_id=role_id)
        response.status_code = status.HTTP_200_OK
        await send_notification("Роль удалёна")
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: str, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    try:
        crud.delete_user_by_id(db=db, user_id=user_id)
        response.status_code = status.HTTP_200_OK
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response

#update
@app.put("/profiles/update/{profile_id}")
async def update_profile(profile_id: str, profile: schemas.ProfileCreate, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    try:
        crud.update_profile_by_id(db, profile_id, profile)
        response.status_code = status.HTTP_200_OK
        await send_notification("Профиль обновлён")
    except:
        response.status_code = status.HTTP_404_NOT_FOUND

    return response


@app.put("/roles/update/{role_id}")
async def update_role(role_id: str, role: schemas.RoleCreate, response: Response, db: Session = Depends(get_db)):
    response = Response()
    response.headers.append('Access-Control-Allow-Origin', '*')
    response.headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.append('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    try:
        crud.update_role_by_id(db, role_id, role)
        response.status_code = status.HTTP_200_OK
        await send_notification("Роль обновлена")
    except:
        response.status_code = status.HTTP_404_NOT_FOUND

    return response


connected_clients = []


async def send_notification(message):
    for client in connected_clients:
        await client.send_text(message)



#Websockets
@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    while True:
        try:
            data = await websocket.receive_text()
            await send_notification(data)
        except WebSocketDisconnect:
            connected_clients.remove(websocket)
        except:
            pass
            break


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
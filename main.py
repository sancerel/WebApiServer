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


@app.get("/")
async def get():
    return HTMLResponse(html)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebApi</title>
        <script src="jquery-3.7.1.min.js"></script>
    </head>
    <body>
        <form method="post" action="http://127.0.0.1:8000/users/create" onsubmit="">
          <div>
            <h1>Register User</h1>
            <p>Please fill in this form to create an account.</p>
            <hr>
            <label><b>Email</b></label>
            <input type="text" name="email" id="email" required>
            <label><b>Username</b></label>
            <input type="text" name="username" id="username" required>
            <label><b>Password</b></label>
            <input type="password" name="password" id="psw" required>
            <hr>
            <button type="submit">Register</button>
          </div>
        </form>
        <ul id='users'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var users = document.getElementById('users')
                var user = document.createElement('li')
                var content = document.createTextNode(event.data)
                user.appendChild(content)
                users.appendChild(user)
            };
            function sendMessage(event) {
                var email = document.getElementById("email")
                var userName = document.getElementById("username")
                var password = document.getElementById("psw")
                ws.send("Пользователь создан")
                email.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
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

from fastapi import FastAPI, Response, Request, status, Cookie, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic import BaseModel
import sqlite3
import hashlib
import os
from dotenv import dotenv_values
import random
from hashlib import sha256
app = FastAPI()
security = HTTPBasic()

app.secret_key = os.getenv("SECRET")
# app.secret_key = app.config[]
app.session_token = ''

@app.get("/")
def root():
    return {"message": "Hello World"}

class ContentRequest(BaseModel):
	content: str

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("textsdb.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")

@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/texts/{id}")
async def texts(id: str):
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    data = cursor.execute("""
                          SELECT Content, Views
                          FROM Texts
                          WHERE ID = ?
                          """,  (id,)).fetchone()
    if data == None:
    	raise HTTPException(status_code=404, detail="Product not found")
    views = data['Views']
    app.db_connection.execute("UPDATE Texts SET Views = (?) where ID = ?", (views+1,id,))
    app.db_connection.commit()
    return {"Content": data['Content'], "Views": data['Views']}

@app.put("/texts/{id}")
async def update(request: ContentRequest, id: int):
	content = request.content;
	app.db_connection.row_factory = sqlite3.Row
	count = app.db_connection.execute("SELECT Count(*) as C FROM Texts WHERE ID = ?", (id,)).fetchone()
	if count['C'] == 0:
		raise HTTPException(status_code=404, detail="Text not found")
	app.db_connection.execute("UPDATE Texts SET Content = (?), Views = 0 where id = ?", (content,id,))
	app.db_connection.commit()
	return {
		"id": id,
		"New content": content
	}

@app.delete("/texts/{id}")
async def delete(id: int):
	app.db_connection.row_factory = sqlite3.Row
	count = app.db_connection.execute("SELECT Count(*) as C FROM Texts WHERE ID = ?", (id,)).fetchone()
	if count['C'] == 0:
		raise HTTPException(status_code=404, detail="Text not found")
	app.db_connection.execute("DELETE FROM Texts WHERE ID = ?",(id,))
	app.db_connection.commit()
	return "Deleted"

@app.post("/texts")
async def insert(response: Response, request: ContentRequest):
	content = request.content
	cursor = app.db_connection.execute(f"INSERT INTO Texts (Content, Views) VALUES (?, ?)", (content,0))
	app.db_connection.commit()
	last_id = int(cursor.lastrowid)
	response.status_code = 201
	return {
		"id": last_id,
		"Content": content
	}

@app.post("/register")
async def insert(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	salt, key = get_hashed_password(credentials.password, generate_salt())
	cursor = app.db_connection.execute(f"INSERT INTO users (username, hashedPassword, salt) VALUES(?, ?, ?)", (credentials.username, key, salt))
	app.db_connection.commit()
	response.status_code = 201
	return "Success"

@app.post("/login")
async def login_token(request: Request, response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	if check_credentials(credentials.password, credentials.username):
		token = generate_token(credentials)
		store_token(token)
		response.status_code = 201
		return {"token": token}
	else:
		response.status_code = 401	

@app.get("/check")
async def check_login(token: str):
	return check_session(token)


def generate_token(credentials: HTTPBasicCredentials):
	seed = credentials.username + credentials.password + str(random.randint(0, 1000)) + app.secret_key
	return sha256(seed.encode()).hexdigest()

def store_token(token: str):
	if token != app.session_token:
		app.session_token = token

def get_hashed_password(password: str, salt: str):
	key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
	return key

def check_session(token: str):
	if token == app.session_token:
		return True
	return False

def generate_salt():
	return os.urandom(32)

def check_credentials(password: str, username: str):
	cursor = app.db_connection.cursor()
	cursor.row_factory = sqlite3.Row
	data = cursor.execute("""
                          SELECT hashedPassword, salt
                          FROM users
                          WHERE username = ?
                          """,  (username,)).fetchone()
	if data == None:
		raise HTTPException(status_code=404, detail="User not found")
	password_from_db = data['hashedPassword']
	salt = data['salt']
	new_hashed_password = get_hashed_password(password, salt)
	if password_from_db == new_hashed_password:
		return True
	else:
		return False


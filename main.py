
from fastapi import FastAPI, Response, Request, status, Cookie, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic import BaseModel
import sqlite3
app = FastAPI()

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


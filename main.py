
from fastapi import FastAPI, Response, Request, status, Cookie
import sqlite3
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("textsdb.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

@app.get("/texts")
async def categories():
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    data = cursor.execute("""
                          SELECT *
                          FROM Texts
                          """).fetchall()
    return data
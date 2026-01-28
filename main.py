from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import os,sqlite3
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DB_PATH=os.path.join(BASE_DIR,"database.db")

import sqlite3

app=FastAPI()

def db():
    connection=sqlite3.connect(DB_PATH)
    cursor=connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, email TEXT, message TEXT)""")

    connection.commit()
    connection.close()


db()

class Contact(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.post("/contact")
def submit_contact(data: Contact):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",(data.name, data.email, data.message) 
    )
    connection.commit()
    connection.close()
    return {"status": "success","message":"saved"}

@app.get("/contacts")
def list():
    connection=sqlite3.connect(DB_PATH)
    cursor=connection.cursor()

    cursor.execute("SELECT id, name, email, message FROM contacts")
    rows=cursor.fetchall()
    data=[]
    for row in rows:
        data.append({
            "id":row[0],
            "name":row[1],
            "email":row[2],
            "message":row[3],

        })
    connection.close()
    return {"contacts":data}
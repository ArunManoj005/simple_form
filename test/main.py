from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

import sqlite3

app=FastAPI()

def db():
    connection=sqlite3.connect("database.db")
    cursor=connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT, email TEXT, message TEXT)""")

    connection.commit()
    connection.close()


db()

class Contact(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.post("/contact")
def submit_contact(data: Contact):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",(data.name, data.email, data.message)

    )
    connection.commit()
    connection.close()
    return {"status": "success","message":"saved"}
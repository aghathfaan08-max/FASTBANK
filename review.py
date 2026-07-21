from pymongo import MongoClient
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)
pwd_context = CryptContext(schemes=["bcrypt"])
client = MongoClient("mongodb://localhost:27017/")
db = client["warung"]
col = db["akun"]
key = "belajar jwt error"
algoritma = "HS256"
ambil_token = OAuth2PasswordBearer(tokenUrl="login")


def cek_token(token: str = Depends(ambil_token)):
    try:
        bongkar = jwt.decode(token, key, algorithms=[algoritma])
        nama = bongkar.get("nama")
        return nama
    except JWTError:
        return {"pesan": "token tidak valid"}

def buat_token(username):
    exp = datetime.now() + timedelta(hours=1)
    payload = {"nama": username, "exp": exp}
    token = jwt.encode(payload, key, algorithm=algoritma)
    return token

class daftar(BaseModel):
    username: str
    password: str

@app.post("/daftar")
def daftar_akun(data: daftar):
    cek = col.find_one({"nama": data.username})
    if cek == None:
        password_terenkripsi = pwd_context.hash(data.password)
        col.insert_one({"nama": data.username, "password": password_terenkripsi, "saldo": 0})
        return {"pesan": f"akun {data.username} berhasil didaftarkan"}
    else:
        return {"pesan": "nama akun sudah terpakai, gunakan nama lain"}
    
@app.post("/login")
def login(data: daftar):
    cek = col.find_one({"nama": data.username})
    if cek is not None:
        confirm = pwd_context.verify(data.password, cek["password"])
        if confirm:
            token = buat_token(data.username)
            return {"pesan": f"akun {data.username} berhasil login !!", "acces_token": token}
        else:
            return {"pesan": "password anda salah"}
    else:
        return {"pesan": "akun tidak ada"}
    
@app.get("/saldo")
def cek_saldo(username: str = Depends(cek_token)):
    cek = col.find_one({"nama": username})
    if cek != None:
        return {"saldo": cek["saldo"]}
    else:
        return {"pesan": "akun tidak ditemukan"}
    



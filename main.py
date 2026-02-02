from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import mysql.connector
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin_123",
    database="chatbot_db"
)
cursor = db.cursor()

class ChatRequest(BaseModel):
    message: str


def is_greeting(text: str):
    greetings = ["hi", "halo", "hai", "hello", "selamat pagi", "selamat siang"]
    text = text.lower()
    return any(g in text for g in greetings)


def extract_entities(text: str):
    name = None
    phone = None
    address = None
    dt = None

    phone_match = re.search(r'08\d{7,12}', text)
    if phone_match:
        phone = phone_match.group()

    name_match = re.search(r'rumah\s+([A-Za-z]+)', text)
    if name_match:
        name = name_match.group(1)

    addr_match = re.search(r'di\s+(jalan.*?)(\.|$)', text)
    if addr_match:
        address = addr_match.group(1)

    date_match = re.search(r'tanggal\s+(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})', text)
    time_match = re.search(r'jam\s+(\d{1,2})', text)

    month_map = {
        "januari":1,"februari":2,"maret":3,"april":4,"mei":5,"may":5,
        "juni":6,"juli":7,"agustus":8,"september":9,"oktober":10,
        "november":11,"desember":12
    }

    if date_match and time_match:
        d = int(date_match.group(1))
        m = month_map.get(date_match.group(2).lower(), 1)
        y = int(date_match.group(3))
        h = int(time_match.group(1))
        dt = datetime(y, m, d, h, 0)

    return name, phone, address, dt


@app.post("/chat")
def chat(req: ChatRequest):
    text = req.message.lower()

    # 1️⃣ Extract dulu
    name, phone, address, dt = extract_entities(text)

    # 2️⃣ Kalau ADA data pengiriman → SIMPAN
    if any([name, phone, address, dt]):
        sql = """INSERT INTO customers (name, phone, address, datetime, raw_text)
                 VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (name, phone, address, dt, req.message))
        db.commit()

        return {
            "reply": "Terima kasih, data pengiriman Anda berhasil dicatat.",
            "name": name,
            "phone": phone,
            "address": address,
            "datetime": str(dt)
        }

    # 3️⃣ Kalau TIDAK ada data → cek greeting
    if is_greeting(text):
        return {
            "reply": "Halo 👋 Silakan kirim data pengiriman (nama, alamat, tanggal, dan nomor telepon)."
        }

    # 4️⃣ Kalau bukan greeting & tidak ada data
    return {
        "reply": "Maaf, saya belum menemukan data pengiriman. Mohon kirim lengkap (nama, alamat, tanggal, dan nomor telepon)."
    }

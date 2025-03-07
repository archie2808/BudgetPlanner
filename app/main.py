from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from app.database import SessionLocal
from app.models import Transaction
from app.routers import tokens, users

templates = Jinja2Templates(directory = "app/templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(tokens.router)
app.include_router(users.router)


@app.get("/")
def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})






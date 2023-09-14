from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import smtplib
from email.message import EmailMessage
import os

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/submit")
def submit(Email: str = Form(), Subject: str = Form(), Message: str = Form()):
    msg = EmailMessage()
    msg['Subject'] = Subject
    msg['From'] = os.environ.get('EMAIL_USER')
    msg['To'] = Email
    msg.set_content(f"""{Message}""")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(str(os.environ.get('EMAIL_USER')), str(os.environ.get('EMAIL_PASS')))
        smtp.send_message(msg)

    return "email successfully sent"

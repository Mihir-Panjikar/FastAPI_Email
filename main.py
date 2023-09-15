import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
import smtplib
from email.message import EmailMessage
import os
import logging

logging.basicConfig(filename='example.log', format= '%(asctime)s %(levelname)s:%(message)s', filemode='w', encoding='utf-8', level=logging.DEBUG)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
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
        
    logging.info(f"status code: {status.HTTP_200_OK}, detail: Email successfully sent")
    return HTTPException(status_code=status.HTTP_200_OK, detail="Email successfully sent")

if __name__ == "__main__":
    uvicorn.run(app)
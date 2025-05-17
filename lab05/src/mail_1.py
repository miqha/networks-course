import os
import argparse
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(recipient: str, subject: str, body: str, is_html: bool):
    msg = EmailMessage()
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient
    msg['Subject'] = subject

    if is_html:
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("Письмо успешно отправлено.")

def main():
    parser = argparse.ArgumentParser(description="Программа для отправки email через Gmail")
    parser.add_argument("--to", required=True, help="Email получателя")
    parser.add_argument("--subject", required=True, help="Тема письма")
    parser.add_argument("--file", required=True, help="Файл с телом письма")
    parser.add_argument("--format", required=True, choices=["txt", "html"], help="Формат письма")

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    send_email(args.to, args.subject, content, is_html=(args.format == "html"))

if __name__ == "__main__":
    main()

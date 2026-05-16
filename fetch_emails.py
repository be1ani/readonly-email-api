import imaplib
import email
import os
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
APP_PASSWORD = os.getenv("APP_PASSWORD")
NUM_EMAILS = 10

def fetch_recent_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, APP_PASSWORD)
    mail.select("inbox")

    _, message_ids = mail.search(None, "ALL")
    ids = message_ids[0].split()
    recent_ids = ids[-NUM_EMAILS:]

    for uid in reversed(recent_ids):
        _, msg_data = mail.fetch(uid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        sender = msg.get("From")
        date = msg.get("Date")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

        print(f"From: {sender}")
        print(f"Date: {date}")
        print(f"Subject: {subject}")
        print(f"Body preview: {body[:200].strip()}")
        print("-" * 60)

    mail.logout()

if __name__ == "__main__":
    fetch_recent_emails()

import imaplib
import email
import os
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
APP_PASSWORD = os.getenv("APP_PASSWORD")

_STATUS_CRITERIA = {
    "all": "ALL",
    "read": "SEEN",
    "unread": "UNSEEN",
}

def fetch_emails(n: int = 10, status: str = "all") -> list[dict]:
    criteria = _STATUS_CRITERIA.get(status, "ALL")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, APP_PASSWORD)
    mail.select("inbox")

    _, message_ids = mail.search(None, criteria)
    ids = message_ids[0].split()
    recent_ids = ids[-n:]

    results = []
    for uid in reversed(recent_ids):
        _, msg_data = mail.fetch(uid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

        results.append({
            "from": msg.get("From"),
            "date": msg.get("Date"),
            "subject": subject,
            "body": body.strip(),
        })

    mail.logout()
    return results

if __name__ == "__main__":
    for e in fetch_emails():
        print(f"From: {e['from']}")
        print(f"Date: {e['date']}")
        print(f"Subject: {e['subject']}")
        print(f"Body preview: {e['body'][:200]}")
        print("-" * 60)

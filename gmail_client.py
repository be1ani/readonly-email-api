import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import HTTPException

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


class GmailClient:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        if not os.path.exists(CREDENTIALS_FILE):
            raise HTTPException(
                status_code=500,
                detail=(
                    f"'{CREDENTIALS_FILE}' not found. Download it from Google Cloud Console "
                    "(APIs & Services → Credentials → OAuth 2.0 Client ID) and place it in "
                    "the project root."
                ),
            )

        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    def fetch_emails(self, n: int, status: str) -> list[dict]:
        query_map = {"unread": "is:unread", "read": "is:read", "all": ""}
        query = query_map[status]

        try:
            result = (
                self.service.users()
                .messages()
                .list(userId="me", maxResults=n, q=query, labelIds=["INBOX"])
                .execute()
            )
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"Gmail API error: {e}")

        messages = result.get("messages", [])
        return [self._get_email(msg["id"]) for msg in messages]

    def _get_email(self, msg_id: str) -> dict:
        try:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=msg_id, format="full")
                .execute()
            )
        except HttpError as e:
            raise HTTPException(status_code=502, detail=f"Gmail API error fetching message {msg_id}: {e}")

        headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
        label_ids = msg.get("labelIds", [])

        return {
            "id": msg["id"],
            "thread_id": msg["threadId"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
            "body": self._extract_body(msg["payload"]),
            "labels": label_ids,
            "is_read": "UNREAD" not in label_ids,
        }

    def _extract_body(self, payload: dict) -> str:
        """Recursively extract plain-text body, falling back to HTML stripped of tags."""
        if "parts" in payload:
            # Prefer text/plain; fall through to multipart children
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    return self._decode_body_data(part["body"].get("data", ""))
            for part in payload["parts"]:
                if part["mimeType"].startswith("multipart/"):
                    text = self._extract_body(part)
                    if text:
                        return text
            # Last resort: first HTML part
            for part in payload["parts"]:
                if part["mimeType"] == "text/html":
                    return self._decode_body_data(part["body"].get("data", ""))

        if payload.get("mimeType") == "text/plain":
            return self._decode_body_data(payload["body"].get("data", ""))
        if payload.get("mimeType") == "text/html":
            return self._decode_body_data(payload["body"].get("data", ""))

        return ""

    @staticmethod
    def _decode_body_data(data: str) -> str:
        if not data:
            return ""
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

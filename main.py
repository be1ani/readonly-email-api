from enum import Enum

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from fetch_emails import fetch_emails

app = FastAPI(
    title="Gmail Inbox API",
    description="Fetch the last N read/unread emails from your Gmail inbox.",
    version="1.0.0",
)


class EmailStatus(str, Enum):
    all = "all"
    read = "read"
    unread = "unread"


@app.get(
    "/emails",
    summary="Fetch emails from inbox",
    response_description="List of emails with metadata and body",
)
def get_emails(
    n: int = Query(default=10, ge=1, le=500, description="Number of emails to fetch"),
    status: EmailStatus = Query(
        default=EmailStatus.all,
        description="Filter by read/unread status",
    ),
):
    """
    Fetch the last **N** emails from the Gmail inbox.

    - **n**: how many emails to return (1–500)
    - **status**: `all` | `read` | `unread`
    """
    emails = fetch_emails(n=n, status=status.value)
    return JSONResponse(content={"count": len(emails), "status_filter": status, "emails": emails})


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}

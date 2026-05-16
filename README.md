# Gmail Read-Only API

![Gmail Read-Only](icon.png)

A backend service that exposes a REST API for reading Gmail inbox emails over IMAP. No Google Cloud Console, no OAuth flow — just an App Password and you're done.

---

## Requirements

- Python 3.8+
- A Gmail account with 2-Step Verification enabled

---

## Setup

### 1. Install dependencies

```bash
pip install python-dotenv
```

### 2. Generate a Gmail App Password

1. Sign in to your Google account
2. Go to **Security → How you sign in to Google → 2-Step Verification**
3. Scroll to the bottom and click **App passwords**
4. Create a new password (e.g. name it `gmail-read-only`)
5. Copy the 16-character password

> If you don't see **App passwords**, make sure 2-Step Verification is turned on first.

### 3. Configure credentials

Create a `.env` file in the project root:

```env
GMAIL_USER=you@gmail.com
APP_PASSWORD=xxxx xxxx xxxx xxxx
```

### 4. Run

```bash
python fetch_emails.py
```

---

## Docker

```bash
docker build -t gmail-read-only .
docker run --env-file .env gmail-read-only
```

Credentials are passed at runtime via `--env-file` and never baked into the image.

---

## Configuration

| Variable | Location | Default | Description |
|---|---|---|---|
| `GMAIL_USER` | `.env` | — | Your Gmail address |
| `APP_PASSWORD` | `.env` | — | Your 16-character App Password |
| `NUM_EMAILS` | `fetch_emails.py` | `10` | Number of recent emails to fetch |

---

## Security

- Add `.env` to `.gitignore` — never commit credentials
- The App Password grants full account access; treat it like your password
- Revoke it anytime under **My Account → Security → App passwords**

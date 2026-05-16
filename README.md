# Gmail Read-Only API

![Gmail Read-Only](icon.png)

A backend REST API service for reading emails from a Gmail inbox over IMAP. No Google Cloud Console, no OAuth flow — just an App Password and you're done.

---

## Requirements

- Python 3.10+
- Docker (optional)
- A Gmail account with 2-Step Verification enabled

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
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

### 4. Start the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` and interactive docs at `http://localhost:8000/docs`.

---

## Docker

```bash
docker build -t gmail-read-only .
docker run --env-file .env -p 8000:8000 gmail-read-only
```

Credentials are passed at runtime via `--env-file` and never baked into the image.

---

## Configuration

| Variable | Location | Default | Description |
|---|---|---|---|
| `GMAIL_USER` | `.env` | — | Your Gmail address |
| `APP_PASSWORD` | `.env` | — | Your 16-character App Password |

---

## Security

- Add `.env` to `.gitignore` — never commit credentials
- The App Password grants full account access; treat it like your password
- Revoke it anytime under **My Account → Security → App passwords**

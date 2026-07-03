---
source_name: authentication-setup-guide
section: Getting Started
last_updated: 2024-02-15
doc_type: guide
access_level: public
---

# Setting Up Authentication

This guide walks you through authenticating your application with our API.

## Step 1 — Generate your API key

Before writing any code, you need an API key. Navigate to your dashboard
at app.example.com, click your profile icon, then go to Settings > API Keys.
Click "Generate New Key". Name it clearly — you will not be able to rename
it later.

**Important:** The key is shown only once. Copy it to a secure location
like a password manager or a secrets manager (AWS Secrets Manager,
HashiCorp Vault, etc.) before closing the dialog.

## Step 2 — Store the key securely

Never hardcode API keys in source code. Use environment variables:

```bash
export API_KEY="your-key-here"
```

Or use a `.env` file (make sure to add `.env` to your `.gitignore`):


## Step 3 — Make your first authenticated request

Pass the key as a Bearer token in the Authorization header:

```bash
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/v1/status
```

A 200 response means you are authenticated. A 401 means the key is
invalid or revoked.

## Rotating keys without downtime

To rotate a key in production without dropping requests:
1. Generate a new key (your old key still works)
2. Deploy your application with the new key
3. Verify the new key is receiving traffic
4. Revoke the old key
---
source_name: key-rotation-guide
section: Security
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# API Key Rotation Guide

## Why Rotate Your API Keys?
Rotating your API keys is an essential security measure to protect against unauthorized access and potential data breaches. DevAPI recommends rotating your API keys every 90 days to minimize the risk of exploitation. Failure to rotate your keys may result in compromised accounts, data exposure, or even denial-of-service attacks.

## Rotation Without Downtime
To rotate your API key without causing downtime, follow these steps:

1. Generate a new API key using the `GET /keys` endpoint with a `timeout=30` parameter.
2. Set the `rotation_token` header to the value returned by the previous step.
3. Use the new API key in subsequent requests.

Example:
```bash
curl -X GET \
  https://devapi.com/keys \
  -H 'Content-Type: application/json' \
  -H 'rotation_token=abc123' \
  --cookie 'devapi_session=xyz456'
```
Response:
```json
{
  "key": "def789",
  "expires_in": 86400 // expires in 1 day
}
```

## Automated Rotation
To automate API key rotation, DevAPI provides a `schedule` endpoint. You can schedule a new API key to rotate every 90 days using the following HTTP method:

```bash
curl -X POST \
  https://devapi.com/schedule \
  -H 'Content-Type: application/json' \
  -d '{"key": "new_key", "rotation_interval": 90}'
```
Response:
```json
{
  "schedule_id": 12345,
  "next_rotation_time": "2023-12-15T00:00:00Z"
}
```

## Emergency Rotation After Compromise
In the event of a security breach, DevAPI will immediately rotate your API key to prevent further unauthorized access. You can verify whether an emergency rotation has occurred by checking the `emergency_rotation` flag in the response:

```bash
curl -X GET \
  https://devapi.com/keys \
  -H 'Content-Type: application/json'
```
Response:
```json
{
  "key": "new_key",
  "expires_in": 86400 // expires in 1 day,
  "emergency_rotation": true
}
```

Note: In case of emergency rotation, the API key will expire immediately. Please generate a new key and contact DevAPI support to verify the cause of the compromise.

Error Codes:

* `HTTP/1.1 400 Bad Request`: Invalid request parameters.
* `HTTP/1.1 401 Unauthorized`: Insufficient permissions or expired token.
* `HTTP/1.1 500 Internal Server Error`: Unexpected server error or service outage.
---
source_name: api-keys-guide
section: Authentication
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# API Key Management Guide

## Generating an API Key

To generate a new API key, send a POST request to `/api/v1/auth/key` with the following parameters:

* `grant_type`: `client_credentials`
* `client_id`: Your registered client ID
* `client_secret`: Your registered client secret

The response will include a JSON object containing the generated API key and its corresponding expiration date. For example:
```json
{
  "key": "abc123def456",
  "expires_in": 86400
}
```
Note that the API key is valid for 24 hours from generation.

## Storing Securely

Store your API keys securely using a secrets management solution or an environment variable manager. Avoid hardcoding or storing sensitive information in plain text.

When storing, ensure to include the following metadata:

* `api_key_id`: A unique identifier for the API key
* `created_at`: The date and time the API key was generated
* `expires_at`: The date and time the API key expires

Use a secure protocol such as HTTPS when transmitting sensitive information.

## Rotating API Keys

Rotate your API keys every 90 days to maintain security. You can do this by sending a POST request to `/api/v1/auth/key/rotate` with no parameters:
```bash
curl -X POST \
  https://devapi.com/api/v1/auth/key/rotate \
  -H 'Authorization: Bearer <current_api_key>' \
  -H 'Content-Type: application/json'
```
The response will include a new API key and its corresponding expiration date.

## Revoking API Keys

Revoke an API key by sending a DELETE request to `/api/v1/auth/key/{key_id}`:
```bash
curl -X DELETE \
  https://devapi.com/api/v1/auth/key/abc123def456 \
  -H 'Authorization: Bearer <current_api_key>' \
  -H 'Content-Type: application/json'
```
This will delete the corresponding API key and metadata.

## Best Practices for Production Use

### Set Timeout Periods

Set reasonable timeout periods to prevent APIs from hanging indefinitely. For example:
```bash
curl -X POST \
  https://devapi.com/api/v1/auth/key \
  -H 'Authorization: Bearer <client_credentials>' \
  --timeout 300
```
This will cancel the request after 5 minutes if no response is received.

### Validate API Key Expiration Dates

Validate the expiration dates of your API keys to prevent unauthorized access. You can do this by checking the `expires_in` value in the generated JSON response:
```python
import requests

response = requests.post('https://devapi.com/api/v1/auth/key', 
                         headers={'Authorization': 'Bearer <client_credentials>'}, 
                         json={'grant_type': 'client_credentials'})

if response.status_code == 200 and 'expires_in' in response.json():
    print(f"API key expires at: {response.json()['expires_at']}")
else:
    print("Error generating API key")
```
This code will check if the `expires_in` value is greater than zero to ensure the API key has not expired.

### Monitor API Key Usage

Monitor your API key usage regularly to detect suspicious activity. You can do this by tracking the number of requests made with each API key:
```sql
SELECT api_key_id, COUNT(*) as request_count 
FROM api_requests 
WHERE api_key_id IN (SELECT id FROM api_keys) 
GROUP BY api_key_id;
```
This will return a list of API keys and their corresponding request counts.
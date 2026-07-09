---
source_name: common-errors-guide
section: Troubleshooting
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Invalid API Key

If your API request returns a 401 Unauthorized response with an error code of `DevAPI-UNAUTHORIZED`, it means that your API key is invalid or has expired.

To resolve this issue, ensure that you have a valid and active API key. You can check the status of your API key by making a GET request to `/api/key/status`. If your API key has expired, contact DevAPI support to obtain a new one. Make sure to update your code to use the new API key. Additionally, consider implementing retry mechanisms with exponential backoff to handle temporary service disruptions.

### Example Request
```bash
GET /api/endpoint HTTP/1.1
Host: example.devapi.com
Authorization: Bearer invalid-api-key-123
```

### Error Response
```json
{
  "errorCode": "DevAPI-UNAUTHORIZED",
  "errorMessage": "Invalid API key",
  "httpStatus": 401
}
```

## Expired Token

If your API request returns a 401 Unauthorized response with an error code of `DevAPI-TOKEN-EXPIRED`, it means that the token has expired.

To resolve this issue, obtain a new access token by making a POST request to `/api/token/renew`. Make sure to include your client ID and refresh token in the request body. The refreshed token will be returned in the response with an expiration time. Update your code to use the new token before it expires.

### Example Request
```bash
POST /api/token/renew HTTP/1.1
Host: example.devapi.com
Content-Type: application/json

{
  "clientId": "your-client-id",
  "refreshToken": "your-refresh-token"
}
```

### Error Response
```json
{
  "errorCode": "DevAPI-TOKEN-EXPIRED",
  "errorMessage": "Access token has expired",
  "httpStatus": 401,
  "newToken": "new-access-token-123"
}
```

## Malformed Request Body

If your API request returns a 400 Bad Request response with an error code of `DevAPI-MALFORMED`, it means that the request body is malformed or invalid.

To resolve this issue, check the request body for errors and ensure that it conforms to the expected format. Make sure to validate user input data before sending it to the server. If the request body is valid but results in an error, contact DevAPI support to obtain assistance.

### Example Request
```bash
POST /api/endpoint HTTP/1.1
Host: example.devapi.com
Content-Type: application/json

{
  "username": "",
  "password": ""
}
```

### Error Response
```json
{
  "errorCode": "DevAPI-MALFORMED",
  "errorMessage": "Invalid request body",
  "httpStatus": 400,
  "errors": [
    {
      "field": "username",
      "message": "Username cannot be empty"
    }
  ]
}
```

## Missing Required Fields

If your API request returns a 422 Unprocessable Entity response with an error code of `DevAPI-MISSING-FIELDS`, it means that one or more required fields are missing from the request body.

To resolve this issue, ensure that you include all required fields in the request body. Review the API documentation to determine which fields are required for each endpoint. If a field is missing, contact DevAPI support to obtain assistance.

### Example Request
```bash
POST /api/endpoint HTTP/1.1
Host: example.devapi.com
Content-Type: application/json

{
  "username": ""
}
```

### Error Response
```json
{
  "errorCode": "DevAPI-MISSING-FIELDS",
  "errorMessage": "Missing required field 'password'",
  "httpStatus": 422,
  "errors": [
    {
      "field": "password",
      "message": "Password is required"
    }
  ]
}
```

## Timeout

If your API request times out, it may be due to a variety of reasons such as network issues or server overload. To resolve this issue, ensure that you have sufficient bandwidth and storage space. Consider implementing retry mechanisms with exponential backoff to handle temporary service disruptions.

### Example Response
```json
{
  "errorCode": "DevAPI-TIMEOUT",
  "errorMessage": "Request timed out",
  "httpStatus": 408
}
```

Note: The above documentation is a fictional example and should not be used in production without proper validation and testing.
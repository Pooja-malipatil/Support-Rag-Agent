---
source_name: authentication-overview
section: Authentication
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Authentication Overview

At DevAPI, we offer various authentication methods to ensure secure and reliable access to our API. The choice of authentication method depends on your specific use case, application requirements, and personal preference.

## API Keys
### Overview

API keys are a simple and straightforward way to authenticate requests. They consist of a unique string of characters, usually generated randomly, which can be used to identify and verify an account.

### Usage

To use an API key, pass it as part of the `Authorization` header in your request:
```http
GET /users HTTP/1.1
Host: api.devapi.com
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```
Replace `YWRtaW46cGFzc3dvcmQ=` with your actual API key.

### Best Practices

* Store API keys securely, using a secrets manager or encrypted storage.
* Rotate API keys periodically to maintain security and prevent unauthorized access.
* Use a rate limiter to restrict the number of requests made with a single API key.

HTTP Status Codes:

* 200 OK: Successful authentication
* 401 Unauthorized: Incorrect API key

Error Code: `invalid_key`

## OAuth 2.0
### Overview

OAuth 2.0 is an industry-standard authorization framework that provides secure and scalable access to APIs. It allows clients to request access to resources on behalf of a user, without sharing credentials.

### Usage

To use OAuth 2.0, follow these steps:

1. Register your application with DevAPI's OAuth 2.0 provider.
2. Redirect the user to the authorization URL, where they can grant or deny access to their account.
3. Obtain an authorization code and exchange it for an access token.

Example:
```http
GET /oauth/authorize?client_id=your_client_id&redirect_uri=https://your-app.com/callback HTTP/1.1
Host: oauth.devapi.com
```
Replace `https://your-app.com/callback` with your actual redirect URI.

### Best Practices

* Use the client ID and secret to sign requests, rather than hardcoding credentials.
* Use the access token to authenticate requests, instead of sharing credentials directly.
* Implement a mechanism for revoking access tokens when they are no longer needed or have been compromised.

HTTP Status Codes:

* 200 OK: Successful authorization
* 401 Unauthorized: Incorrect client ID or secret

Error Code: `invalid_token`

## JWT Tokens
### Overview

JSON Web Tokens (JWT) are a compact, URL-safe way to transmit information between parties. They provide secure and reliable authentication for API requests.

### Usage

To use JWT tokens, follow these steps:

1. Register your application with DevAPI's JWT provider.
2. Generate a JWT token using the client ID and secret.
3. Include the JWT token in the `Authorization` header of your request:
```http
GET /users HTTP/1.1
Host: api.devapi.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
Replace `...` with the actual JWT token.

### Best Practices

* Store JWT tokens securely, using a secrets manager or encrypted storage.
* Use a mechanism to refresh expired tokens, such as by rotating them periodically.
* Implement a mechanism for revoking tokens when they are no longer needed or have been compromised.

HTTP Status Codes:

* 200 OK: Successful authentication
* 401 Unauthorized: Incorrect client ID or secret

Error Code: `token_expired`

Timeouts:

* API key requests: 30 seconds
* OAuth 2.0 authorization requests: 5 minutes
* JWT token requests: 10 minutes (with a refresh mechanism)

Note: The above documentation is just an example and should be adapted to fit the specific requirements of your API and application.
---
source_name: oauth-guide
section: Authentication
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# OAuth 2.0 Implementation Guide
=====================================================

## Authorization Code Flow

The authorization code flow is a popular method for obtaining access tokens from a resource server. It involves redirecting the user to the authorization server, where they grant permission to your application to access their data.

### Step-by-Step Process

1. Your client application makes an HTTP request to `http://devapi.com/oauth/authorize` with the following parameters:
	* `client_id`: The ID of your application (e.g., "myapp")
	* `redirect_uri`: The URL that will receive the authorization response (e.g., "http://localhost:8080/callback")
	* `scope`: The scope of access requested by your application (e.g., "read emails", "write profile")
2. The authorization server redirects the user to the specified `redirect_uri` with an authorization code as a query parameter.
3. Your client application extracts the authorization code and exchanges it for an access token by making an HTTP request to `http://devapi.com/oauth/token`.
	* `grant_type`: Set to "authorization_code"
	* `code`: The authorization code received in step 2
	* `redirect_uri`: The same value as above

Example Request:
```bash
GET /oauth/authorize?
    client_id=myapp&
    redirect_uri=http://localhost:8080/callback&
    scope=read+emails&
    response_type=code
```
Example Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaGFuIjoiMjMwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "Bearer"
}
```
## Client Credentials Flow

The client credentials flow is used when your application needs to access data on behalf of a user, but the user has already granted permission.

### Step-by-Step Process

1. Your client application makes an HTTP request to `http://devapi.com/oauth/token` with the following parameters:
	* `grant_type`: Set to "client_credentials"
	* `client_id`: The ID of your application (e.g., "myapp")
	* `client_secret`: The secret key for your application
2. The authorization server returns an access token that can be used to make requests on behalf of the user.

Example Request:
```bash
POST /oauth/token HTTP/1.1
Host: devapi.com
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=myapp&
client_secret=1234567890abcdef
```
Example Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaGFuIjoiMjMwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "Bearer"
}
```
## Scopes

Scopes define the permissions that your application needs to access on behalf of a user. The authorization server returns an error if the scope is not recognized.

### Valid Scopes

* `read`: Read-only access
* `write`: Write access
* `email`: Access to email data
* `profile`: Access to profile data

Example Request:
```bash
GET /oauth/authorize?
    client_id=myapp&
    redirect_uri=http://localhost:8080/callback&
    scope=read+email&
    response_type=code
```
## Token Refresh

Tokens are valid for a specified duration (typically 1 hour). If the token expires, your application needs to refresh it.

### Step-by-Step Process

1. Your client application makes an HTTP request to `http://devapi.com/oauth/token` with the following parameters:
	* `grant_type`: Set to "refresh_token"
	* `refresh_token`: The token received in step 2
2. The authorization server returns a new access token.

Example Request:
```bash
POST /oauth/token HTTP/1.1
Host: devapi.com
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=1234567890abcdef
```
Example Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaGFuIjoiMjMwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "Bearer"
}
```
## Error Handling

The authorization server returns HTTP status codes to indicate errors.

* `401 Unauthorized`: Access denied due to invalid credentials
* `403 Forbidden`: Access denied due to lack of permission
* `400 Bad Request`: Request format is invalid
* `429 Too Many Requests`: Rate limit exceeded

Example Response:
```json
{
  "error": "invalid_grant",
  "error_description": "Access token has expired"
}
```
Note: This documentation is for illustrative purposes only and may not reflect the actual implementation details of a production OAuth 2.0 authorization server.
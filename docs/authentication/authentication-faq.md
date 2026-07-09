---
source_name: authentication-faq
section: Authentication
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

## Common Errors During Authentication

### Expired Tokens
If you receive an HTTP status code of 401 Unauthorized when trying to make a request without including a valid token, it's likely that your token has expired. Check the `expires_in` value returned in the token response for the actual number of seconds until the token expires. You can use this value to calculate the correct timestamp and generate a new token before making subsequent requests.

### Invalid Token
If you receive an HTTP status code of 401 Unauthorized when including an invalid token, it's likely that the token is malformed or doesn't match the expected format. Check that your token includes all required fields (e.g., `token_type`, `exp`) and that they match the values returned in the authentication response.

### Token Validation Failures
If you receive an HTTP status code of 400 Bad Request when including a valid but invalid token, it's likely that the token validation failed due to a mismatched scope or audience. Check that your token includes the correct scopes and audiences for the requested resources.

## Token Expiry

The token expiry time is specified in seconds within the `expires_in` field of the authentication response. If you exceed this value without including a new token, your requests will be rejected with an HTTP status code of 401 Unauthorized. Make sure to store the actual timestamp when receiving the token and calculate the correct token validity period.

## Scope Issues

### Mismatched Scopes
If you receive an HTTP status code of 403 Forbidden when requesting resources that require a scope not present in your token, it's likely that the scopes don't match. Check that your token includes all required scopes for the requested resource and make sure to use the correct audience.

### Missing Audiences
If you receive an HTTP status code of 400 Bad Request when including a valid but missing audience in the token, it's likely that the audience doesn't match the expected value. Make sure to include the correct audience in your requests.

## Troubleshooting

If you're experiencing issues with authentication or tokens, try increasing the timeout period by setting the `timeout` parameter within the request headers (e.g., `Content-Type: application/json; timeout=30`). If this doesn't resolve the issue, check that your token is valid and includes all necessary fields.
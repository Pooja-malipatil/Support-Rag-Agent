---
source_name: error-handling-faq
section: Errors
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

# Errors

## Understanding API Error Codes

API errors are an essential part of any application that makes requests to external services. In this section, we will discuss two common types of API errors: 401 Unauthorized and 403 Forbidden.

### HTTP Status Code 401 Unauthorized
The HTTP status code 401 Unauthorized is returned when the API client does not have access to the requested resource or action. This error typically occurs when a user attempts to make an API request without proper authentication credentials.

Example:
```bash
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error_code": 401,
  "error_message": "Invalid username or password"
}
```
If you encounter this error, ensure that your authentication token is valid and up-to-date. You can use the `retry_with_refresh_token` parameter to refresh the token before retrying the request.

### HTTP Status Code 403 Forbidden
The HTTP status code 403 Forbidden is returned when the API client does not have permission to access a specific resource or action. This error typically occurs when a user attempts to make an API request without proper authorization.

Example:
```bash
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error_code": 403,
  "error_message": "Insufficient permissions"
}
```
If you encounter this error, ensure that your authentication token has the required permissions to access the requested resource or action.

## Handling 500 Errors

500 errors are internal server errors returned by the API. These errors typically occur due to unexpected failures within the system, such as database connectivity issues or service unavailability.

Example:
```bash
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error_code": 500,
  "error_message": "Server error"
}
```
When handling 500 errors, you should:

*   Check if the issue is transient and retry the request after a short delay.
*   Log the error for further investigation.
*   Implement exponential backoff to prevent overwhelming the API with repeated requests.

### Retry Policy

To implement a retry policy for 500 errors, use the `retry_with_exponential_backoff` parameter. This allows you to specify the number of attempts and the wait time between retries.

Example:
```bash
retry_with_exponential_backoff(attempts=3, max_wait_time=5000)
```
This will attempt to retry the request up to 3 times with increasing wait times (up to 5 seconds) before giving up.

## Idempotent API Requests

Idempotency is a property of an HTTP method where making the same request multiple times has the same effect as making it once. In our API, we strive to make all requests idempotent to prevent abuse and ensure predictable behavior.

When sending requests, keep in mind that if you need to retry a failed request:

*   Use the `retry_with_idempotency` parameter.
*   The client should be able to handle temporary failures without making duplicate requests.

If you're unsure whether a request is idempotent or not, consider the following examples:

### Idempotent Request
```bash
GET /users HTTP/1.1
Host: api.example.com

Accept: application/json

[Code snippet]

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name": "John Doe"
}
```
In this example, making the same request multiple times has no effect on the outcome.

### Non-Idempotent Request
```bash
POST /users HTTP/1.1
Host: api.example.com

Accept: application/json

[Code snippet]

HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 123,
  "name": "John Doe"
}
```
In this example, making the same request multiple times will result in duplicate user records being created.

When in doubt, consult our API documentation for more information on idempotent requests and retry policies.
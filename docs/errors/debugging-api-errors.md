---
source_name: debugging-api-errors
section: Errors
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Debugging API Errors in DevAPI

## Reading Error Responses

When an API request fails, your application will receive an error response from the server. The error response includes a unique `request_id` that can be used to retrieve more information about the error. The `request_id` is included in the `X-Request-ID` header of the response.

To read the error response, you should check the following:

*   HTTP status code: 4xx (client errors) or 5xx (server errors)
*   `error_code`: a unique identifier for the error
*   `error_message`: a human-readable description of the error

Here is an example of an error response:

```json
{
    "request_id": "1234567890",
    "http_status_code": 404,
    "error_code": "NOT_FOUND",
    "error_message": "Resource not found"
}
```

## Using Request IDs to Retrieve Error Information

You can use the `request_id` in your application to retrieve more information about the error from DevAPI. To do this, you need to send a GET request to `/api/v1/error/${request_id}`.

The API returns an object that includes more detailed information about the error, such as the cause and any additional data required for recovery.

Here is an example of what the response might look like:

```json
{
    "request_id": "1234567890",
    "error_message": "Resource not found",
    "cause": "The requested resource was not found.",
    "additional_data": {
        "resource_id": 123,
        "reason": "Not found"
    }
}
```

## Checking Logs for Additional Error Information

You can also check the logs on DevAPI to retrieve additional information about an error. The logs are available in two formats: a JSON file and a CSV spreadsheet.

To access the logs, you need to send a GET request to `/api/v1/logs/${request_id}` or `/api/v1/logs/${error_code}`.

The API returns an object that includes log entries for the given `request_id` or `error_code`. The log entries include timestamps, error messages, and any additional data required for recovery.

Here is an example of what the response might look like:

```json
[
    {
        "timestamp": 1643723900,
        "message": "GET /api/v1/resource HTTP/1.1 failed",
        "level": "ERROR",
        "request_id": "1234567890"
    },
    {
        "timestamp": 1643723910,
        "message": "Resource not found",
        "level": "INFO",
        "error_code": "NOT_FOUND"
    }
]
```

## Common Mistakes and Their Fixes

Here are some common mistakes when debugging API errors:

*   **Incorrect request headers**: Make sure to include the required headers, such as `Content-Type` and `Accept`.
*   **Insufficient timeouts**: Increase the timeout value for your requests to allow enough time for the server to respond.
*   **Invalid error codes**: Make sure to use valid error codes when sending an error response.

Here is an example of how you can fix these mistakes:

```bash
# Incorrect request headers
curl -X GET \
  https://devapi.com/api/v1/resource \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

# Insufficient timeouts
curl -X GET \
  https://devapi.com/api/v1/resource \
  --timeout 30

# Invalid error codes
curl -X POST \
  https://devapi.com/api/v1/error \
  -H 'Content-Type: application/json' \
  -d '{"error_code": "NOT_FOUND"}'
```

## Example Error Handling Code

Here is an example of how you can handle errors in your application:

```javascript
// Error handling middleware
function errorHandlingMiddleware(req, res, next) {
    req.on('error', (err) => {
        const errorResponse = {
            request_id: req.requestId,
            http_status_code: err.statusCode,
            error_code: err.errorCode,
            error_message: err.errorMessage
        };
        res.status(err.statusCode).json(errorResponse);
    });
    next();
}

// Using the middleware in an Express application
const express = require('express');
const app = express();

app.use(errorHandlingMiddleware);

app.get('/api/v1/resource', (req, res) => {
    // Send a GET request to DevAPI
});
```

This example uses the `errorHandlingMiddleware` function to catch any errors that occur during the execution of an Express application. The middleware sends an error response back to the client with the relevant information about the error.

I hope this helps you when debugging API errors! If you have any questions or need further clarification, please don't hesitate to ask.
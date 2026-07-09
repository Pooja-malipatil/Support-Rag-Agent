---
source_name: error-codes-reference
section: Errors
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Errors

## HTTP Error Codes Reference

DevAPI uses standard HTTP status codes to indicate errors. Below is a comprehensive list of common error codes encountered during API interactions.

### 400 Bad Request
#### Description:
The request was invalid or cannot be processed due to user-provided data being malformed.

#### Causes:
-   Missing or null parameters in the query string.
-   Incomplete or improperly formatted JSON data in the request body.

#### Fixes:

*   Ensure all required parameters are provided, and their values conform to expected formats.
*   Validate JSON data using schema validation libraries before sending it.

### 401 Unauthorized
#### Description:
The client did not provide valid credentials or is not authorized to access the requested resource.

#### Causes:
-   Incorrect username or password in the authentication header.
-   Authentication token has expired or is invalid.

#### Fixes:

*   Verify and update your API keys and tokens before making requests.
*   Consider implementing session management for persisted authentication data.

### 403 Forbidden
#### Description:
The client does not have permission to access the requested resource, even with valid credentials.

#### Causes:
-   Incorrectly formatted or missing required headers (e.g., `Authorization`).
-   Authentication failed due to expired tokens or invalid credentials.

#### Fixes:

*   Check and update your headers before making requests.
*   Verify that authentication details are accurate and up-to-date.

### 404 Not Found
#### Description:
The requested resource could not be found, either because it does not exist or the client cannot access it.

#### Causes:
-   Requested endpoint has been removed, renamed, or moved without proper updates.
-   Incorrect URL format in the request.

#### Fixes:

*   Double-check URLs before making requests and ensure they match existing endpoints.
*   Consider using endpoint versioning to handle changes over time.

### 429 Too Many Requests
#### Description:
The rate limit for a given resource has been exceeded, meaning you're too aggressive with your requests.

#### Causes:
-   Request count is higher than allowed limits for the specific resource.

#### Fixes:

*   Implement a reasonable delay between requests based on the API's rate limiting policy.
*   Use caching mechanisms to reduce the number of requests made within a short time frame.
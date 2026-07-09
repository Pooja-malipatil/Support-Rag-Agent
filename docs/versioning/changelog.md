---
source_name: changelog
section: Versioning
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Versioning Guide

DevAPI's API follows a versioning strategy to ensure compatibility and predictability across different releases. The versioning scheme is based on Semantic Versioning (SemVer), where major, minor, and patch versions are incremented according to specific rules.

### Major Version Changes

Major version changes occur when significant updates are made to the underlying system or technology stack. These changes often result in breaking changes, which may require adjustments to your codebase. For example:

* Version 2.0 introduces support for a new database schema, replacing the legacy schema.
* Version 3.1 adds a new API endpoint for authentication.

### Minor Version Changes

Minor version changes introduce new features or enhancements without affecting backward compatibility. These changes typically involve adding new endpoints, parameters, or response formats.

For example:

* Version 2.5 introduces a new `limit` query parameter to control the number of results returned in response to GET /users.
* Version 3.0 adds support for JSON Web Tokens (JWT) authentication.

### Patch Version Changes

Patch version changes address bug fixes and minor issues, ensuring stability and reliability. These changes are typically smaller and do not affect the overall API surface.

For example:

* Version 2.1 fixes a critical issue with incorrect pagination in GET /users.
* Version 3.5 resolves an error causing timeouts when processing large requests.

### Deprecation Notices

DevAPI reserves the right to deprecate API endpoints, parameters, or response formats that are no longer supported or useful. Users should use `GET /apis/{endpoint}/deprecated` to check if a specific endpoint is deprecated.

For example:

* Version 2.8 marks GET /users as deprecated in favor of POST /users, which returns a list of users.
* Version 3.8 removes support for the `username` parameter in GET /users due to security concerns.

### Breaking Changes

Breaking changes occur when a new version introduces significant updates that may break existing code or workflows. Users should review changes carefully before upgrading their applications.

For example:

* Version 2.9 modifies the response format for GET /users, replacing the `metadata` property with `pagination`.
* Version 3.4 changes the authentication mechanism, requiring users to use JWT tokens instead of basic auth.

### Example API Request

Here's an example request using the latest version (3.5) of the API:

```bash
GET https://api.devapi.com/v3/users?limit=10&offset=0 HTTP/1.1
Host: api.devapi.com
Authorization: Bearer <your-jwt-token>
```

### Error Handling

DevAPI returns standard HTTP status codes to indicate the outcome of an API request:

* 200 OK (default response code)
* 400 Bad Request (invalid request data or syntax errors)
* 401 Unauthorized (authentication failed)
* 404 Not Found (requested endpoint not available)

Example error responses:

```bash
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Invalid username or password",
  "code": "auth-001"
}
```

```bash
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "Authentication failed",
  "code": "auth-002"
}
```

### Timeouts and Rate Limiting

DevAPI has a reasonable timeout period of 30 seconds for all requests. Exceeding this limit will result in a 429 Too Many Requests error.

Rate limiting is enforced on each API endpoint, with the following limits:

* GET /users: 100 requests per minute
* POST /users: 50 requests per hour
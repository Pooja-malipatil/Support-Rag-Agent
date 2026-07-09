---
source_name: versioning-faq
section: Versioning
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

# Versioning FAQ

## Introduction to Versioning

DevAPI follows semantic versioning (SemVer) for its API releases. This means that our API versions are numbered in the format `major.minor.patch`, where:

* `major` is incremented for backwards-incompatible changes
* `minor` is incremented for new features or enhancements without breaking existing functionality
* `patch` is incremented for bug fixes and minor updates

## What happens when a version is deprecated?

When we deprecate an API version, it means that we no longer recommend using it. However, the deprecated version will still be available for a limited time to allow you to update your applications. After the deprecation period (currently 6 months), we will return a `409 Conflict` HTTP status code and a `DeprecationWarning` error message in the API response.

Example:
```bash
GET /api/1.2.3 HTTP/1.1
Host: devapi.com

HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": {
    "code": 409,
    "message": "DeprecationWarning: Version 1.2.3 is deprecated and will be removed on [insert date]."
  }
}
```
## Can I use multiple versions?

Yes, you can use multiple API versions concurrently. However, we recommend using the latest version (currently `major.minor`) for new applications or features. If you need to support older versions for compatibility reasons, you can use the `?version=specific_version` query parameter.

Example:
```bash
GET /api/1.2.3?version=1.2 HTTP/1.1
Host: devapi.com

HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": [...]
}
```
## Testing new versions

To test a new version of the API, you can use our staging environment (currently at `staging.devapi.com`). We recommend testing in a sandbox or development environment before deploying to production. You can also use our `--dev` query parameter to enable debug logging and error reporting.

Example:
```bash
GET /api/next?version=next&--dev HTTP/1.1
Host: staging.devapi.com

HTTP/1.1 200 OK
Content-Type: application/json

{
  "debug": true,
  "error": [...]
}
```
## Additional notes

* Our API versioning policy can be found in the [Terms of Service](https://devapi.com/terms).
* If you're experiencing issues with our API, please contact us at [support@devapi.com](mailto:support@devapi.com) for assistance.
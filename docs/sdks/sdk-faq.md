---
source_name: sdk-faq
section: SDKs
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

## Supported Programming Languages for DevAPI SDKs

DevAPI provides SDKs in multiple programming languages to cater to different developer needs. The following languages are currently supported:

* Java (version 8 or later)
* Python (3.6 or later)
* C++14
* JavaScript (ES6+)

Each language has its own documentation and API reference, which can be found on the DevAPI website.

## SDK Version Compatibility with API Version

DevAPI SDKs are designed to work seamlessly with our API versions. The compatibility between SDK versions and API versions is as follows:

| SDK Version | Compatible with API Versions |
| --- | --- |
| v1.0 | v1, v2 |
| v2.0 | v1, v2, v3 |
| v3.0 | all API versions |

Please note that we recommend using the latest SDK version to ensure compatibility and stability.

## Contributing to Open Source SDKs

DevAPI encourages contributions from the developer community to improve our open-source SDKs. To contribute, please follow these guidelines:

* Fork the repository on GitHub or Bitbucket.
* Create a new branch for your changes and submit a pull request.
* Ensure that all tests pass before submitting your changes.
* Our review process typically takes 3-5 business days.

Example: To report an issue with the SDK, you can create a new issue on our GitHub repository using the following code snippet:
```bash
curl -X POST \
  https://api.devapi.com/issues \
  -H 'Content-Type: application/json' \
  -d '{"issue": {"title": "SDK Bug", "description": "SDK crashes when..."}}'
```
This will create a new issue with the specified title and description. If you're reporting an error, our API returns a 400 Bad Request response with an error code indicating the nature of the error.

## Handling Timeout Errors

If your request times out, DevAPI returns a 504 Gateway Timeout response with a timeout value indicating the length of time the request took to complete. The following HTTP status codes are returned for timeouts:

* 504 Gateway Timeout: timeout occurs after 30 seconds (default) or can be configured by the developer
* 408 Request Timeout: timeout occurs after 15 seconds

Example:
```bash
curl -X GET \
  https://api.devapi.com/data?limit=1000 \  # request times out
```
Response:
```json
{
  "error": {
    "code": 504,
    "message": "Gateway Timeout"
  }
}
```
Note that the timeout value can be configured by setting the `timeout` parameter in your SDK.
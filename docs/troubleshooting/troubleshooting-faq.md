---
source_name: troubleshooting-faq
section: Troubleshooting
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

# Troubleshooting FAQ

## Failing Requests Silently
When a request fails silently, it may be due to a timeout or an unhandled exception. Check the HTTP status code returned by the server. A 408 Request Timeout error indicates that the server timed out waiting for the request to complete.

To troubleshoot this issue, check the `timeout` setting in your client-side configuration (e.g., `.curl` file or API client library). Ensure it is set to a reasonable value (e.g., 30 seconds) and not too low. You can also increase the timeout value using the `Timeout` header in your request.

For example, to retry a failed request with a higher timeout, add the following headers:
```bash
curl -H "Timeout: 60" https://api.devapi.com/endpoint
```
## Testing Without Affecting Production

To test your application without affecting production, use our staging environment. DevAPI provides a separate staging instance for testing and debugging purposes.

Before making changes to the live API, use our staging endpoint (e.g., `https://staging-api.devapi.com/endpoint`). Make sure to update your client-side configuration to point to the staging URL instead of the production URL.

For example:
```bash
curl https://staging-api.devapi.com/endpoint
```
Note: Our staging environment uses a different set of API keys and credentials. Ensure you are using the correct credentials for testing purposes.

## Getting Support

DevAPI provides 24/7 support via our [support ticket system](https://support.devapi.com/). When creating a support ticket, please provide detailed information about the issue you're experiencing, including:

* HTTP request details (e.g., URL, method, headers)
* Client-side code snippets
* Error messages or stack traces

Our support team will respond to your ticket within 1-2 business days. If you need urgent assistance, feel free to contact us via phone at +1 (555) 123-4567.

## Error Codes and Status Codes

DevAPI returns a standard set of error codes and status codes for each API endpoint. Below are some common error codes and their corresponding descriptions:

| Error Code | Description |
| --- | --- |
| 401 Unauthorized | Invalid or missing authentication credentials |
| 422 Unprocessable Entity | Request body is invalid or cannot be processed |

Common HTTP status codes returned by DevAPI include:

| Status Code | Description |
| --- | --- |
| 200 OK | Request was successful |
| 404 Not Found | Requested resource not found |
| 500 Internal Server Error | Server-side error occurred |

Refer to our [API Reference](https://api.devapi.com/) for a complete list of available endpoints, error codes, and status codes.
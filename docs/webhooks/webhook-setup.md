---
source_name: webhook-setup
section: Webhooks
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Setting up Webhooks
### Overview

Webhooks are an essential feature of our API, allowing you to receive notifications when a specific event occurs. To set up webhooks, you'll need to register one or more endpoints, select which events you want to trigger them for, and test them using our command-line interface (CLI).

### Registering Endpoints
When registering an endpoint, you must specify the following details:
* Endpoint URL: The complete URL of your webhook endpoint.
* Content Type: `application/json` is the only supported content type. You can use any other content type, but it will be ignored by our API.
* Event Types: Choose one or more events that trigger this endpoint.

Here's an example of a successful registration request:
```bash
curl -X POST \
  https://api.devapi.com/webhooks \
  -H 'Content-Type: application/json' \
  -d '{"endpoint_url": "https://example.com/webhook", "content_type": "application/json"}'
```
This will create a new webhook with the specified endpoint URL.

### Verifying Delivery
To verify that our API is successfully delivering notifications to your endpoint, use the `verify` endpoint:
```bash
curl -X POST \
  https://api.devapi.com/webhooks/verify \
  -H 'Content-Type: application/json' \
  -d '{"endpoint_url": "https://example.com/webhook", "event_type": "new_user"}'
```
This will return a JSON response with the following structure:
```json
{
  "status": "success",
  "timestamp": "2023-03-09T14:30:00Z"
}
```
If your endpoint is not receiving notifications, you'll receive an error response with a `404 Not Found` status code.

### Testing with CLI
To test your webhook endpoint using our CLI, use the `test` command:
```bash
devapi-test --endpoint-url https://example.com/webhook --event-type new_user
```
This will send a request to your endpoint and verify that it receives the notification. If your endpoint is working correctly, you'll see an output indicating success.

### Error Handling

If your webhook registration or verification fails, our API will return an error response with a specific status code:
* `400 Bad Request`: Invalid request data.
* `401 Unauthorized`: Insufficient authentication credentials.
* `404 Not Found`: Endpoint URL not found.

For more information on handling errors and implementing retries, refer to the [API Error Handling documentation](https://devapi.com/docs/error-handling).
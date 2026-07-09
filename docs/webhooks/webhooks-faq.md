---
source_name: webhooks-faq
section: Webhooks
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

## Webhook Delays and Delivery Out of Order

Webhooks can sometimes be delivered out of order due to various factors such as network latency or congestion on the receiving end. In most cases, webhooks are delivered in chronological order based on their event timestamp, but in rare instances, they might not arrive at the expected time.

When dealing with delayed or out-of-order webhooks, it's essential to verify that your application is correctly handling incoming events. Check your event processing pipeline and ensure that you're using a consistent sorting method to process events from oldest to most recent.

If you suspect an issue with webhook delivery timing, check the HTTP status code of the received webhook: 202 Accepted indicates that the request has been accepted but not yet processed (usually means it's delayed), while 429 Too Many Requests might indicate network congestion.

## Debugging Failed Webhooks

When debugging failed webhooks, it's crucial to examine the HTTP response headers and body for clues. Look for specific error codes such as:

* `500 Internal Server Error`: Indicates an unexpected server-side failure
* `404 Not Found`: Suggests that the event was not recognized or processed by your application
* `429 Too Many Requests`: May indicate network congestion or excessive request volume

You can also check the `X-Request-ID` header, which contains a unique identifier for each incoming webhook. Using this ID in your logs and error messages will help you identify recurring issues.

Example code snippet for logging failed webhooks:
```python
import logging

def log_webhook_failure(event_id):
    logging.error(f"Failed webhook event {event_id}: "
                 f"{logging.getLogger().name} returned HTTP status code {response.status_code}")
```

## Testing Locally with ngrok

When testing locally with ngrok, ensure that you're using the correct `Content-Type` header for your webhooks. The default value is usually set to `application/json`, so make sure to verify this in your development environment.

To test webhook delivery with ngrok, use the following command:
```bash
ngrok http 5000 --cert /path/to/cert.crt --key /path/to/key.key -log stdout
```
This sets up an HTTPS tunnel and logs incoming requests. You can then access your local web server using `http://localhost:5000`.

When testing locally, you might encounter timeouts (usually around 2-3 seconds) due to the overhead of handling webhook requests. To mitigate this, consider using a slower-than-usual connection speed or adjusting your test environment accordingly.

## Error Handling and Retry Mechanisms

When implementing retry mechanisms for failed webhooks, ensure that you're handling errors correctly according to your application's error handling strategy.

Consider implementing exponential backoff with jitter (e.g., `backoff.sleep(1)`) to avoid overwhelming your application with repeated requests. Also, verify that your timeout settings are reasonable and take into account potential network latency or service availability issues.

Example code snippet for retrying failed webhooks:
```python
import time

def retry_webhook(event_id, max_attempts=3):
    attempt = 0
    while attempt < max_attempts:
        try:
            # Attempt to process the webhook event
            return process_event(event_id)
        except Exception as e:
            # Log the error and wait for a short duration before retrying
            logging.error(f"Webhook failed with code {e}: "
                         f"Retrying in {backoff.sleep(1)} seconds")
            attempt += 1
```
In this example, we're using a simple exponential backoff strategy with a maximum of 3 attempts.
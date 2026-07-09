---
source_name: webhook-retries
section: Webhooks
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Webhooks

## Introduction

The DevAPI Webhook service allows developers to receive notifications from our platform in real-time. This guide outlines the behavior of our webhook retry mechanism, including when and how retries are attempted, what triggers a retry, and how we handle duplicate events.

## Retry Schedule

Our webhooks use an exponential backoff strategy to retry failed requests. The retry schedule is as follows:

* Initial retry: 500ms after the initial failure
* Subsequent retries: 2x the previous interval (e.g., 1000ms, 2000ms, etc.)
* Maximum retry attempts: 5

If all retries fail, the webhook will return a `429 Too Many Requests` error with a Retry-After header containing the expected time to try again.

Example Request:
```bash
POST /webhooks HTTP/1.1
Host: api.devapi.com
Content-Type: application/json

{
    "id": "example-webhook-id",
    "url": "https://example.com/webhook",
    "secret": "abc123"
}
```
## What Triggers a Retry

Retries are triggered by the following conditions:

* HTTP 500 Internal Server Error response from our server
* HTTP 502 Bad Gateway response from our server (indicating an error in the relay)
* Network errors (e.g., DNS resolution failures, timeouts)

If any of these conditions occur during the initial request or a retry, we will attempt to retry the webhook.

## Idempotency Keys

To prevent duplicate events from being processed, we use idempotent keys for each webhook. These keys are included in the `id` field of the webhook event payload and must be present in the `X-DevAPI-Webhook-ID` header on incoming requests.

Example Request:
```bash
POST /webhooks HTTP/1.1
Host: api.devapi.com
Content-Type: application/json

{
    "id": "example-webhook-id",
    "url": "https://example.com/webhook",
    "secret": "abc123"
}
```
In this example, the `id` field in the payload matches the value of the `X-DevAPI-Webhook-ID` header.

## Handling Duplicate Events

To handle duplicate events, we use a combination of event timestamps and idempotent keys. When processing an event, we check if:

* The event timestamp is newer than the last processed timestamp for that webhook
* The event has a different `X-DevAPI-Webhook-ID` header value (indicating a different instance of the same webhook)

If either condition is true, we will process the event as usual. Otherwise, we will ignore it.

Example Event Payload:
```json
{
    "id": "example-webhook-id",
    "timestamp": 1643723400,
    "data": {"foo": "bar"}
}
```
In this example, the `timestamp` field indicates that the event occurred at some point in the past. If a subsequent request with the same `X-DevAPI-Webhook-ID` header value is received, we will process it as usual.

## Error Codes

Here are some common error codes associated with webhook retries:

* 429 Too Many Requests: retry after the specified time
* 502 Bad Gateway: retry or contact support
* 500 Internal Server Error: retry or contact support
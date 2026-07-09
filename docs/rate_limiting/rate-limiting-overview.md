---
source_name: rate-limiting-overview
section: Rate Limiting
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Rate Limiting Guide

Rate limiting is a crucial mechanism in DevAPI to prevent abuse and ensure fair usage of our APIs. This guide explains how rate limiting works, including request quotas, time windows, token bucket algorithm, and limits per endpoint.

## Request Quotas
The request quota refers to the maximum number of requests allowed within a specified time window (also known as a time slice). DevAPI enforces the following request quotas:

* **Global Quota**: 100 requests per minute (60-second time window)
* **Endpoint-Specific Quotas**:
 + `/users`: 50 requests per minute
 + `/products`: 75 requests per minute
 + `/orders`: 25 requests per minute

Exceeding these quotas will result in a `429 Too Many Requests` HTTP status code with the following error message: "Rate limit exceeded. Please try again later."

## Time Windows and Tokens
The token bucket algorithm is used to manage rate limiting. The algorithm maintains a bucket of tokens, which represent the allowed number of requests within a time window. When a request is made, one token is removed from the bucket, and the bucket is refilled at a constant rate.

* **Token Bucket Refill Rate**: 10 tokens per second (global quota), adjusted based on endpoint-specific quotas
* **Token Expiration Time**: 60 seconds (60-second time window)
* **Time Window Size**: 1 minute (60-second time window)

## Limits Per Endpoint
Each endpoint has its own rate limiting limits. These limits are enforced in addition to the global and endpoint-specific quotas.

* **Endpoint-Specific Rate Limiting Limits**:
 + `/users`: 100 requests per hour
 + `/products`: 500 requests per day
 + `/orders`: 50 requests per week

Exceeding these limits will result in a `429 Too Many Requests` HTTP status code with the following error message: "Rate limit exceeded. Please try again later."

## Handling Rate Limit Exceeded Errors
If a request exceeds the rate limiting quota, DevAPI returns a `429 Too Many Requests` HTTP status code with a retry-after header containing the number of seconds until the rate limit expires.

Example response:
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 300
Content-Type: application/json

{
  "error": "Rate limit exceeded",
  "message": "Please try again later"
}
```
To avoid hitting the rate limit, consider implementing a caching strategy or using a more gradual request frequency.

## Code Snippet Example
Here is an example of how to implement token bucket algorithm in Node.js:
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute time window
  max: 100, // global quota
  handler: (req, res) => {
    return res.status(429).json({ error: 'Rate limit exceeded', message: 'Please try again later' });
  },
});

// Apply rate limiting to the endpoint
app.use('/users', limiter);
```
Note that this is just a basic example and you should adjust the rates and limits according to your specific use case.
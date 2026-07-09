---
source_name: rate-limit-tiers
section: Rate Limiting
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Rate Limiting

DevAPI's rate limiting system is designed to prevent abuse and ensure a fair experience for all users. The rate limit tiers are based on the plan chosen by the user, and each tier has its own set of rules and restrictions.

## Free Plan (100 req/min)

The free plan has a rate limit of 100 requests per minute. This means that if you exceed this limit, your API calls will be throttled back to prevent abuse. HTTP status code 429 (Too Many Requests) will be returned in such cases.

To check the current request rate, you can use the following endpoint:
```bash
GET /rate-limit
```
This will return a JSON response with the current rate limit and the number of requests made in the last minute.

If you need to make more than 100 API calls per minute, please upgrade to our Pro plan or contact our support team for assistance.

## Pro Plan (1000 req/min)

The Pro plan has a much higher rate limit of 1000 requests per minute. This is suitable for most developers who require high levels of performance and reliability.

Burst limits apply to the Pro plan as well. If you exceed the burst limit, your API calls will be throttled back. The current burst limit is 50 requests within a span of 5 minutes.

If you need more than this burst limit, please contact our support team for assistance.

## Burst Limits

Burst limits are designed to prevent abuse and ensure fair usage. If you exceed the burst limit, HTTP status code 429 (Too Many Requests) will be returned.

To avoid hitting the burst limit, make sure to spread your API calls across multiple minutes. You can use our [rate-limiting library](https://github.com/devapi/rate-limiter) in your application to help manage your request rate.

## Daily Quotas

Daily quotas apply to all plans and are designed to prevent abuse on a per-day basis. If you exceed your daily quota, HTTP status code 429 (Too Many Requests) will be returned.

The current daily quota is 10,000 requests for the Free plan and 50,000 requests for the Pro plan.

## Error Codes

Here's a summary of error codes related to rate limiting:

* 429: Too Many Requests
* 429 Too Many Requests – Rate Limit Exceeded
* 429 Too Many Requests – Burst Limit Exceeded
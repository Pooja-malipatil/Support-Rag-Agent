---
source_name: rate-limiting-faq
section: Rate Limiting
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

# Rate Limiting

## What Counts as a Request

The DevAPI rate limiting system counts HTTP requests that make a valid API call to our servers. This includes:

* Successful API calls (200 OK)
* Failed API calls due to invalid credentials or request payload errors (400 Bad Request, 401 Unauthorized, etc.)
* Timed-out requests (429 Too Many Requests)

However, requests from cached responses are not counted as separate requests.

## Shared Limits Across Keys

DevAPI rate limits apply across all keys and API endpoints. If you have multiple keys with overlapping rate limit periods, it's recommended to use a single key for each set of related APIs to avoid exceeding the combined limit.

For example, if you have two keys `key1` and `key2`, both with a 100 requests per minute limit, using these keys together would result in an effective 200 requests per minute limit. To avoid this, create separate keys for each API endpoint or group related APIs under a single key.

## Monitoring Usage

To monitor your usage and see if you're approaching the rate limit threshold, use our [API Monitoring Tool](https://devapi.com/tools/monitoring). This tool provides real-time metrics on your request count, including:

* Request count per minute
* Requests remaining before exceeding the limit
* Time of day/week/month when requests are most frequent

You can also view historical data for each key and API endpoint.

## Requesting Limit Increases

To request a rate limit increase, send a POST request to our [rate limit request endpoint](https://devapi.com/endpoints/rate-limit-request). Include the following fields in your request body:

* `key`: The key you're requesting an increase for
* `reason`: A brief explanation of why you need the increase (e.g. "High usage due to increased customer adoption")
* `request_count`: The expected number of requests per minute
* `response_time_threshold`: The maximum response time in seconds

Example request body:
```json
{
  "key": "my_key",
  "reason": "Increased customer adoption leading to high API call volume",
  "request_count": 150,
  "response_time_threshold": 5000
}
```

If your request is approved, we'll update the rate limit for the specified key and API endpoint.
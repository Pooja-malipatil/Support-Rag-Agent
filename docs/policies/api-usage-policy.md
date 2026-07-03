---
source_name: api-usage-policy
section: Acceptable Use
last_updated: 2024-01-10
doc_type: policy
access_level: public
---

# API Usage Policy

## Rate Limits

All API keys are subject to rate limits. Free tier: 100 requests/minute.
Pro tier: 1,000 requests/minute. Enterprise: custom limits negotiated
at contract time.

Exceeding rate limits returns HTTP 429. Your client should implement
exponential backoff when this occurs.

## Key Security Requirements

You are responsible for keeping API keys confidential. Sharing keys
between multiple applications is discouraged. Keys embedded in
client-side code (JavaScript, mobile apps) must use restricted keys
with limited permissions.

## Prohibited Uses

API keys may not be used to:
- Scrape or bulk-download content beyond your plan's limits
- Resell API access to third parties
- Circumvent access controls or rate limiting

Violations may result in immediate key revocation without notice.
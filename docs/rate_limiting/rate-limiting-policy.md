---
source_name: rate-limiting-policy
section: Rate Limiting
last_updated: "2024-03-01"
doc_type: policy
access_level: public
---

# Rate Limiting Policy

## Fair Use Requirements

DevAPI adheres to a fair use policy for rate limiting, ensuring that our services remain accessible and usable by our customers. The following rates are applicable:

* **Free Tier**: 100 requests per minute (RPM), 1,000 requests per hour (RPH)
* **Premium Tier**: 500 RPM, 10,000 RPH

These limits apply to all API endpoints and are enforced globally. Exceeding these limits will result in an HTTP status code of 429 Too Many Requests.

## Consequences of Limit Abuse

Excessive or abusive behavior, such as attempting to breach rate limits with malicious intent, may result in:

* Temporary or permanent IP blocking
* Account suspension or termination
* Imposition of additional rate limiting tiers or restrictions on API access

DevAPI reserves the right to investigate and take action against any users suspected of abusing our rate limiting policies.

## Limits Calculation and Enforcement

Limits are calculated based on the timestamp of each request, ensuring that bursts of activity are not unfairly penalized. Our system uses a combination of algorithms and statistical analysis to enforce limits, including:

* **Request timestamp**: Requests are assigned a unique timestamp upon receipt. This information is used to track usage patterns and calculate limits.
* **IP blocking**: IP addresses are temporarily or permanently blocked if rate limiting limits are breached. This helps prevent abuse from a single IP address.
* **Rate limiting timeouts**: Excessive bursts of activity may trigger temporary rate limiting timeouts, lasting up to 10 minutes.

## Exception Handling

DevAPI makes exceptions for legitimate business use cases, such as:

* **Test environments**: Developers can register for a test environment with increased rate limits (up to 1,000 RPM) for a period of one month.
* **Enterprise agreements**: Large enterprise customers may be eligible for custom rate limiting configurations.

To apply for an exception, please contact our support team with your company's unique requirements and justification.
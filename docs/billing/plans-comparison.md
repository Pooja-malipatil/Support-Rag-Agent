---
source_name: plans-comparison
section: Billing
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Billing Overview
The DevAPI billing system provides three tiers of plans: Free, Pro, and Enterprise. Each plan offers a unique set of features and pricing.

### Pricing Plans

| Plan | Request Limitation | SLA Percentage | Monthly Fee |
| --- | --- | --- | --- |
| Free | 100,000 requests | N/A | $0 |
| Pro | 1,000,000 requests | 99.9% | $49/month |
| Enterprise | Custom pricing | Dedicated support | Custom |

## Charging for Requests
The DevAPI billing system charges for each request made to our API. The charge per request is as follows:

* Free plan: $0.00001 per request ( effective rate of $1,000,000 requests)
* Pro plan: $0.000005 per request (effective rate of $50,000 requests)
* Enterprise plan: Custom pricing based on usage

### Request Limit Exceeded
If the number of requests exceeds the limit for a given plan, the API will return a 429 Too Many Requests HTTP status code with an error message:

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Error Message: Request limit exceeded for Pro plan.
```

Example response body:
```json
{
    "error": "RequestLimitExceeded",
    "message": "Request limit exceeded for Pro plan."
}
```

## Cancellation and Refund Policy
To cancel an account, please contact our support team via email at [support@devapi.com](mailto:support@devapi.com). A refund will be processed within 7-10 business days of the cancellation request.

### Refund Error
If a refund is not processed due to invalid or incomplete information, the API will return a 400 Bad Request HTTP status code with an error message:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Error Message: Invalid refund request.
```

Example response body:
```json
{
    "error": "InvalidRefundRequest",
    "message": "Invalid refund request."
}
```

## Billing Cycles and Auto-Renewal
Billing cycles occur on the 1st day of each month. The DevAPI billing system uses a monthly billing cycle, with payments due on the same date as the previous month. Payments are auto-renewed if not cancelled before the end of the billing period.

### Overdue Payment Error
If payment is overdue for more than 30 days, the API will return a 503 Service Unavailable HTTP status code with an error message:

```
HTTP/1.1 503 Service Unavailable
Content-Type: application/json
Error Message: Overdue payment.
```

Example response body:
```json
{
    "error": "OverduePayment",
    "message": "Overdue payment."
}
```
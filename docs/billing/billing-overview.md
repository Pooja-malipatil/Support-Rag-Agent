---
source_name: billing-overview
section: Billing
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Billing Overview

The DevAPI billing system is designed to provide flexible and scalable pricing plans for our customers. We offer both usage-based and subscription pricing models, allowing you to choose the best fit for your project's needs.

## Pricing Models

We have two primary pricing models: Usage-Based and Subscription.

- **Usage-Based:** Charges based on actual resource utilization (e.g., API calls, data transfer). Rates are $0.001 per request for basic plans, increasing with tiered increments as the usage level increases.
- **Subscription:** Offers a fixed monthly fee for a set amount of resources. These rates start at $100/month for 100 requests and scale up based on resource demand.

### Example Request

To verify your current billing plan's details, use the GET /billing/plans endpoint:
```bash
curl -X GET \
  https://api.devapi.com/v1/billing/plans \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

## Billing Cycle

Our standard billing cycle is a 30-day month. However, for enterprise customers, we can accommodate custom billing cycles upon request.

### Example Billing Schedule

For example, if your usage exceeds $500 in the current billing period, you will receive an invoice by the end of that month with payment due within 15 days of receipt.
```bash
curl -X GET \
  https://api.devapi.com/v1/invoices/this_month \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

## Invoice Generation

Invoices are generated at the beginning and midpoint of each billing cycle, or as needed for custom plans.

### Example Invoice Response

When generating an invoice using the POST /billing/invoices endpoint:
```bash
curl -X POST \
  https://api.devapi.com/v1/billing/invoices \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -d '{"amount": 500, "currency": "USD"}'
```

## Payment Methods

We accept major credit cards (Visa, Mastercard), PayPal, and wire transfers.

### Example Payment Response

For a successful payment made with the POST /payment endpoint:
```bash
curl -X POST \
  https://api.devapi.com/v1/payment \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -d '{"amount": 500, "currency": "USD"}'
```

### Error Handling

- **InvalidPayment:** 400 Bad Request (payment failure due to invalid credentials).
- **PaymentFailed:** 500 Internal Server Error (payment processing failed).

## Troubleshooting

If you encounter issues with billing or payment processing, please contact our support team.

### Example Support Request

To report an issue using the POST /support/requests endpoint:
```bash
curl -X POST \
  https://api.devapi.com/v1/support/requests \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -d '{"description": "Billing error", "email": "user@example.com"}'
```

### Response

Upon successful submission, you will receive a confirmation response:
```bash
curl -X GET \
  https://api.devapi.com/v1/support/requests/this_request \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

This guide outlines the key aspects of DevAPI billing and payment processes. If you need more information or have questions, feel free to reach out to our support team at any time.
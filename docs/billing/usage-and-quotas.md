---
source_name: usage-and-quotas
section: Billing
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Monitoring Usage and Quotas

## Getting Started

The DevAPI usage dashboard provides a comprehensive overview of your project's usage, including data storage, API calls, and user activity. To access the dashboard, send a GET request to `https://devapi.com/dashboard`. The response will include a JSON object with the following properties:

- `usage_data`: an array of objects containing usage metrics for each resource type
- `quota_status`: an object indicating whether you have reached your current quota limits

Example Response:
```json
{
  "usage_data": [
    {
      "resource": "storage",
      "used": 100,
      "limit": 500
    },
    {
      "resource": "api_calls",
      "used": 200,
      "limit": 1000
    }
  ],
  "quota_status": {
    "storage": true,
    "api_calls": false
  }
}
```
## Setting Spending Limits

To set spending limits for your project, send a POST request to `https://devapi.com/settings/spending-limits`. The request body should contain the following properties:

- `resource`: the type of resource to set a limit for (e.g. "storage", "api_calls")
- `limit`: the new limit value

Example Request:
```bash
curl -X POST \
  https://devapi.com/settings/spending-limits \
  -H 'Content-Type: application/json' \
  -d '{"resource": "storage", "limit": 750}'
```
The response will include a JSON object with a `status` property indicating whether the request was successful.

Example Response:
```json
{
  "status": "success",
  "message": "Spending limit for storage set to 750 units"
}
```

## Alerts for Quota Thresholds

To enable alerts for quota thresholds, send a POST request to `https://devapi.com/settings/alerts`. The request body should contain the following properties:

- `resource`: the type of resource to monitor (e.g. "storage", "api_calls")
- `threshold`: the percentage value above or below which an alert will be triggered

Example Request:
```bash
curl -X POST \
  https://devapi.com/settings/alerts \
  -H 'Content-Type: application/json' \
  -d '{"resource": "storage", "threshold": 80}'
```
The response will include a JSON object with a `status` property indicating whether the request was successful.

Example Response:
```json
{
  "status": "success",
  "message": "Alert enabled for storage usage above 80%"
}
```

## Overage Charges

If your project exceeds its allocated quota, you will be charged an overage fee based on the amount of usage exceeding the limit. The fee is calculated as follows:

- `storage_overage`: $0.10 per unit of usage exceeding the limit
- `api_call_overage`: $0.05 per API call above the limit

Example Calculation:
```bash
storage_usage = 1000 units (limit) + 200 extra units (overage)
storage_fee = 0.10 \* (200 - 500) = $20.00

api_call_usage = 1200 calls (limit) + 50 extra calls (overage)
api_call_fee = 0.05 \* 50 = $2.50
```
The total overage fee would be `$22.50`.
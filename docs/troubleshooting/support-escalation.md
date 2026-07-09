---
source_name: support-escalation
section: Troubleshooting
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Getting Support Through DevAPI

DevAPI provides multiple channels for support, catering to different needs and plan tiers. This guide outlines the process of getting help through our community forums, email support, dedicated Slack, and SLA response times by plan.

### Community Forums
The DevAPI community forum is a great place to find answers to common questions and issues. All plans have access to this resource, but Pro+ tier users can also report their issues directly on the forum without waiting for moderation.

- HTTP Status Code: 200 OK
- Response Time: 1-2 minutes

Example:
```bash
GET /support/forums HTTP/1.1
Host: forums.devapi.com

Response:
{
    "results": [
        {
            "id": 12345,
            "title": "Error 500"
        }
    ]
}
```
If you're unable to find an answer on the forum, you can submit a request for assistance.

### Email Support (Pro+)
For Pro+ tier users, email support is available. Please note that this service has limited hours of operation:

- Monday - Friday: 9:00 AM - 5:00 PM EST
- Response Time: 1 hour

To report an issue via email, include your order number and a detailed description of the problem in the subject line.

Example Email:
```bash
Subject: Error on Order #12345

Dear DevAPI Support,

I am experiencing an error with my account. Please assist me as soon as possible.

Best regards,
[Your Name]
```
Keep in mind that if you're outside our regular business hours, your request will be processed the next business day.

### Dedicated Slack (Enterprise)
The Enterprise plan includes a dedicated Slack channel for priority support:

- HTTP Status Code: 202 Accepted
- Response Time: Immediate

To initiate a session with your dedicated support team, simply mention `@devapi-support` in your channel message.

Example:
```bash
POST /support slack HTTP/1.1
Host: slack.devapi.com
Content-Type: application/json

{
    "channel": "#my-team",
    "message": "@devapi-support Need help with my account"
}
```
Please note that this service requires 30 days of active subscription.

### SLA Response Times by Plan

| Plan | Response Time |
| --- | --- |
| Community Forum | 1-2 minutes |
| Pro+ Email Support | 1 hour |
| Enterprise Dedicated Slack | Immediate |

SLA (Service Level Agreement) is subject to change. DevAPI reserves the right to adjust our response times at any time without notice.

### Error Codes
For technical issues, you may encounter one of the following error codes:

- `500 Internal Server Error`: An unexpected server-side error.
```bash
HTTP/1.1 500 Internal Server Error
Content-Type: text/plain; charset=utf-8

Internal Server Error
```
- `504 Gateway Timeout`: The request timed out due to network issues or high traffic.
```bash
HTTP/1.1 504 Gateway Timeout
Content-Type: text/plain; charset=utf-8

Gateway Timeout
```

Remember to report any errors you encounter while accessing our support resources so we can work towards improving them.

### Additional Resources
If you're looking for more detailed information on DevAPI's services or troubleshooting guides, please visit our official documentation at <https://docs.devapi.com>.
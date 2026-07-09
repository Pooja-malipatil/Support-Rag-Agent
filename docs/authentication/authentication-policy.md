---
source_name: authentication-policy
section: Authentication
last_updated: "2024-03-01"
doc_type: policy
access_level: public
---

## Authentication Security Policy
=====================================

### Key Rotation Requirements
---------------------------

DevAPI requires all API clients to rotate their API keys every 90 days. This ensures that any potential security breaches are minimized and helps prevent unauthorized access to our services.

To implement key rotation, clients must use the `RotateApiKey` endpoint to request a new API key. The response will include the new key in JSON format, as shown below:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "apiKey": "new_api_key_here"
}
```
If the client fails to rotate their API key within the specified timeframe, they will receive a `401 Unauthorized` response with an error message indicating the number of days remaining before rotation is required.

### Prohibited Uses
------------------

DevAPI prohibits the use of our APIs for any purposes that are illegal, unethical, or damaging to others. Specifically, clients are prohibited from:

* Using our APIs to harvest or collect personal data without explicit consent
* Engaging in spamming or phishing activities using our APIs
* Conducting denial-of-service (DoS) or distributed denial-of-service (DDoS) attacks against other systems

Violations of these prohibitions may result in termination of API access and/or legal action.

### Compliance Requirements
-------------------------

DevAPI clients are required to comply with the following compliance requirements:

* All requests must be made using HTTPS (TLS 1.2 or higher)
* All responses must be validated against the `Content-Type` header
* Client IDs must be provided in each request, formatted as `client_id=1234567890`
* Errors must be handled according to the specifications outlined in our error handling guide

 Failure to comply with these requirements may result in API access being terminated or modified.

### Consequences of Violation
---------------------------

DevAPI takes security breaches and violations seriously. As a result, clients who violate this policy may face consequences such as:

* Termination of API access
* Suspension or revocation of client ID
* Financial penalties (up to $100,000 per incident)
* Exposure of sensitive data

In extreme cases, DevAPI reserves the right to pursue legal action against clients who repeatedly violate this policy.
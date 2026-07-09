---
source_name: webhook-security
section: Webhooks
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Webhooks Guide
======================================================

## Overview of Webhook Security
---------------------------

DevAPI's webhook service is designed to allow secure communication between our servers and your applications. To ensure the integrity and authenticity of these interactions, we require strict security measures to be implemented. This guide outlines the recommended practices for securing webhooks using HMAC signature verification, replay attack prevention, IP allowlisting, and HTTPS requirements.

## Signature Verification using HMAC
------------------------------

To verify the signature sent by DevAPI in our webhook notifications, you must use the following steps:

1.  Store the shared secret key securely.
2.  Generate a signature for the request body using your chosen hashing algorithm (e.g., SHA-256).
3.  Include the base64 encoded signature as a header parameter named `X-HMAC-SHA256`.
4.  Verify the received signature by comparing it to the expected signature.

**Example Signature Verification Code**

```python
import hmac
import hashlib

shared_secret_key = b"your_shared_secret_key_here"
signature_header = "X-HMAC-SHA256"

request_body = b"your_request_body_here"

# Generate the expected signature
expected_signature = hmac.new(shared_secret_key, request_body, hashlib.sha256).digest()

# Extract the received signature from the header parameter
received_signature_header_value = request.headers.get(signature_header)
received_signature = base64.b64decode(received_signature_header_value)

# Compare the received and expected signatures
if hmac.compare_digest(received_signature, expected_signature):
    # Signature verified successfully
else:
    # Handle verification failure
```

**HTTP Status Code for Invalid Signature**

*   401 Unauthorized - Returned when an invalid or missing signature is provided.

## Replay Attack Prevention
----------------------

To prevent replay attacks, DevAPI will automatically include a unique identifier in each webhook notification. This identifier can be used to check if the request has been received before by checking our database of previous requests. If the request does not exist, you should return an error response with a 429 Too Many Requests status code.

**Example Replay Attack Prevention Code**

```python
import datetime

# Get the unique identifier from the request headers or body
unique_id = request.headers.get("X-DevAPI-Replay-Id")

# Check if the request already exists in our database
if not db.check_unique_id(unique_id):
    # Return a 429 Too Many Requests error response
    return jsonify({"error": "Too many requests"}), 429

# If the request exists, process it as usual
```

**HTTP Status Code for Replay Attack**

*   429 Too Many Requests - Returned when a replay attack is detected.

## IP Allowlisting
-----------------

To improve security, DevAPI can be configured to only accept webhook requests from specific IP addresses. You can specify these allowed IPs by passing them in the `X-DevAPI-Allow-Ip` header parameter.

**Example IP Allowlisting Configuration**

```python
# Specify the allowed IPs as a comma-separated list
allowed_ips = ["192.168.1.100", "192.168.1.200"]

def validate_ip(ip_address):
    return ip_address in allowed_ips

request_header_value = request.headers.get("X-DevAPI-Allow-Ip")
if not validate_ip(request_header_value):
    # Return a 403 Forbidden error response
    return jsonify({"error": "Forbidden IP"}), 403
```

**HTTP Status Code for Invalid IP**

*   403 Forbidden - Returned when an invalid or missing `X-DevAPI-Allow-Ip` header parameter is provided.

## HTTPS Requirements
------------------

All webhook requests must be made over a secure connection using HTTPS. This ensures that all data transmitted between our servers and your application remains encrypted and tamper-proof.

**Example HTTPS Request**

```python
import ssl

# Create an SSL context for the request
context = ssl.create_default_context()
context.check_hostname = False  # Disable hostname checking
context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

# Make the HTTPS request using the SSL context
request = requests.get("https://api.devapi.com/webhook", verify=context)
```

**HTTP Status Code for Insecure Request**

*   403 Forbidden - Returned when an insecure HTTP request is made.

By following these guidelines and implementing the necessary security measures, you can ensure that your application receives secure and reliable webhook notifications from DevAPI.
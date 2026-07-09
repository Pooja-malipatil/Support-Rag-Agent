---
source_name: ip-allowlisting
section: Security
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# IP Allowlisting Guide for DevAPI

## Introduction to IP Allowlisting

IP allowlisting is a security feature that restricts API access to specific IP addresses or ranges of IP addresses. This guide provides detailed information on how to configure and use IP allowlisting with DevAPI.

## Configuring Static IP Allowlisting

To set up static IP allowlisting, you can use the `ALLOWED_IPS` header in your API requests. The allowed IPs should be specified in CIDR notation (e.g., `192.168.1.0/24`). Here's an example:

```http
GET /api/data HTTP/1.1
Host: devapi.com
ALLOWED_IPS: 192.168.1.0/24, 10.0.0.0/16
```

If the request is made from a whitelisted IP address, DevAPI will return a `200 OK` response with the requested data. If not, it will return a `403 Forbidden` response.

## Configuring Dynamic IP Allowlisting

To allow access to dynamic IPs, you can use the `X-Forwarded-For` header in your API requests. This header specifies the original IP address of the client making the request. Here's an example:

```http
GET /api/data HTTP/1.1
Host: devapi.com
X-Forwarded-For: 192.168.1.100
```

If the `X-Forwarded-For` header is present and matches a whitelisted IP address or range, DevAPI will return a `200 OK` response with the requested data.

## Allowlisting for CI/CD Pipelines

DevAPI provides an additional feature to allowlist specific IPs for CI/CD pipelines. This can be done by setting the `CI/CD_allowlisted_ips` environment variable when running your pipeline. The allowed IPs should be specified in CIDR notation (e.g., `192.168.1.0/24`). Here's an example:

```bash
export CI/CD_allowlisted_ips=192.168.1.0/24,10.0.0.0/16
```

When your pipeline runs, DevAPI will automatically allow access to the specified IP addresses or ranges.

## Timeouts and Error Handling

If a request is made from an unwhitelisted IP address, DevAPI will return a `403 Forbidden` response with a timeout of 30 seconds. If the request times out, it will also return a `504 Gateway Timeout` response.

```http
GET /api/data HTTP/1.1
Host: devapi.com
Timeout: 30s

HTTP/1.1 403 Forbidden
Content-Type: application/json
{
  "error": "Forbidden",
  "code": 403,
  "message": "API access is restricted to specific IP addresses."
}
```

```http
GET /api/data HTTP/1.1
Host: devapi.com
Timeout: 60s

HTTP/1.1 504 Gateway Timeout
Content-Type: application/json
{
  "error": "Gateway Timeout",
  "code": 504,
  "message": "API request timed out."
}
```

## Conclusion

IP allowlisting is an essential security feature for DevAPI that restricts API access to specific IP addresses or ranges. By following this guide, you can configure and use IP allowlisting to ensure secure access to your APIs.
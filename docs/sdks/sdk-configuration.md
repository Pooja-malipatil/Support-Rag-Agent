---
source_name: sdk-configuration
section: SDKs
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## SDK Configuration Options: Timeout Settings

The DevAPI SDK provides flexible timeout settings to accommodate varying application requirements. The `timeout` option allows developers to specify a request timeout in seconds, while the `connectTimeout` and `readTimeout` options control the timeout for establishing connections and reading responses, respectively.

Example configuration:
```javascript
const config = {
  timeout: 30000, // 30 seconds
  connectTimeout: 20000, // 20 seconds
  readTimeout: 5000, // 5 seconds
};
```
HTTP status codes that may be returned when a request times out include:

* `408 Request Timeout` (HTTP/1.1)
* `504 Gateway Timeout` (HTTP/1.1)

## SDK Configuration Options: Retry Configuration

The DevAPI SDK also provides retry options to handle transient errors and improve overall application reliability. The `retryCount` option specifies the maximum number of retries, while the `minDelay` and `maxDelay` options control the minimum and maximum delay between retries.

Example configuration:
```javascript
const config = {
  retryCount: 3,
  minDelay: 1000, // 1 second
  maxDelay: 5000, // 5 seconds
};
```
Error codes that may be returned when a retry fails include:

* `500 Internal Server Error` (HTTP/1.1)
* `502 Bad Gateway` (HTTP/1.1)

## SDK Configuration Options: Base URL Override

The DevAPI SDK allows developers to override the base URL for API requests using the `baseUrl` option.

Example configuration:
```javascript
const config = {
  baseUrl: 'https://devapi.com/v2',
};
```
Note that this option can be used to test specific features or to use a different endpoint when development is not supported.

## SDK Configuration Options: Logging

The DevAPI SDK provides logging options to help developers diagnose issues and monitor API requests. The `logLevel` option specifies the log level, with possible values including `debug`, `info`, `warn`, and `error`.

Example configuration:
```javascript
const config = {
  logLevel: 'info',
};
```
Logging levels are as follows:

* `debug`: Detailed debug messages (HTTP/1.1: `200 OK`)
* `info`: General informational messages (HTTP/1.1: `200 OK` or `400 Bad Request`)
* `warn`: Warnings and potential issues (HTTP/1.1: `500 Internal Server Error`)
* `error`: Critical errors (HTTP/1.1: `500 Internal Server Error`)

## SDK Configuration Options: Proxy Settings

The DevAPI SDK allows developers to configure proxy settings for API requests using the `proxy` option.

Example configuration:
```javascript
const config = {
  proxy: 'https://my-proxy.com:8080',
};
```
Proxy settings can be used to bypass firewalls, use a different network connection, or to test specific features when development is not supported.
---
source_name: error-handling-best-practices
section: Errors
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Errors
### Introduction

At DevAPI, we understand that errors are an inevitable part of our services. This guide outlines best practices for handling errors in a way that ensures reliability, security, and a good user experience.

### Retry Logic

We use a retry logic mechanism to handle transient failures that may occur during request processing. The retry policy has the following parameters:
* Maximum number of retries: 3
* Exponential backoff multiplier: 2
* Initial timeout: 500ms
* Maximum wait time: 30s

To implement this in your client code, use the following example:
```java
RetryConfig config = new RetryConfig(3, 2);
try {
    // Make API request
} catch (Exception e) {
    // Apply retry logic
    if (e instanceof transient failure) {
        try {
            Thread.sleep(e.getInitialTimeout());
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
        throw new RequestExecutionException("Transient error", e);
    } else {
        throw new PermanentError(e, "Permanent error");
    }
}
```
### Circuit Breakers

To prevent cascading failures when dealing with persistent errors, we use circuit breakers. The circuit breaker has the following parameters:
* Time window: 60s
* Error threshold: 5 consecutive errors
* Timeout duration: 30s

When a circuit breaker is triggered, all subsequent requests are returned with an HTTP status code of `503 Service Unavailable` until it times out.

To implement this in your client code, use the following example:
```java
CircuitBreakerConfig config = new CircuitBreakerConfig(60s, 5);
try {
    // Make API request
} catch (Exception e) {
    // Apply circuit breaker logic
    if (e instanceof transient failure) {
        throw new RequestExecutionException("Transient error", e);
    } else {
        throw new PermanentError(e, "Permanent error");
    }
}
```
### Logging Errors

We log all errors with the following format:
```json
{
    "timestamp": 1643723400,
    "error_code": 404,
    "message": "Resource not found",
    "request_id": "123456789",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.37"
}
```
### User-Facing Error Messages

We use the following error codes and messages for user-facing errors:
* `400 Bad Request`: "Invalid request data. Please try again."
* `401 Unauthorized`: "Authentication failed. Please re-enter your credentials."
* `404 Not Found`: "Resource not found. Please check the URL."

To display these error messages to users, use the following example:
```javascript
try {
    // Make API request
} catch (Exception e) {
    if (e instanceof transient failure) {
        renderError(`Invalid request data. Please try again.`);
    } else if (e instanceof permanent error) {
        renderError(`Authentication failed. Please re-enter your credentials.`);
    } else {
        renderError("Resource not found. Please check the URL.");
    }
}
```
Note: The specific values and formats used in this documentation are fictional and for demonstration purposes only. In a real-world scenario, you should use production-ready error handling mechanisms and adapt them to your application's specific requirements.
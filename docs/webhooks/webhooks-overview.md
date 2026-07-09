---
source_name: webhooks-overview
section: Webhooks
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Introduction to Webhooks

A webhook is a callback function that is triggered by an event in our API. When a new resource is created or updated, we can notify your application via HTTP POST using the provided URL.

## Key Differences Between Webhooks and Polling

Webhooks differ from polling in several key ways:

*   **Reduced latency**: With webhooks, you only receive updates when there's significant change, reducing unnecessary requests.
*   **Increased efficiency**: Since you only request data when necessary, you can better control your server load.

## Types of Webhooks Available

We offer three types of webhooks for different use cases:

### 1. `users.created` and `users.updated`

When a new user is created or an existing one is updated, we send a webhook notification to the provided URL with the following data:
*   `user_id`: The ID of the affected user.
*   `email`: The email address associated with the user.

    Example request body:

    ```json
{
    "user_id": 123,
    "email": "john.doe@example.com"
}
```

### 2. `orders.placed` and `orders.cancelled`

When a new order is placed or an existing one is cancelled, we send a webhook notification to the provided URL with the following data:
*   `order_id`: The ID of the affected order.
*   `total_cost`: The total cost of the order.

    Example request body:

    ```json
{
    "order_id": 456,
    "total_cost": 100.00
}
```

### 3. `error`

When an error occurs, we send a webhook notification to the provided URL with the following data:
*   `error_code`: The code corresponding to the error.
*   `error_message`: A description of the error.

    Example request body:

    ```json
{
    "error_code": 404,
    "error_message": "Resource not found"
}
```

## Best Practices for Using Webhooks

Here are some guidelines on how to use webhooks effectively in your application:

*   **Handle requests within a reasonable time frame**. We expect responses within 10 seconds of receiving the request.
*   **Return HTTP status code 204 No Content** if the data has changed but no response body is required.

## Troubleshooting Common Issues

If you encounter any issues with our webhooks, here are some common problems and their solutions:

### 1. Failed requests due to invalid URLs

If your webhook URL is not properly formatted, you'll receive a `400 Bad Request` error.

Solution: Ensure that the URL starts with `https://api.devapi.com/webhooks/` followed by the actual endpoint.

    Example valid URL: `https://api.devapi.com/webhooks/users.created`

### 2. Incomplete or missing data

If the request body is incomplete or missing required fields, we'll assume it's an invalid request and return a `400 Bad Request` error.

Solution: Verify that all required fields are present in your code to ensure successful data exchange.

    Example complete request body:

    ```json
{
    "user_id": 123,
    "email": "john.doe@example.com"
}
```

### 3. Timeouts

If you fail to respond within the expected time frame (10 seconds), we'll assume it's a timeout and return a `500 Internal Server Error`.

Solution: Ensure that your server can handle incoming requests efficiently.

    Example response:

    ```json
HTTP/1.1 204 No Content
```
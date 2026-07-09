---
source_name: python-sdk-quickstart
section: SDKs
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Installing the DevAPI Python SDK

The DevAPI Python SDK is a lightweight library that allows you to interact with our API using Python. To install the SDK, run the following command in your terminal:

```bash
pip install devapi
```

This will download and install the latest version of the DevAPI Python SDK.

## Initializing the SDK

After installation, you need to initialize the SDK by creating an instance of the `DevApiClient` class and specifying your API credentials. You can do this using the following code snippet:

```python
import devapi

client = devapi.DevApiClient(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY'
)
```

Replace `'YOUR_API_KEY'` and `'YOUR_SECRET_KEY'` with your actual DevAPI API key and secret key.

## Making a First Request

To make the first request, you can use the `get()` method of the `DevApiClient` instance. Here's an example:

```python
import devapi

client = devapi.DevApiClient(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY'
)

response = client.get('/users')
print(response.json())
```

In this example, we're making a GET request to the `/users` endpoint. The response will be returned as a JSON object.

## Handling Responses

When you make a request to the DevAPI API, you'll receive a response with an HTTP status code. Here are some common status codes and their meanings:

| Status Code | Meaning |
| --- | --- |
| 200 OK | The request was successful. |
| 401 Unauthorized | Authentication failed or token is missing. |
| 404 Not Found | The requested resource was not found. |
| 500 Internal Server Error | An unexpected error occurred on the server-side. |

You can check the HTTP status code and handle it accordingly using the following code snippet:

```python
import devapi

client = devapi.DevApiClient(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY'
)

try:
    response = client.get('/users')
    if response.status_code == 200:
        print("Users were found successfully")
    elif response.status_code == 401:
        print("Authentication failed. Please try again.")
except devapi DeVError as e:
    print(f"An error occurred: {e.error_code}")
```

## Handling Errors

The DevAPI SDK uses a custom error class `devapi.DeVError` to handle errors. The error code is used to identify the type of error that occurred.

Here are some common error codes and their meanings:

| Error Code | Meaning |
| --- | --- |
| 1 | Network connection failed. |
| 2 | Request timed out. |
| 3 | Authentication failed or token is missing. |

You can handle errors using the following code snippet:

```python
import devapi

client = devapi.DevApiClient(
    api_key='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY'
)

try:
    response = client.get('/users', timeout=10)
    if response.status_code == 200:
        print("Users were found successfully")
    else:
        raise devapi.DeVError(response.status_code)
except devapi.DeVError as e:
    if e.error_code == 1:
        print("Network connection failed. Please try again.")
    elif e.error_code == 2:
        print("Request timed out. Please try again.")
```

This is a quickstart guide to get you started with the DevAPI Python SDK. For more information, please refer to our API documentation and API reference section.
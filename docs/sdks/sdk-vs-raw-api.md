---
source_name: sdk-vs-raw-api
section: SDKs
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# SDKs
## Overview of DevAPI SDKs

DevAPI offers two primary options for interacting with our API: the official SDK and raw HTTP API. The choice between these two options depends on your specific use case, development requirements, and performance considerations.

The official SDK provides a streamlined experience for many common tasks, such as handling authentication, encoding requests, and parsing responses. It also includes features like automatic retry mechanisms, caching, and logging. On the other hand, using raw HTTP API gives you full control over every request, allowing for more customization and flexibility.
## Which SDK to Use

When deciding which SDK to use, consider the following factors:
- **Development speed**: If you need to develop a project quickly, the official SDK is usually the better choice. It provides pre-built functionality that reduces development time.
- **Complexity**: For more complex tasks or projects requiring low-level control, using raw HTTP API might be necessary.
- **Performance**: Raw HTTP API can offer better performance for high-traffic or real-time applications, as it eliminates any potential overhead from the SDK.

## What Does the SDK Handle Automatically?

The DevAPI official SDK handles several tasks automatically:
- Authentication: The SDK takes care of managing your access tokens, authentication headers, and refresh tokens.
- Encoding requests: The SDK encodes requests with the correct content type and parameters, reducing the risk of errors or corruption during transmission.
- Parsing responses: The SDK parses response bodies into JSON-like objects, making it easier to work with the data in your application.

However, some features are not handled automatically:
- **Timeouts**: When using raw HTTP API, you must manually set timeouts for requests. For example, setting `maxWaitTime` (default 30 seconds).
- **Error handling**: While the SDK will throw errors if authentication fails or other issues arise, you may need to implement custom error handling depending on your application's specific requirements.

## Code Snippets

Here is an example of using the official DevAPI SDK in Python:
```python
import requests

# Initialize the DevAPI client with access token
client = requests.Session()
client.auth = ('your_client_id', 'your_access_token')

# Create a request to get data from the API
response = client.get('https://api.devapi.com/data/endpoint')

# Check if the response was successful
if response.status_code == 200:
    # Parse the response body into JSON-like object
    data = response.json()
    print(data)
else:
    # Handle errors
    error_code = response.status_code // 100
    error_message = 'Unknown Error' + str(error_code) + ': ' + response.text
    raise Exception(error_message)
```

And here's an example using raw HTTP API in Python (for comparison):
```python
import requests

# Set headers and parameters
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_access_token'
}

params = {
    'param1': 'value1',
    'param2': 12345
}

try:
    response = requests.get('https://api.devapi.com/data/endpoint', headers=headers, params=params)
except requests.Timeout as e:
    # Handle timeout error
    raise TimeoutError('Timeout occurred: {}'.format(e))
except requests.exceptions.RequestException as e:
    # Handle other exceptions
    raise Exception('Request Error: {}'.format(e))
else:
    # Check if response was successful
    if response.status_code != 200:
        # Get the HTTP status code and parse error message
        status_code = response.status_code // 100
        error_message = 'HTTP Error {}: {}'.format(status_code, response.text)
        raise Exception(error_message)
```

## Performance Considerations

The official SDK is optimized for performance in many scenarios, but raw HTTP API can offer better performance when:
- **Handling high traffic**: By avoiding overhead from the SDK and optimizing request parameters.
- **Real-time applications**: When strict latency requirements are necessary.

However, be aware that using raw HTTP API may require more manual optimization to achieve optimal performance.
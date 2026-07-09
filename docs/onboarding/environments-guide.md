---
source_name: environments-guide
section: Onboarding
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Test vs Production Environments
The DevAPI platform provides a robust infrastructure to support developers and organizations through different environments. Two main types of environments are available for use: test and production.

### API Keys per Environment
Each environment has its own unique API key, which is used for authentication purposes when making requests to the API. The keys can be found in the corresponding environment settings sections within the developer console.

For example, a test environment API key might have a value of `test-api-key-12345`, while a production environment API key would have a value of `prod-api-key-67890`. It is essential to use the correct API key for each environment to avoid unauthorized access to data and potential security breaches.

### Sandbox Behavior
The DevAPI platform includes sandbox environments where developers can test their APIs without affecting the actual data. Sandbox behavior is enabled by default, but it can be disabled if necessary.

When sandbox behavior is enabled, certain features are simulated or limited for testing purposes, such as limited data availability or reduced API performance. To disable sandbox behavior, you need to set an environment variable `DEVAPI_SANDBOX` to `false`.

### Test Data
Test data is available in the test environments and can be used by developers to simulate real-world scenarios without affecting actual data.

Test data includes sample user information, orders, products, and other relevant data. However, please note that the availability of specific data may vary across different test environment configurations. 

For example, when making a request to retrieve all users in the test environment, you can use the `GET /users` endpoint with an authentication header containing your test API key.

```http
GET https://api.devapi.com/users HTTP/1.1
Host: api.devapi.com
Authorization: Bearer test-api-key-12345
```

## Promoting to Production
Once a developer is confident that their application is working correctly in the test environment, they can promote it to production.

To do this, you need to update your `environment.json` file with the correct API key for the production environment. The updated configuration should look like this:

```json
{
  "environment": "production",
  "api_key": "prod-api-key-67890"
}
```

Additionally, ensure that all necessary settings and configurations are in place before promoting to production.

### Example: Updating `environment.json`
To promote your application to production, you can update the `environment.json` file with the correct API key for the production environment. Here is an example of how this would look:

```json
{
  "environment": "production",
  "api_key": "prod-api-key-67890"
}
```

With this configuration, your application should now function correctly in the production environment.

### Error Handling and Timeouts

In case of errors or timeouts during API calls, you can expect a specific HTTP status code:

*   `404`: The requested resource could not be found. In this case, an error message will be returned.
*   `500`: An internal server error has occurred. You may need to retry the request after a short delay.

To configure timeouts for your API calls, you can use the following HTTP headers:

```http
GET https://api.devapi.com/users?timeout=10 HTTP/1.1
Host: api.devapi.com
Authorization: Bearer test-api-key-12345
```

In this example, the request will timeout after 10 seconds if it fails to complete successfully.

### Error Codes

DevAPI uses standard HTTP error codes for API requests. Below are some of the most common ones:

| Code | Description | Meaning |
| --- | --- | --- |
| 200 OK | The request was successful and returned data in the expected format. | The request was completed without any issues. |
| 400 Bad Request | The provided request was invalid or could not be processed by the server. | Typically used when a developer provides an invalid API key, invalid JSON payload, etc., which results in a bad request response. |
| 401 Unauthorized | The client's authentication credentials were invalid. The request is refused. | If the developer does not provide a valid API key or if the authentication fails for any reason (e.g., expired token).
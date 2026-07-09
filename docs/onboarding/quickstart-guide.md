---
source_name: quickstart-guide
section: Onboarding
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Creating an Account and Generating an API Key

To get started with DevAPI, you'll need to create an account. This can be done by visiting our [Sign Up page](https://devapi.com/signup) and following the prompts. Once your account is created, you'll receive an email inviting you to generate your first API key.

Your API key is a unique identifier that will be used to authenticate all requests made to DevAPI's endpoints. You can find this key in the [My Account page](https://devapi.com/account) under the "API Keys" tab. 

### Example: Creating an Account and Generating an API Key

```bash
# Create account using curl
curl -X POST \
  https://devapi.com/signup \
  -H 'Content-Type: application/json' \
  -d '{"username": "johndoe", "email": "johndoe@example.com", "password": "mypassword"}'

# Generate API key using curl
curl -X GET \
  https://devapi.com/account/apikeys \ 
  -H 'Authorization: Bearer <API_KEY>'
```

## Making the First Request

Once you have an API key, you can make your first request to DevAPI's endpoint. For this example, we'll use the [Users endpoint](https://devapi.com/docs/users).

### Example: Making a GET Request to Users Endpoint

```bash
# Make GET request using curl
curl -X GET \
  https://devapi.com/api/v1/users \ 
  -H 'Authorization: Bearer <API_KEY>'
```

This should return a JSON response with the following format:

```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "johndoe@example.com"
    }
  ]
}
```

## Understanding the Response Format

DevAPI's responses are in JSON format, with specific fields and values.

*   `data`: an array of objects representing the requested data. Each object will have an `id` field, a `name` field, and an `email` field.
*   `error`: an object containing error information if an error occurred while processing the request.
*   `meta`: an object containing metadata about the response.

### Example: Error Response

```json
{
  "error": {
    "code": 404,
    "message": "Not Found"
  }
}
```

Note that DevAPI uses HTTP status codes to indicate the outcome of a request. For example, a `200 OK` indicates success, while a `404 Not Found` indicates that no data was found.

### Example: Response with Meta

```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "johndoe@example.com"
    }
  ],
  "meta": {
    "total_count": 10,
    "page_size": 5,
    "current_page": 1
  }
}
```

## Timeout and Rate Limiting

DevAPI has a maximum request timeout of 30 seconds. If you exceed this limit, your requests will be rate-limited for a period of time before they are blocked.

The current API usage is as follows:

| Endpoint | Request Limit |
| --- | --- |
| Users endpoint | 100/minute |

You can check the current usage using our [API Usage page](https://devapi.com/stats).

### Example: Request Limit

```bash
# Check request limit using curl
curl -X GET \
  https://devapi.com/api/v1/rate \ 
  -H 'Authorization: Bearer <API_KEY>'
```

This should return the current usage for your API key.
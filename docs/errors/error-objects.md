---
source_name: error-objects
section: Errors
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Error Response Format

The DevAPI API returns error responses in a standardized format. Each error response is represented by an `error` object that includes information about the error.

### Error Object Structure
```json
{
  "error_code": int,
  "error_message": string,
  "request_id": string
}
```
The `error_code` field represents the error code returned by the API. The `error_message` field contains a human-readable description of the error. The `request_id` field is a unique identifier for the request that generated the error.

### Error Codes

DevAPI uses the following standard error codes:

| Error Code | Error Message |
| --- | --- |
| 40001 | Invalid Request Data |
| 40002 | Missing Required Fields |
| 50003 | Internal Server Error |
| 60005 | Timeout (Request Timed Out) |

### HTTP Status Codes
When an error response is returned, the API will include a corresponding HTTP status code in the `error_code` field. For example:

* `200 OK`: No error occurred.
* `400 Bad Request`: Invalid request data.
* `404 Not Found`: Resource not found.
* `500 Internal Server Error`: Server error.

### Example Values
```json
{
  "error_code": 40001,
  "error_message": "Invalid Request Data",
  "request_id": "1234567890abcdef"
}
```

## Debugging

DevAPI includes a request ID in each error response to facilitate debugging. The `request_id` field is a unique identifier for the request that generated the error.

### Request IDs
```bash
# Get the request ID from an error response
echo $error["request_id"]

# Use the curl command to print the request ID
curl -v -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.devapi.com/endpoint \
     -w "Request ID: %{http_code}" | grep Request ID:
```

## Error Handling

DevAPI encourages developers to handle errors properly in their applications. The error response format and error codes provided above can help with error handling.

### Timeouts
```bash
# Set a timeout for 30 seconds
curl -v --max-time 30 \
     https://api.devapi.com/endpoint \
     -H "Authorization: Bearer YOUR_API_KEY"
```

## Best Practices

When using the DevAPI API, make sure to handle errors properly and check the error response format regularly.
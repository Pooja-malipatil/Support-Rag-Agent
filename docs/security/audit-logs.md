---
source_name: audit-logs
section: Security
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Audit Logs API

## Event Types Logged

The DevAPI audit logs feature logs all significant events that occur within our platform. These events are categorized into three main types:

*   **User Activity**: All user-related actions, such as login attempts, account creations, and password changes.
*   **System Events**: System-level events like server restarts, database updates, and API request counts.
*   **Security Events**: Security-related events including IP blocking, password reset requests, and two-factor authentication failures.

Each event logged includes the following details:

-   User ID or IP Address
-   Date and Time of the event
-   Event Type (User Activity, System Events, or Security Events)
-   Additional context for each event

### Request Example

```http
GET /api/v1/audit/logs?limit=100&offset=0 HTTP/1.1
Host: devapi.com
Authorization: Bearer YOUR_API_KEY
```

Response:

```json
{
  "data": [
    {
      "id": 123,
      "userId": "JohnDoe",
      "ipAddress": "192.168.1.100",
      "eventType": "User Activity",
      "eventTime": "2023-02-20T14:30:00Z",
      "message": "User logged in from remote location"
    },
    {
      "id": 124,
      "userId": "",
      "ipAddress": "192.168.1.101",
      "eventType": "System Events",
      "eventTime": "2023-02-20T14:30:15Z",
      "message": "Server restart initiated"
    }
  ],
  "meta": {
    "totalCount": 200,
    "limit": 100
  }
}
```

## Log Retention

The DevAPI audit logs are retained for a maximum of **90 days**.

### Retrieving Logs Before Retention Period Ends

If you try to retrieve logs older than the retention period, an error response is returned with a corresponding HTTP status code:

```http
GET /api/v1/audit/logs?limit=100&offset=0 HTTP/1.1
Host: devapi.com
Authorization: Bearer YOUR_API_KEY
```

Response:

```json
{
  "error": {
    "code": "LOG_RETENTION_ERROR",
    "message": "Retrieved logs are older than the retention period (90 days)"
  },
  "status": 429,
  "headers": {
    "Retry-After": 3600
  }
}
```

## Exporting Logs

You can export your audit logs to a CSV file using the following API endpoint:

```http
POST /api/v1/audit/logs/export HTTP/1.1
Host: devapi.com
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "start": {
    "timeRange": {
      "startTime": "2023-02-01",
      "endTime": "2023-03-01"
    },
    "filter": {
      "eventType": ["User Activity", "System Events"]
    }
  },
  "end": {
    "timeRange": {
      "startTime": "2024-01-01",
      "endTime": "2024-02-01"
    },
    "filter": {
      "userId": []
    }
  }
}
```

Response:

```http
HTTP/1.1 201 Created
Location: https://devapi.com/api/v1/audit/logs/export?uuid=export_id_12345

{
  "uuid": "export_id_12345",
  "filename": "/path/to/exported_file.csv",
  "status": "success"
}
```

## Integrating with SIEM Systems

You can integrate your DevAPI audit logs with your Security Information and Event Management (SIEM) system using the following API endpoint:

```http
POST /api/v1/audit/logs/integrate-siem HTTP/11
Host: devapi.com
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "siemToken": "your_siem_token",
  "logFormat": {
    "json": true,
    "fields": ["id", "time", "type", "message"]
  }
}
```

Response:

```http
HTTP/1.1 201 Created
Location: https://devapi.com/api/v1/audit/logs/integrate-siem?uuid=siem_integration_12345

{
  "uuid": "siem_integration_12345",
  "status": "success"
}
```

### Error Handling

The following error codes are used when integrating with SIEM systems:

| Error Code | Description |
| --- | --- |
| invalid_siem_token | Invalid SIEM token provided |
| invalid_log_format | Invalid log format specified for SIEM integration |

If an error occurs during the integration, a JSON response is returned with the corresponding HTTP status code and error details.

```json
{
  "error": {
    "code": "invalid_siem_token",
    "message": "Invalid SIEM token provided"
  },
  "status": 401,
  "headers": {
    "Retry-After": 3600
  }
}
```
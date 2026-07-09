---
source_name: performance-troubleshooting
section: Troubleshooting
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Troubleshooting High Latency Causes
High latency issues can be caused by a variety of factors, including network congestion, server overload, and poor geographic routing. To troubleshoot high latency causes, first check the HTTP status codes returned by your API. For example, if you receive an HTTP 503 Service Unavailable response code, it may indicate that the server is overloaded or experiencing maintenance.

## Common Causes of High Latency

| Cause | Example Value |
| --- | --- |
| Network congestion | 429 Too Many Requests (server returns "Too Many Requests" error) |
| Server overload | 504 Gateway Timeout (server returns "Gateway Timeout" error) |

To resolve high latency issues, check your API usage patterns and adjust as needed. Be mindful of request quotas and avoid making excessive requests in a short period.

## Example: Adjusting Request Quotas

```bash
curl -X GET \
  https://api.devapi.com/endpoint \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  --max-redirs 10 \
  --max-time 300
```

In this example, the `--max-redirs` option limits the number of redirects to 10, and the `--max-time` option sets a timeout of 5 minutes (300 seconds).

## Connection Pooling Configuration

Connection pooling is a mechanism used by many frameworks to improve performance by reusing existing connections. However, if not configured correctly, it can lead to issues such as connection exhaustion or delayed responses.

## Best Practices for Connection Pooling
To configure connection pooling effectively:

* Set the `max-active` property in your application configuration to control the maximum number of active connections.
* Adjust the `min-idle` and `time-between-eviction-runouts` properties to balance connection reuse with new connection creation.

Example configuration:
```bash
application.properties
spring.datasource.url=jdbc:mysql://localhost:3306/devapi
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.max-active=100
spring.datasource.min-idle=5
spring.datasource.time-between-eviction-runouts=60
```

## Timeouts Configuration
Timeouts are an essential aspect of API design, as they help ensure that requests complete within a reasonable time frame.

### HTTP Timeout Configuration

To configure HTTP timeouts in your application:

* Set the `timeout` property in your Spring Boot configuration file.
* Use the `@org.springframework.web.client.RequestOptionsBuilder` class to customize request timeout values for individual endpoints.

Example configuration:
```java
import org.springframework.web.client.RequestOptions;

@Configuration
public class WebConfig {
 
    @Bean
    public RequestOptions requestOptions() {
        RequestOptions requestOptions = new RequestOptions();
        requestOptions.setTimeout(new Duration(60, TimeUnit.SECONDS));
        return requestOptions;
    }
}
```

### Geographic Routing

Geographic routing is a technique used to distribute traffic across multiple geographic locations. This can help improve performance by reducing the distance between users and API endpoints.

## Implementing Geographic Routing
To implement geographic routing in your application:

* Use a mapping service such as Google Maps or OpenCage Geocoder to determine user locations.
* Route requests based on user location using your preferred geographic routing algorithm.

Example code snippet:
```java
import com.google.maps.geocoding.Geocoding;
import com.google.maps.models.Place;

public class GeographicRoutingService {
 
    public Place routeRequest(String userId) throws Exception {
        // Determine user location using mapping service
        Geocoding geocoding = new Geocoding.Builder(GoogleMapsApiKey.INSTANCE).geocode(userId).build();
        List<Place> places = geocoding.geocode();
        return places.get(0);
    }
}
```

Note that this is a simplified example and may require additional implementation details to ensure optimal performance.
---
source_name: api-versioning-overview
section: Versioning
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# Versioning

## Overview of API Versioning

DevAPI uses a combination of URL path and HTTP headers to implement versioning for our APIs. This allows developers to choose the version they prefer, while also enabling seamless upgrades and backward compatibility.

## URL Path Versioning

For most endpoints, you can specify the desired API version by including it in the URL path. The format for versioned URLs is as follows:
```bash
https://devapi.com/v<version>/endpoint
```
Replace `<version>` with the numeric value of the API version you want to use.

Some examples:

* `https://devapi.com/v1/users` (API v1)
* `https://devapi.com/v2/orders` (API v2)

## Header-Based Versioning

For certain endpoints, it is required to specify the API version using an HTTP header. The `Accept-Version` header should be used with a value in the format of `<version>.json`.
```bash
GET /endpoint HTTP/1.1
Host: devapi.com
Accept-Version: v2.json
```
This will force the server to return data in API version 2.

## Current Versions

At this time, we support two main versions of our APIs:

* `v1`: The current stable version, which is deprecated.
* `v2`: The latest version, with significant updates and improvements over v1.

You can specify either `v1` or `v2` in your requests to get the data for that respective API version.

## Example Request

Here's an example request using both URL path versioning and header-based versioning:
```bash
GET https://devapi.com/v2/users HTTP/1.1
Host: devapi.com
Accept-Version: v1.json
```
This will send a request to the `/v2/users` endpoint, but also include `Accept-Version: v1.json`, which overrides the URL path to use API version 1.

## Handling Deprecation

Please note that API version 1 (`v1`) is deprecated and will be removed entirely in six months. If you're currently using `v1`, we recommend migrating to `v2` as soon as possible.

If you encounter any issues or errors while making requests, refer to our [Error Handling Guide](link_to_error_handling_guide) for more information on error codes and status codes used by DevAPI.
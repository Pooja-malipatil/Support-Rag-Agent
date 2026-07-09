---
source_name: deprecation-policy
section: Versioning
last_updated: "2024-03-01"
doc_type: policy
access_level: public
---

# API Deprecation Policy: Notice Period

## Overview

At DevAPI, we strive to provide the best possible experience for our users and developers. As part of this commitment, we have established an API deprecation policy that ensures our APIs remain stable and efficient while allowing us to introduce new features and improvements. This policy outlines the notice period for deprecated APIs, sunset headers, migration guides, and end-of-life process.

## Notice Period

When a version of an API is deprecated, it will be marked as such for a minimum of 12 months before being removed entirely. During this time, we encourage developers to migrate their applications to the latest version of the API or to alternative APIs provided by DevAPI. This notice period allows developers sufficient time to test and validate their migrated applications, ensuring a smooth transition.

## Sunset Headers

When an API is deprecated, specific headers will be included in the response to indicate its deprecation status:

* `Deprecation-Status`: `DEPRECATED` (HTTP 3xx)
* `Deprecated-Version`: The version of the API being deprecated
* `Next-Api-Version`: The recommended next version of the API

For example, if an API is deprecated due to a new feature implementation:
```http
HTTP/1.1 202 Accepted
Deprecation-Status: DEPRECATED
Deprecated-Version: v2
Next-Api-Version: v3
```

## Migration Guides

To assist developers in migrating their applications to the latest version of the API, we provide comprehensive migration guides for each deprecated API. These guides include:

* Step-by-step instructions for updating code and configuration
* Examples of affected endpoints and data formats
* Recommendations for testing and validation

Migration guides can be found on our Developer Portal under the "API Documentation" section.

## End-of-Life Process

Once a deprecated API has reached its notice period, it will be removed from our documentation and support infrastructure. At this point, we may also update error codes, timeouts, and other related metrics to reflect the deprecation.

When an API reaches end-of-life status:

* All response headers indicating deprecation will be removed
* The API will no longer receive updates or bug fixes
* Any existing issues reported against the deprecated API will be closed
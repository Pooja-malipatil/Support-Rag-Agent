---
source_name: javascript-sdk-quickstart
section: SDKs
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

# JavaScript SDK Quickstart

## Installing the SDK

To get started with the DevAPI JavaScript SDK, first install the package using npm:
```
npm install @devapi/sdk
```
Alternatively, you can use a package manager like yarn or pnpm:
```
yarn add @devapi/sdk
```
or
```
pnpm install @devapi/sdk
```
Make sure to check the version of the SDK installed on your system.

## CommonJS vs ESM

The DevAPI JavaScript SDK supports both CommonJS and ESM (ES Modules) syntax. When using CommonJS, you'll need to require the module as follows:
```javascript
const { SDK } = require('@devapi/sdk');
```
When using ESM, you can import the module directly:
```javascript
import { SDK } from '@devapi/sdk';
```
Both approaches will give you access to the same API functionality.

## Asynchronous Requests with Async/Await

To make asynchronous requests to the DevAPI servers, use the `SDK` instance and its `get`, `post`, `put`, and `delete` methods. These methods return promises that resolve to JSON objects or throw errors. Here's an example:
```javascript
const sdk = new SDK({
  token: 'your_api_token',
  timeout: 10000,
});

sdk.get('users')
  .then((response) => {
    const users = response.data;
    console.log(users);
  })
  .catch((error) => {
    if (error.code === 'E001') {
      console.error('Invalid API token');
    } else {
      console.error(error.message);
    }
  });
```
Note that the `timeout` property is set to 10 seconds by default, but you can adjust this value as needed.

## Error Handling

The DevAPI JavaScript SDK uses a standardized error code system. The most common error codes are:

* `E001`: Invalid API token
* `E002`: Unauthorized access
* `E003`: Request timeout exceeded (if the `timeout` property is set too low)
* `E004`: Server-side error

When an error occurs, the SDK throws a custom error object with one of these codes. You can handle errors in your code using try-catch blocks or by listening for the `error` event on the SDK instance.

For example:
```javascript
const sdk = new SDK({
  token: 'your_api_token',
});

sdk.on('error', (error) => {
  if (error.code === 'E001') {
    console.error('Invalid API token');
  } else {
    console.error(error.message);
  }
});
```
This way, you can catch and handle errors in a centralized manner.
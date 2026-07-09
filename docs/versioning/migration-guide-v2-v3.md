---
source_name: migration-guide-v2-v3
section: Versioning
last_updated: "2024-03-01"
doc_type: guide
access_level: public
---

## Migration Guide from API v2 to v3: Breaking Changes

The DevAPI team is excited to announce the release of our new API version, v3. This migration guide will help you transition your applications from API v2 to v3, highlighting breaking changes, new endpoints, deprecated fields, and code examples for each change.

### Changes to Authentication and Authorization

In API v3, we have replaced the old token-based authentication with a more secure JSON Web Token (JWT) system. New users will need to register using the `/register` endpoint and obtain an access token upon successful login.

```bash
curl -X POST \
  https://api.devapi.com/v3/register \
  -H 'Content-Type: application/json' \
  -d '{"username": "newuser", "password": "securepass"}'
```

Error code 401 will be returned for invalid credentials. Existing users can continue using their old tokens until they are exchanged for new ones within the next 30 days.

### Removal of `async` Endpoint

The `/async` endpoint has been deprecated in API v2 and removed entirely in API v3. All requests should now use the `/process` endpoint instead.

```bash
curl -X POST \
  https://api.devapi.com/v3/process \
  -H 'Content-Type: application/json' \
  -d '{"input": "data", "output": "result"}'
```

Error code 500 will be returned for invalid requests.

## New Endpoints

### Introduction to the `/users` Endpoint

The new `/users` endpoint provides a list of all registered users, with optional filtering and sorting capabilities.

```bash
curl -X GET \
  https://api.devapi.com/v3/users?name=John%20Doe&sort=last_name
```

This request will return a JSON array containing user data, including `id`, `username`, `email`, and `created_at` timestamp. The `/users` endpoint is optimized for performance and returns up to 100 items per page.

### Introduction to the `/projects` Endpoint

The new `/projects` endpoint provides a list of all registered projects, with optional filtering and sorting capabilities.

```bash
curl -X GET \
  https://api.devapi.com/v3/projects?name=My%20Project&sort=created_at
```

This request will return a JSON array containing project data, including `id`, `name`, `description`, and `owner`. The `/projects` endpoint is optimized for performance and returns up to 100 items per page.

## Code Examples

### Updated Authentication Flow

```javascript
const express = require('express');
const app = express();
const jwt = require('jsonwebtoken');

app.use((req, res, next) => {
  const token = req.header('Authorization').replace('Bearer ', '');
  if (!token) return res.status(401).send({ message: 'Unauthorized' });
  try {
    const decoded = jwt.verify(token, process.env.SECRET_KEY);
    req.user = decoded;
    next();
  } catch (ex) {
    console.error(ex);
    res.status(500).send({ message: 'Internal Server Error' });
  }
});

// Register new user
app.post('/register', (req, res) => {
  const { username, password } = req.body;
  // register user logic here
  return res.send({ message: 'User registered successfully' });
});

// Login existing user
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // login logic here
  const token = jwt.sign({ id: 123 }, process.env.SECRET_KEY);
  return res.send({ message: 'Login successful', token });
});
```

### Updated Code for `/process` Endpoint

```python
import requests

def fetch_data():
    response = requests.get('https://api.devapi.com/v3/process')
    data = response.json()
    # process data here
    return data['result']

# Call the endpoint
result = fetch_data()
print(result)
```

### Updated Code for `/users` Endpoint

```javascript
const axios = require('axios');

async function get_users(filter) {
  const url = 'https://api.devapi.com/v3/users';
  const params = { ...filter };
  try {
    const response = await axios.get(url, { params });
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error('Failed to fetch users');
  }
}

// Get all users
get_users({}).then((users) => {
  // process users here
});
```
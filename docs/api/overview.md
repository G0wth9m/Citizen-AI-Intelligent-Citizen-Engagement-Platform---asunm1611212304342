# API Overview

CitizenAI provides a comprehensive REST API that allows developers to integrate citizen engagement capabilities into their applications and services.

## API Philosophy

The CitizenAI API is designed with the following principles:

!!! info "Design Principles"
    - **RESTful**: Following REST architectural principles
    - **JSON-first**: All data exchange in JSON format
    - **Versioned**: API versioning for backward compatibility
    - **Consistent**: Uniform response patterns and error handling
    - **Documented**: Comprehensive documentation and examples

## Base URL

All API endpoints are relative to the base URL:

```
https://your-domain.com/api/v1
```

For development environments:
```
http://localhost:5000/api/v1
```

## Authentication

CitizenAI uses session-based authentication for web applications and API key authentication for programmatic access.

### Session Authentication

For web applications, authentication is handled through login sessions:

```python
# Login endpoint
POST /api/v1/auth/login
{
    "username": "admin",
    "password": "password"
}

# Response
{
    "success": true,
    "user": {
        "id": "admin",
        "role": "administrator"
    },
    "session_id": "abc123..."
}
```

### API Key Authentication

For programmatic access, include your API key in the Authorization header:

```http
Authorization: Bearer YOUR_API_KEY
```

## Request/Response Format

### Standard Request Format

All POST and PUT requests should include:

```http
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

```json
{
    "data": {
        // Request payload
    },
    "metadata": {
        "timestamp": "2025-01-01T00:00:00Z",
        "request_id": "req_12345"
    }
}
```

### Standard Response Format

All API responses follow this format:

```json
{
    "success": true,
    "data": {
        // Response payload
    },
    "metadata": {
        "timestamp": "2025-01-01T00:00:00Z",
        "request_id": "req_12345",
        "version": "v1"
    },
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "pages": 5
    }
}
```

## Error Handling

### Error Response Format

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid request parameters",
        "details": {
            "field": "email",
            "message": "Invalid email format"
        }
    },
    "metadata": {
        "timestamp": "2025-01-01T00:00:00Z",
        "request_id": "req_12345"
    }
}
```

### HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid request parameters |
| `401` | Unauthorized | Authentication required |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `422` | Unprocessable Entity | Validation errors |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server error |

### Common Error Codes

| Error Code | Description |
|------------|-------------|
| `AUTHENTICATION_REQUIRED` | API key or session required |
| `INVALID_API_KEY` | API key is invalid or expired |
| `VALIDATION_ERROR` | Request validation failed |
| `RESOURCE_NOT_FOUND` | Requested resource does not exist |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `INTERNAL_ERROR` | Server-side error |

## Rate Limiting

API requests are rate-limited to ensure fair usage:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```

**Default Limits:**
- **Authenticated requests**: 1000 requests per hour
- **Unauthenticated requests**: 100 requests per hour
- **Chat API**: 500 requests per hour
- **Analytics API**: 200 requests per hour

## API Endpoints Overview

### Core Endpoints

| Endpoint | Description |
|----------|-------------|
| `/auth/*` | Authentication and session management |
| `/chat/*` | AI chat interactions |
| `/analytics/*` | Analytics and reporting |
| `/concerns/*` | Concern management |
| `/users/*` | User management |

### Chat API

```http
POST /api/v1/chat/message
GET  /api/v1/chat/history
POST /api/v1/chat/session
```

### Analytics API

```http
GET  /api/v1/analytics/dashboard
GET  /api/v1/analytics/metrics
GET  /api/v1/analytics/export
POST /api/v1/analytics/query
```

### Concerns API

```http
GET    /api/v1/concerns
POST   /api/v1/concerns
GET    /api/v1/concerns/{id}
PUT    /api/v1/concerns/{id}
DELETE /api/v1/concerns/{id}
```

## API Examples

### Chat Interaction

```python
import requests

# Send a chat message
response = requests.post(
    'http://localhost:5000/api/v1/chat/message',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'message': 'What services are available for new residents?',
        'session_id': 'session_123'
    }
)

# Response
{
    "success": true,
    "data": {
        "response": "New residents can access the following services...",
        "confidence": 0.95,
        "intent": "services_inquiry",
        "session_id": "session_123"
    }
}
```

### Analytics Query

```python
# Get dashboard metrics
response = requests.get(
    'http://localhost:5000/api/v1/analytics/dashboard',
    headers={'Authorization': 'Bearer YOUR_API_KEY'},
    params={
        'date_range': '7d',
        'metrics': 'conversations,sentiment,concerns'
    }
)

# Response
{
    "success": true,
    "data": {
        "conversations": {
            "total": 1250,
            "trend": "+15%"
        },
        "sentiment": {
            "positive": 78,
            "neutral": 15,
            "negative": 7
        },
        "concerns": {
            "total": 45,
            "resolved": 38,
            "pending": 7
        }
    }
}
```

### Concern Management

```python
# Create a new concern
response = requests.post(
    'http://localhost:5000/api/v1/concerns',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'title': 'Broken street light',
        'description': 'Street light on Main St is not working',
        'category': 'infrastructure',
        'priority': 'medium',
        'location': '123 Main Street'
    }
)

# Response
{
    "success": true,
    "data": {
        "id": "concern_12345",
        "title": "Broken street light",
        "status": "submitted",
        "created_at": "2025-01-01T10:00:00Z",
        "tracking_number": "TRK-2025-001"
    }
}
```

## Webhooks

CitizenAI supports webhooks for real-time notifications:

### Webhook Events

| Event | Description |
|-------|-------------|
| `concern.created` | New concern submitted |
| `concern.updated` | Concern status changed |
| `chat.escalated` | Chat escalated to human agent |
| `analytics.threshold` | Metric threshold exceeded |

### Webhook Configuration

```python
# Configure webhook endpoint
POST /api/v1/webhooks
{
    "url": "https://your-app.com/webhooks/citizenai",
    "events": ["concern.created", "concern.updated"],
    "secret": "webhook_secret_key"
}
```

### Webhook Payload

```json
{
    "event": "concern.created",
    "data": {
        "concern_id": "concern_12345",
        "title": "Broken street light",
        "status": "submitted"
    },
    "timestamp": "2025-01-01T10:00:00Z",
    "signature": "sha256=..."
}
```

## SDKs and Libraries

### Python SDK

```python
from citizenai import CitizenAI

# Initialize client
client = CitizenAI(api_key='YOUR_API_KEY')

# Send chat message
response = client.chat.send_message(
    message="What are your office hours?",
    session_id="session_123"
)

# Get analytics
metrics = client.analytics.get_dashboard_metrics(
    date_range='7d'
)

# Create concern
concern = client.concerns.create(
    title="Pothole on Oak Street",
    category="infrastructure"
)
```

### JavaScript SDK

```javascript
import { CitizenAI } from '@citizenai/sdk';

const client = new CitizenAI({
    apiKey: 'YOUR_API_KEY',
    baseUrl: 'http://localhost:5000/api/v1'
});

// Send chat message
const response = await client.chat.sendMessage({
    message: 'How do I apply for a permit?',
    sessionId: 'session_123'
});

// Get analytics
const metrics = await client.analytics.getDashboardMetrics({
    dateRange: '7d'
});
```

## Testing the API

### Using curl

```bash
# Test authentication
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Send chat message
curl -X POST http://localhost:5000/api/v1/chat/message \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test_session"}'
```

### Using Postman

1. Import the CitizenAI Postman collection
2. Set environment variables:
   - `base_url`: `http://localhost:5000/api/v1`
   - `api_key`: Your API key
3. Run the authentication request
4. Test other endpoints

## API Versioning

CitizenAI uses URL-based versioning:

- **Current version**: `v1`
- **Version format**: `/api/v{version}/`
- **Deprecation policy**: 12 months notice before deprecation

### Version History

| Version | Release Date | Status | Notes |
|---------|--------------|--------|-------|
| `v1` | 2025-01-01 | Current | Initial API release |

## Best Practices

### Performance Optimization

!!! tip "API Best Practices"
    - **Pagination**: Use pagination for large datasets
    - **Caching**: Implement client-side caching for static data
    - **Compression**: Enable gzip compression
    - **Connection pooling**: Reuse HTTP connections
    - **Batch requests**: Group multiple requests when possible

### Error Handling

```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.post(
        'http://localhost:5000/api/v1/chat/message',
        json={'message': 'Hello'},
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    
    if not data.get('success'):
        # Handle API error
        error = data.get('error', {})
        print(f"API Error: {error.get('message')}")
    
except RequestException as e:
    # Handle network/HTTP errors
    print(f"Request failed: {e}")
```

### Security Considerations

- **Always use HTTPS** in production
- **Store API keys securely** (environment variables, key management systems)
- **Implement request signing** for sensitive operations
- **Validate all inputs** before sending to API
- **Monitor API usage** for unusual patterns

## Next Steps

- **[Authentication](authentication.md)** - Detailed authentication guide
- **[Endpoints](endpoints.md)** - Complete endpoint documentation
- **Development Guide** - API integration examples and tutorials

For specific endpoint documentation, see the detailed [Endpoints](endpoints.md) reference.

# API Endpoints

Complete reference for all CitizenAI API endpoints, including request/response formats, parameters, and examples.

## Base URL

All endpoints are relative to the base API URL:

```
Production: https://your-domain.com/api/v1
Development: http://localhost:5000/api/v1
```

## Authentication Endpoints

### Login

Authenticate a user and create a session.

```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
    "username": "string (required)",
    "password": "string (required)",
    "remember_me": "boolean (optional, default: false)"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "user": {
            "id": "string",
            "username": "string",
            "role": "string",
            "permissions": ["string"]
        },
        "session": {
            "id": "string",
            "expires_at": "string (ISO 8601)"
        }
    }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password"
  }'
```

### Logout

End the current user session.

```http
POST /api/v1/auth/logout
```

**Headers:** `Authorization: Bearer session-token`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Logged out successfully"
}
```

### Validate Session

Check if current session is valid.

```http
GET /api/v1/auth/validate
```

**Headers:** `Authorization: Bearer session-token`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "valid": true,
        "user": {
            "id": "string",
            "username": "string",
            "role": "string"
        },
        "expires_at": "string (ISO 8601)"
    }
}
```

## Chat Endpoints

### Send Message

Send a message to the AI chat assistant.

```http
POST /api/v1/chat/message
```

**Headers:** `Authorization: Bearer api-key`

**Request Body:**
```json
{
    "message": "string (required, max: 500)",
    "session_id": "string (optional)",
    "context": "object (optional)"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "response": "string",
        "confidence": "number (0-1)",
        "intent": "string",
        "sentiment": "string (positive|neutral|negative)",
        "session_id": "string",
        "conversation_id": "string"
    }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/v1/chat/message \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your office hours?",
    "session_id": "session_123"
  }'
```

### Get Chat History

Retrieve conversation history for a session.

```http
GET /api/v1/chat/history
```

**Headers:** `Authorization: Bearer api-key`

**Query Parameters:**
- `session_id` (string, required): Session identifier
- `limit` (integer, optional, default: 50): Number of messages to return
- `offset` (integer, optional, default: 0): Pagination offset

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "messages": [
            {
                "id": "string",
                "message": "string",
                "response": "string",
                "timestamp": "string (ISO 8601)",
                "intent": "string",
                "sentiment": "string"
            }
        ],
        "session_info": {
            "session_id": "string",
            "started_at": "string (ISO 8601)",
            "message_count": "integer"
        }
    },
    "pagination": {
        "page": 1,
        "per_page": 50,
        "total": 100,
        "pages": 2
    }
}
```

### Create Chat Session

Start a new chat session.

```http
POST /api/v1/chat/session
```

**Headers:** `Authorization: Bearer api-key`

**Request Body:**
```json
{
    "user_id": "string (optional)",
    "context": "object (optional)"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "session_id": "string",
        "created_at": "string (ISO 8601)",
        "expires_at": "string (ISO 8601)"
    }
}
```

## Analytics Endpoints

### Get Dashboard Data

Retrieve main dashboard metrics and charts.

```http
GET /api/v1/analytics/dashboard
```

**Headers:** `Authorization: Bearer api-key`

**Query Parameters:**
- `date_range` (string, optional, default: "7d"): Time range (1d, 7d, 30d, 90d, custom)
- `start_date` (string, optional): Start date for custom range (YYYY-MM-DD)
- `end_date` (string, optional): End date for custom range (YYYY-MM-DD)
- `metrics` (string, optional): Comma-separated list of metrics

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "summary": {
            "total_conversations": 1250,
            "avg_response_time": 1.4,
            "satisfaction_score": 4.2,
            "resolution_rate": 87
        },
        "conversations": {
            "daily_counts": [45, 67, 89, 123, 98, 34, 28],
            "trend": "+15%"
        },
        "sentiment": {
            "positive": 65,
            "neutral": 25,
            "negative": 10
        },
        "concerns": {
            "total": 45,
            "resolved": 38,
            "pending": 7
        }
    }
}
```

### Get Specific Metrics

Retrieve detailed metrics for specific data points.

```http
GET /api/v1/analytics/metrics/{metric_type}
```

**Headers:** `Authorization: Bearer api-key`

**Path Parameters:**
- `metric_type` (string): Type of metric (conversations, sentiment, concerns, performance)

**Query Parameters:**
- `granularity` (string, optional, default: "daily"): Data granularity (hourly, daily, weekly, monthly)
- `start_date` (string, required): Start date (YYYY-MM-DD)
- `end_date` (string, required): End date (YYYY-MM-DD)
- `filters` (string, optional): JSON-encoded filter object

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "metric_type": "conversations",
        "granularity": "daily",
        "data_points": [
            {
                "date": "2025-01-01",
                "value": 45,
                "metadata": {
                    "avg_duration": 300,
                    "unique_users": 32
                }
            }
        ],
        "aggregates": {
            "total": 1250,
            "average": 45.5,
            "peak": 123,
            "trend": "+15%"
        }
    }
}
```

### Export Analytics Data

Export analytics data in various formats.

```http
GET /api/v1/analytics/export
```

**Headers:** `Authorization: Bearer api-key`

**Query Parameters:**
- `format` (string, required): Export format (csv, json, pdf, xlsx)
- `date_range` (string, optional, default: "30d"): Time range
- `metrics` (string, optional): Comma-separated metrics to include
- `include_details` (boolean, optional, default: false): Include detailed breakdowns

**Response (200 OK):**
Returns file download based on format requested.

## Concerns Endpoints

### List Concerns

Retrieve a list of concerns with filtering and pagination.

```http
GET /api/v1/concerns
```

**Headers:** `Authorization: Bearer api-key`

**Query Parameters:**
- `status` (string, optional): Filter by status (submitted, in_progress, resolved, closed)
- `category` (string, optional): Filter by category
- `priority` (string, optional): Filter by priority (low, medium, high, emergency)
- `limit` (integer, optional, default: 20): Number of results per page
- `offset` (integer, optional, default: 0): Pagination offset
- `sort` (string, optional, default: "created_at"): Sort field
- `order` (string, optional, default: "desc"): Sort order (asc, desc)

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "concerns": [
            {
                "id": "string",
                "tracking_number": "string",
                "title": "string",
                "description": "string",
                "category": "string",
                "priority": "string",
                "status": "string",
                "location": "string",
                "submitted_at": "string (ISO 8601)",
                "last_updated": "string (ISO 8601)",
                "estimated_resolution": "string (ISO 8601)"
            }
        ]
    },
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "pages": 5
    }
}
```

### Create Concern

Submit a new concern.

```http
POST /api/v1/concerns
```

**Headers:** `Authorization: Bearer api-key`

**Request Body:**
```json
{
    "title": "string (required, max: 100)",
    "description": "string (required, max: 2000)",
    "category": "string (required)",
    "priority": "string (optional, default: medium)",
    "location": "string (optional)",
    "contact": {
        "email": "string (optional)",
        "phone": "string (optional)",
        "name": "string (optional)"
    },
    "anonymous": "boolean (optional, default: false)",
    "attachments": ["string (optional)"]
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": "string",
        "tracking_number": "string",
        "title": "string",
        "status": "submitted",
        "priority": "string",
        "estimated_resolution": "string (ISO 8601)",
        "created_at": "string (ISO 8601)"
    }
}
```

### Get Concern Details

Retrieve detailed information about a specific concern.

```http
GET /api/v1/concerns/{concern_id}
```

**Headers:** `Authorization: Bearer api-key`

**Path Parameters:**
- `concern_id` (string): Concern ID or tracking number

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": "string",
        "tracking_number": "string",
        "title": "string",
        "description": "string",
        "category": "string",
        "priority": "string",
        "status": "string",
        "location": "string",
        "contact": "object",
        "submitted_at": "string (ISO 8601)",
        "last_updated": "string (ISO 8601)",
        "estimated_resolution": "string (ISO 8601)",
        "updates": [
            {
                "id": "string",
                "timestamp": "string (ISO 8601)",
                "status": "string",
                "message": "string",
                "updated_by": "string"
            }
        ],
        "attachments": [
            {
                "id": "string",
                "filename": "string",
                "url": "string",
                "size": "integer",
                "uploaded_at": "string (ISO 8601)"
            }
        ]
    }
}
```

### Update Concern

Update concern status and add comments (admin only).

```http
PUT /api/v1/concerns/{concern_id}
```

**Headers:** `Authorization: Bearer api-key`

**Path Parameters:**
- `concern_id` (string): Concern ID

**Request Body:**
```json
{
    "status": "string (optional)",
    "priority": "string (optional)",
    "message": "string (optional)",
    "estimated_resolution": "string (optional, ISO 8601)",
    "assigned_to": "string (optional)",
    "internal_notes": "string (optional)"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": "string",
        "status": "string",
        "last_updated": "string (ISO 8601)",
        "message": "Concern updated successfully"
    }
}
```

### Delete Concern

Delete a concern (admin only).

```http
DELETE /api/v1/concerns/{concern_id}
```

**Headers:** `Authorization: Bearer api-key`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Concern deleted successfully"
}
```

## Users Endpoints

### List Users

Retrieve list of users (admin only).

```http
GET /api/v1/users
```

**Headers:** `Authorization: Bearer api-key`

**Query Parameters:**
- `role` (string, optional): Filter by role
- `active` (boolean, optional): Filter by active status
- `limit` (integer, optional, default: 50): Results per page
- `offset` (integer, optional, default: 0): Pagination offset

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "users": [
            {
                "id": "string",
                "username": "string",
                "email": "string",
                "role": "string",
                "active": "boolean",
                "created_at": "string (ISO 8601)",
                "last_login": "string (ISO 8601)"
            }
        ]
    },
    "pagination": {
        "page": 1,
        "per_page": 50,
        "total": 25,
        "pages": 1
    }
}
```

### Create User

Create a new user account (admin only).

```http
POST /api/v1/users
```

**Headers:** `Authorization: Bearer api-key`

**Request Body:**
```json
{
    "username": "string (required)",
    "email": "string (required)",
    "password": "string (required)",
    "role": "string (required)",
    "active": "boolean (optional, default: true)"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": "string",
        "username": "string",
        "email": "string",
        "role": "string",
        "active": "boolean",
        "created_at": "string (ISO 8601)"
    }
}
```

### Get User Details

Get detailed user information.

```http
GET /api/v1/users/{user_id}
```

**Headers:** `Authorization: Bearer api-key`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": "string",
        "username": "string",
        "email": "string",
        "role": "string",
        "active": "boolean",
        "permissions": ["string"],
        "created_at": "string (ISO 8601)",
        "last_login": "string (ISO 8601)",
        "profile": {
            "first_name": "string",
            "last_name": "string",
            "department": "string"
        }
    }
}
```

### Update User

Update user information.

```http
PUT /api/v1/users/{user_id}
```

**Headers:** `Authorization: Bearer api-key`

**Request Body:**
```json
{
    "email": "string (optional)",
    "role": "string (optional)",
    "active": "boolean (optional)",
    "profile": "object (optional)"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": "string",
        "message": "User updated successfully"
    }
}
```

### Delete User

Delete a user account (admin only).

```http
DELETE /api/v1/users/{user_id}
```

**Headers:** `Authorization: Bearer api-key`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "User deleted successfully"
}
```

## System Endpoints

### Health Check

Check system health and status.

```http
GET /api/v1/system/health
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "status": "healthy",
        "timestamp": "string (ISO 8601)",
        "version": "string",
        "uptime": "integer (seconds)",
        "components": {
            "database": "healthy",
            "watson_api": "healthy",
            "file_storage": "healthy"
        },
        "metrics": {
            "memory_usage": "512MB",
            "cpu_usage": "15%",
            "disk_usage": "45%"
        }
    }
}
```

### System Information

Get system configuration and information (admin only).

```http
GET /api/v1/system/info
```

**Headers:** `Authorization: Bearer api-key`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "version": "string",
        "build": "string",
        "environment": "string",
        "features": ["string"],
        "limits": {
            "max_file_size": "10MB",
            "rate_limit": "1000/hour",
            "session_timeout": "30 minutes"
        }
    }
}
```

## WebSocket Endpoints

### Real-time Chat

Establish WebSocket connection for real-time chat.

```javascript
// WebSocket connection
const ws = new WebSocket('ws://localhost:5000/api/v1/ws/chat');

// Send message
ws.send(JSON.stringify({
    type: 'message',
    session_id: 'session_123',
    message: 'Hello'
}));

// Receive response
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('AI Response:', data.response);
};
```

### Real-time Notifications

Subscribe to system notifications.

```javascript
// WebSocket connection for notifications
const ws = new WebSocket('ws://localhost:5000/api/v1/ws/notifications');

// Authentication
ws.send(JSON.stringify({
    type: 'auth',
    token: 'your-api-key'
}));

// Receive notifications
ws.onmessage = function(event) {
    const notification = JSON.parse(event.data);
    console.log('Notification:', notification);
};
```

## Error Responses

All endpoints may return error responses in this format:

```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": "object (optional additional details)"
    },
    "metadata": {
        "timestamp": "string (ISO 8601)",
        "request_id": "string"
    }
}
```

### Common HTTP Status Codes

| Status | Description | When Used |
|--------|-------------|-----------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## SDKs and Code Examples

### Python SDK

```python
from citizenai import CitizenAI

# Initialize client
client = CitizenAI(
    api_key='your-api-key',
    base_url='http://localhost:5000/api/v1'
)

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
    title="Broken street light",
    description="Street light on Main St is not working",
    category="infrastructure"
)
```

### JavaScript SDK

```javascript
import { CitizenAI } from '@citizenai/sdk';

const client = new CitizenAI({
    apiKey: 'your-api-key',
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

// Create concern
const concern = await client.concerns.create({
    title: 'Pothole on Oak Street',
    category: 'infrastructure'
});
```

## Testing the API

### Using curl

```bash
# Test authentication
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Test chat endpoint
curl -X POST http://localhost:5000/api/v1/chat/message \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test_session"}'

# Test analytics endpoint
curl -X GET "http://localhost:5000/api/v1/analytics/dashboard?date_range=7d" \
  -H "Authorization: Bearer your-api-key"
```

### Postman Collection

Import the CitizenAI Postman collection to test all endpoints:

1. Download collection: `CitizenAI_API.postman_collection.json`
2. Set environment variables:
   - `base_url`: `http://localhost:5000/api/v1`
   - `api_key`: Your API key
3. Run collection tests

## Next Steps

- **[Authentication](authentication.md)** - Detailed authentication guide
- **[User Guide](../user-guide/features.md)** - Learn about platform features
- **[Development Guide](../development/contributing.md)** - API integration examples

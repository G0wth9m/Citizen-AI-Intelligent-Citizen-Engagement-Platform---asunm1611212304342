# Configuration

Configure CitizenAI to meet your specific requirements and environment.

## Configuration Overview

CitizenAI uses a flexible configuration system that supports:

- Environment variables (`.env` file)
- Configuration files
- Runtime configuration
- Default fallback values

## Environment Configuration

### Creating the .env File

Create a `.env` file in the project root directory:

```bash title=".env"
# =============================================================================
# CitizenAI Configuration
# =============================================================================

# Flask Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-super-secret-key-change-this-in-production

# Server Configuration
HOST=127.0.0.1
PORT=5000

# Session Configuration
SESSION_TYPE=filesystem
SESSION_PERMANENT=False
SESSION_USE_SIGNER=True
PERMANENT_SESSION_LIFETIME=1800

# IBM Watson AI Configuration
WATSON_API_KEY=your-watson-api-key-here
WATSON_URL=your-watson-service-url
WATSON_VERSION=2021-06-14
WATSON_ASSISTANT_ID=your-assistant-id

# IBM Cloud Configuration
IBM_CLOUD_API_KEY=your-ibm-cloud-api-key
IBM_CLOUD_URL=https://api.us-south.assistant.watson.cloud.ibm.com

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/citizenai.log

# Analytics Configuration
ANALYTICS_ENABLED=True
ANALYTICS_RETENTION_DAYS=90

# Security Configuration
CSRF_ENABLED=True
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

### Configuration Sections

#### Flask Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Application environment | `development` | No |
| `FLASK_DEBUG` | Enable debug mode | `True` | No |
| `SECRET_KEY` | Session encryption key | Generated | **Yes** |
| `HOST` | Server host address | `127.0.0.1` | No |
| `PORT` | Server port number | `5000` | No |

!!! warning "Production Security"
    Always set a secure `SECRET_KEY` in production environments. Never use default or weak keys.

#### IBM Watson Configuration

| Variable | Description | Required for AI |
|----------|-------------|-----------------|
| `WATSON_API_KEY` | IBM Watson API key | **Yes** |
| `WATSON_URL` | Watson service URL | **Yes** |
| `WATSON_VERSION` | API version date | **Yes** |
| `WATSON_ASSISTANT_ID` | Assistant instance ID | **Yes** |

#### Session Management

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION_TYPE` | Session storage type | `filesystem` |
| `SESSION_PERMANENT` | Permanent sessions | `False` |
| `PERMANENT_SESSION_LIFETIME` | Session timeout (seconds) | `1800` |

## IBM Watson Setup

### Getting Watson Credentials

1. **Create IBM Cloud Account**
   - Visit [IBM Cloud](https://cloud.ibm.com/)
   - Sign up for a free account

2. **Create Watson Assistant Service**
   ```bash
   # Using IBM Cloud CLI
   ibmcloud login
   ibmcloud resource service-instance-create watson-assistant conversation lite us-south
   ```

3. **Get Service Credentials**
   - Navigate to Watson Assistant in IBM Cloud
   - Go to "Service credentials"
   - Create new credentials
   - Copy API key and URL

### Watson Assistant Configuration

```json title="Watson Assistant Skills"
{
  "name": "CitizenAI Assistant",
  "description": "AI assistant for citizen engagement",
  "language": "en",
  "workspace": {
    "intents": [
      {
        "intent": "greetings",
        "examples": ["hello", "hi", "good morning"]
      },
      {
        "intent": "services_inquiry",
        "examples": ["what services are available", "city services"]
      }
    ]
  }
}
```

## Application Configuration

### Config Classes

```python title="config.py"
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Watson configuration
    WATSON_API_KEY = os.environ.get('WATSON_API_KEY')
    WATSON_URL = os.environ.get('WATSON_URL')
    WATSON_VERSION = os.environ.get('WATSON_VERSION', '2021-06-14')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
```

## Database Configuration

### File-based Storage

For development and small deployments:

```python title="Storage Configuration"
import os

# Data directories
DATA_DIR = os.path.join(os.getcwd(), 'data')
SESSIONS_DIR = os.path.join(DATA_DIR, 'sessions')
ANALYTICS_DIR = os.path.join(DATA_DIR, 'analytics')
CONCERNS_DIR = os.path.join(DATA_DIR, 'concerns')

# Ensure directories exist
for directory in [DATA_DIR, SESSIONS_DIR, ANALYTICS_DIR, CONCERNS_DIR]:
    os.makedirs(directory, exist_ok=True)
```

### External Database (Optional)

For production deployments:

```bash title=".env additions"
# Database Configuration (Optional)
DATABASE_URL=postgresql://user:password@localhost:5432/citizenai
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30
```

## Logging Configuration

### Basic Logging Setup

```python title="logging_config.py"
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """Configure application logging"""
    
    if not app.debug:
        # Create logs directory
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configure file handler
        file_handler = RotatingFileHandler(
            'logs/citizenai.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('CitizenAI startup')
```

## Performance Configuration

### Caching

```python title="Cache Configuration"
# Redis cache (for production)
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6379/0'
CACHE_DEFAULT_TIMEOUT = 300

# Simple cache (for development)
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300
```

### Rate Limiting

```python title="Rate Limiting"
# API rate limiting
RATELIMIT_STORAGE_URL = 'redis://localhost:6379/1'
RATELIMIT_DEFAULT = '100 per hour'
RATELIMIT_HEADERS_ENABLED = True
```

## Security Configuration

### Authentication Settings

```bash title="Security Environment Variables"
# Authentication
AUTH_TIMEOUT=1800
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900

# CORS settings
CORS_ORIGINS=*
CORS_METHODS=GET,POST,PUT,DELETE
CORS_HEADERS=Content-Type,Authorization

# Content Security Policy
CSP_DEFAULT_SRC='self'
CSP_SCRIPT_SRC='self' 'unsafe-inline'
CSP_STYLE_SRC='self' 'unsafe-inline'
```

## Deployment Configurations

### Development

```bash title="Development .env"
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
ANALYTICS_ENABLED=False
```

### Production

```bash title="Production .env"
FLASK_ENV=production
FLASK_DEBUG=False
LOG_LEVEL=WARNING
SESSION_COOKIE_SECURE=True
ANALYTICS_ENABLED=True
```

### Docker Configuration

```dockerfile title="Dockerfile environment"
# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PORT=8080

# Copy configuration
COPY .env.production .env
```

## Validation and Testing

### Configuration Validation

```python title="config_validator.py"
def validate_config():
    """Validate required configuration"""
    required_vars = [
        'SECRET_KEY',
        'WATSON_API_KEY',
        'WATSON_URL'
    ]
    
    missing = []
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)
    
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")

# Usage in app initialization
validate_config()
```

### Testing Configuration

```bash title="Test Environment"
# Create test configuration
cp .env.example .env.test

# Set test-specific values
echo "FLASK_ENV=testing" >> .env.test
echo "WATSON_API_KEY=test-key" >> .env.test
```

## Troubleshooting

### Common Configuration Issues

??? question "Watson API connection fails"
    Check your Watson credentials:
    ```bash
    # Test Watson connection
    curl -u "apikey:$WATSON_API_KEY" "$WATSON_URL/v2/assistants?version=2021-06-14"
    ```

??? question "Session data not persisting"
    Verify session configuration:
    ```python
    # Check session directory permissions
    import os
    print(os.access('flask_session', os.W_OK))
    ```

??? question "Environment variables not loading"
    Ensure `.env` file is in the project root:
    ```bash
    # Check .env file location
    ls -la .env
    
    # Verify python-dotenv is installed
    pip show python-dotenv
    ```

## Next Steps

After configuring CitizenAI:

1. **Test Configuration**: Run the application and verify all features work
2. **Security Review**: Ensure production security settings are applied
3. **Performance Tuning**: Optimize for your expected load
4. **Monitoring Setup**: Configure logging and monitoring

For advanced configuration options, see the [Development Guide](../development/architecture.md).

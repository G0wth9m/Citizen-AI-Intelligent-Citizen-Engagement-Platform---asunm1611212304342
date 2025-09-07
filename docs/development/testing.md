# Testing

Comprehensive testing guide for CitizenAI, covering unit tests, integration tests, and quality assurance practices.

## Testing Philosophy

CitizenAI follows a comprehensive testing approach:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Validate system performance
- **Security Tests**: Ensure security requirements

## Test Structure

### Directory Organization

```
tests/
├── unit/                   # Unit tests
│   ├── test_auth.py       # Authentication tests
│   ├── test_chat.py       # Chat engine tests
│   ├── test_analytics.py  # Analytics tests
│   └── test_concerns.py   # Concern management tests
├── integration/           # Integration tests
│   ├── test_api.py       # API endpoint tests
│   ├── test_watson.py    # Watson integration tests
│   └── test_workflows.py # End-to-end workflows
├── fixtures/              # Test data and fixtures
│   ├── sample_data.json  # Sample analytics data
│   ├── test_users.json   # Test user accounts
│   └── mock_responses.py # Mock API responses
├── performance/           # Performance tests
│   ├── test_load.py      # Load testing
│   └── test_stress.py    # Stress testing
└── conftest.py           # Pytest configuration
```

## Unit Testing

### Test Configuration

```python
# conftest.py
import pytest
import tempfile
import os
from src.core.app import create_app
from src.auth.models import User

@pytest.fixture
def app():
    """Create application for testing."""
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test-secret-key',
        'WATSON_API_KEY': 'test-watson-key'
    })
    
    with app.app_context():
        # Initialize test database
        init_test_db()
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """Create authenticated test client."""
    client.post('/api/v1/auth/login', json={
        'username': 'test_user',
        'password': 'test_password'
    })
    return client
```

### Authentication Tests

```python
# tests/unit/test_auth.py
import pytest
from src.auth.models import User
from src.auth.utils import hash_password, verify_password

class TestAuthentication:
    """Test authentication functionality."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "secure_password_123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert verify_password(hashed, password)
        assert not verify_password(hashed, "wrong_password")
    
    def test_login_success(self, client):
        """Test successful login."""
        response = client.post('/api/v1/auth/login', json={
            'username': 'admin',
            'password': 'password'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'user' in data['data']
        assert 'session' in data['data']
    
    def test_login_failure(self, client):
        """Test login with invalid credentials."""
        response = client.post('/api/v1/auth/login', json={
            'username': 'admin',
            'password': 'wrong_password'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert data['error']['code'] == 'AUTHENTICATION_FAILED'
    
    def test_logout(self, auth_client):
        """Test user logout."""
        response = auth_client.post('/api/v1/auth/logout')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    @pytest.mark.parametrize("username,password,expected", [
        ("", "password", False),
        ("admin", "", False),
        ("admin", "short", False),
        ("admin", "valid_password_123", True),
    ])
    def test_credential_validation(self, username, password, expected):
        """Test credential validation with various inputs."""
        from src.auth.utils import validate_credentials
        
        result = validate_credentials(username, password)
        assert result == expected
```

### Chat Engine Tests

```python
# tests/unit/test_chat.py
import pytest
from unittest.mock import Mock, patch
from src.chat.engine import ChatEngine

class TestChatEngine:
    """Test chat engine functionality."""
    
    @pytest.fixture
    def chat_engine(self):
        """Create ChatEngine instance for testing."""
        config = {
            'watson_api_key': 'test-key',
            'watson_url': 'test-url',
            'mode': 'demo'
        }
        return ChatEngine(config)
    
    def test_process_message_demo_mode(self, chat_engine):
        """Test message processing in demo mode."""
        result = chat_engine.process_message("Hello")
        
        assert result['success'] is True
        assert 'response' in result
        assert 'confidence' in result
        assert result['mode'] == 'demo'
    
    @patch('src.chat.watson.WatsonAssistant')
    def test_process_message_ai_mode(self, mock_watson, chat_engine):
        """Test message processing in AI mode."""
        # Configure mock
        mock_watson.return_value.message.return_value = {
            'output': {'generic': [{'text': 'AI response'}]},
            'context': {'confidence': 0.95}
        }
        
        chat_engine.mode = 'ai'
        result = chat_engine.process_message("What are your hours?")
        
        assert result['success'] is True
        assert result['response'] == 'AI response'
        assert result['confidence'] == 0.95
    
    def test_sentiment_analysis(self, chat_engine):
        """Test sentiment analysis functionality."""
        positive_text = "I love this service! It's amazing!"
        negative_text = "This is terrible and frustrating!"
        neutral_text = "What are your office hours?"
        
        pos_sentiment = chat_engine.analyze_sentiment(positive_text)
        neg_sentiment = chat_engine.analyze_sentiment(negative_text)
        neu_sentiment = chat_engine.analyze_sentiment(neutral_text)
        
        assert pos_sentiment['sentiment'] == 'positive'
        assert neg_sentiment['sentiment'] == 'negative'
        assert neu_sentiment['sentiment'] == 'neutral'
    
    def test_message_validation(self, chat_engine):
        """Test message validation."""
        # Valid messages
        assert chat_engine.validate_message("Hello") is True
        assert chat_engine.validate_message("What are your hours?") is True
        
        # Invalid messages
        assert chat_engine.validate_message("") is False
        assert chat_engine.validate_message(None) is False
        assert chat_engine.validate_message("x" * 1000) is False  # Too long
```

### Analytics Tests

```python
# tests/unit/test_analytics.py
import pytest
from datetime import datetime, timedelta
from src.analytics.processor import AnalyticsProcessor

class TestAnalytics:
    """Test analytics functionality."""
    
    @pytest.fixture
    def analytics_processor(self):
        """Create AnalyticsProcessor for testing."""
        return AnalyticsProcessor()
    
    @pytest.fixture
    def sample_data(self):
        """Sample analytics data."""
        return [
            {
                'timestamp': datetime.now() - timedelta(hours=1),
                'type': 'conversation',
                'data': {'duration': 300, 'sentiment': 'positive'}
            },
            {
                'timestamp': datetime.now() - timedelta(hours=2),
                'type': 'conversation', 
                'data': {'duration': 450, 'sentiment': 'neutral'}
            }
        ]
    
    def test_process_conversation_data(self, analytics_processor, sample_data):
        """Test conversation data processing."""
        result = analytics_processor.process_conversations(sample_data)
        
        assert 'total_conversations' in result
        assert 'average_duration' in result
        assert 'sentiment_distribution' in result
        assert result['total_conversations'] == 2
        assert result['average_duration'] == 375  # (300 + 450) / 2
    
    def test_sentiment_aggregation(self, analytics_processor):
        """Test sentiment data aggregation."""
        sentiment_data = [
            {'sentiment': 'positive', 'count': 10},
            {'sentiment': 'neutral', 'count': 5},
            {'sentiment': 'negative', 'count': 2}
        ]
        
        result = analytics_processor.aggregate_sentiment(sentiment_data)
        
        assert result['positive'] == 59  # 10/17 * 100
        assert result['neutral'] == 29   # 5/17 * 100  
        assert result['negative'] == 12  # 2/17 * 100
    
    def test_date_range_filtering(self, analytics_processor, sample_data):
        """Test date range filtering."""
        start_date = datetime.now() - timedelta(hours=1, minutes=30)
        end_date = datetime.now()
        
        filtered = analytics_processor.filter_by_date_range(
            sample_data, start_date, end_date
        )
        
        assert len(filtered) == 1  # Only one record in range
```

## Integration Testing

### API Integration Tests

```python
# tests/integration/test_api.py
import pytest
import json

class TestAPIIntegration:
    """Test API endpoint integration."""
    
    def test_chat_api_flow(self, auth_client):
        """Test complete chat API workflow."""
        # Start chat session
        response = auth_client.post('/api/v1/chat/session')
        assert response.status_code == 201
        
        session_data = response.get_json()
        session_id = session_data['data']['session_id']
        
        # Send message
        response = auth_client.post('/api/v1/chat/message', json={
            'message': 'What are your office hours?',
            'session_id': session_id
        })
        assert response.status_code == 200
        
        chat_data = response.get_json()
        assert chat_data['success'] is True
        assert 'response' in chat_data['data']
        
        # Get chat history
        response = auth_client.get(f'/api/v1/chat/history?session_id={session_id}')
        assert response.status_code == 200
        
        history_data = response.get_json()
        assert len(history_data['data']['messages']) >= 1
    
    def test_concern_management_flow(self, auth_client):
        """Test concern creation and management."""
        # Create concern
        concern_data = {
            'title': 'Test concern',
            'description': 'This is a test concern',
            'category': 'infrastructure',
            'priority': 'medium'
        }
        
        response = auth_client.post('/api/v1/concerns', json=concern_data)
        assert response.status_code == 201
        
        created_concern = response.get_json()
        concern_id = created_concern['data']['id']
        
        # Get concern details
        response = auth_client.get(f'/api/v1/concerns/{concern_id}')
        assert response.status_code == 200
        
        concern_details = response.get_json()
        assert concern_details['data']['title'] == 'Test concern'
        
        # Update concern status
        update_data = {
            'status': 'in_progress',
            'message': 'Work has begun on this concern'
        }
        
        response = auth_client.put(f'/api/v1/concerns/{concern_id}', json=update_data)
        assert response.status_code == 200
    
    def test_analytics_api(self, auth_client):
        """Test analytics API endpoints."""
        # Get dashboard data
        response = auth_client.get('/api/v1/analytics/dashboard?date_range=7d')
        assert response.status_code == 200
        
        dashboard_data = response.get_json()
        assert 'summary' in dashboard_data['data']
        assert 'conversations' in dashboard_data['data']
        
        # Get specific metrics
        response = auth_client.get('/api/v1/analytics/metrics/conversations')
        assert response.status_code == 200
        
        metrics_data = response.get_json()
        assert 'data_points' in metrics_data['data']
```

### Watson Integration Tests

```python
# tests/integration/test_watson.py
import pytest
from unittest.mock import patch, Mock
from src.chat.watson import WatsonIntegration

class TestWatsonIntegration:
    """Test IBM Watson API integration."""
    
    @pytest.fixture
    def watson_config(self):
        """Watson configuration for testing."""
        return {
            'api_key': 'test-api-key',
            'url': 'https://api.watson.test.com',
            'version': '2021-06-14'
        }
    
    @patch('ibm_watson.AssistantV2')
    def test_watson_connection(self, mock_assistant, watson_config):
        """Test Watson API connection."""
        mock_instance = Mock()
        mock_assistant.return_value = mock_instance
        
        watson = WatsonIntegration(watson_config)
        
        # Verify assistant was initialized correctly
        mock_assistant.assert_called_once()
        assert watson.assistant == mock_instance
    
    @patch('ibm_watson.AssistantV2')
    def test_send_message(self, mock_assistant, watson_config):
        """Test sending message to Watson."""
        mock_instance = Mock()
        mock_assistant.return_value = mock_instance
        
        # Mock Watson response
        mock_instance.message.return_value.get_result.return_value = {
            'output': {
                'generic': [{'text': 'Watson response'}]
            },
            'context': {
                'global': {'system': {'turn_count': 1}}
            }
        }
        
        watson = WatsonIntegration(watson_config)
        response = watson.send_message('Hello', {})
        
        assert response['text'] == 'Watson response'
        assert 'context' in response
```

## End-to-End Testing

### User Workflow Tests

```python
# tests/integration/test_workflows.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserWorkflows:
    """Test complete user workflows."""
    
    @pytest.fixture
    def driver(self):
        """Create Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()
    
    def test_login_and_chat_workflow(self, driver):
        """Test login and chat interaction."""
        # Navigate to application
        driver.get('http://localhost:5000')
        
        # Login
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.TYPE, 'submit')
        
        username_field.send_keys('admin')
        password_field.send_keys('password')
        login_button.click()
        
        # Wait for dashboard to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dashboard'))
        )
        
        # Navigate to chat
        chat_link = driver.find_element(By.LINK_TEXT, 'Chat')
        chat_link.click()
        
        # Send message
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'message-input'))
        )
        send_button = driver.find_element(By.ID, 'send-button')
        
        message_input.send_keys('What are your office hours?')
        send_button.click()
        
        # Wait for response
        response_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ai-response'))
        )
        
        assert 'office hours' in response_element.text.lower()
    
    def test_concern_submission_workflow(self, driver):
        """Test concern submission process."""
        # Login and navigate to concerns
        self.login(driver)
        
        concerns_link = driver.find_element(By.LINK_TEXT, 'Concerns')
        concerns_link.click()
        
        # Submit new concern
        new_concern_button = driver.find_element(By.ID, 'new-concern-button')
        new_concern_button.click()
        
        # Fill form
        title_field = driver.find_element(By.NAME, 'title')
        description_field = driver.find_element(By.NAME, 'description')
        category_select = driver.find_element(By.NAME, 'category')
        submit_button = driver.find_element(By.TYPE, 'submit')
        
        title_field.send_keys('Test Concern')
        description_field.send_keys('This is a test concern description')
        category_select.send_keys('Infrastructure')
        submit_button.click()
        
        # Verify submission
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'success-message'))
        )
        
        assert 'concern submitted' in success_message.text.lower()
    
    def login(self, driver):
        """Helper method for login."""
        driver.get('http://localhost:5000')
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.TYPE, 'submit')
        
        username_field.send_keys('admin')
        password_field.send_keys('password')
        login_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dashboard'))
        )
```

## Performance Testing

### Load Testing

```python
# tests/performance/test_load.py
import pytest
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

class TestLoadPerformance:
    """Test system performance under load."""
    
    @pytest.mark.asyncio
    async def test_concurrent_chat_requests(self):
        """Test chat endpoint under concurrent load."""
        async def send_chat_request(session, message_id):
            """Send single chat request."""
            async with session.post('/api/v1/chat/message', json={
                'message': f'Test message {message_id}',
                'session_id': f'test_session_{message_id}'
            }) as response:
                return await response.json()
        
        # Create session with authentication
        async with aiohttp.ClientSession(
            'http://localhost:5000',
            headers={'Authorization': 'Bearer test-api-key'}
        ) as session:
            
            # Send 100 concurrent requests
            start_time = time.time()
            tasks = [
                send_chat_request(session, i) 
                for i in range(100)
            ]
            responses = await asyncio.gather(*tasks)
            end_time = time.time()
            
            # Verify all requests succeeded
            successful_requests = sum(1 for r in responses if r.get('success'))
            assert successful_requests >= 95  # 95% success rate
            
            # Verify performance
            total_time = end_time - start_time
            requests_per_second = 100 / total_time
            assert requests_per_second >= 50  # Minimum 50 RPS
    
    def test_memory_usage_under_load(self):
        """Test memory usage during heavy load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Simulate heavy load
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(self.simulate_heavy_operation)
                for _ in range(100)
            ]
            
            # Wait for completion
            for future in futures:
                future.result()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024
    
    def simulate_heavy_operation(self):
        """Simulate CPU and memory intensive operation."""
        import json
        
        # Generate and process data
        data = [{'id': i, 'value': f'test_{i}'} for i in range(1000)]
        json_data = json.dumps(data)
        parsed_data = json.loads(json_data)
        
        # Simulate processing
        result = sum(len(item['value']) for item in parsed_data)
        return result
```

## Test Coverage

### Coverage Configuration

```ini
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */config/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

[html]
directory = htmlcov
```

### Running Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m pytest tests/

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html

# View detailed coverage
open htmlcov/index.html
```

## Continuous Integration

### GitHub Actions Test Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run linting
      run: |
        flake8 src tests
        black --check src tests
        
    - name: Run type checking
      run: mypy src
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
        
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
```

## Testing Best Practices

### Writing Good Tests

!!! tip "Test Writing Guidelines"
    - **One assertion per test**: Focus on single behavior
    - **Descriptive test names**: Clearly indicate what's being tested
    - **Arrange-Act-Assert**: Structure tests clearly
    - **Use fixtures**: Avoid code duplication
    - **Mock external dependencies**: Isolate units under test
    - **Test edge cases**: Include boundary conditions
    - **Keep tests fast**: Optimize for quick feedback

### Test Data Management

```python
# Test data factories
class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_user(username="test_user", role="staff"):
        """Create test user."""
        return {
            'username': username,
            'email': f"{username}@test.com",
            'role': role,
            'active': True
        }
    
    @staticmethod
    def create_concern(title="Test Concern"):
        """Create test concern."""
        return {
            'title': title,
            'description': f"Description for {title}",
            'category': 'infrastructure',
            'priority': 'medium',
            'status': 'submitted'
        }
    
    @staticmethod
    def create_chat_message(message="Test message"):
        """Create test chat message."""
        return {
            'message': message,
            'session_id': 'test_session',
            'timestamp': '2025-01-01T10:00:00Z'
        }
```

## Debugging Tests

### Test Debugging Tips

```python
# Add debugging information to tests
def test_with_debugging(self, caplog):
    """Test with debugging output."""
    import logging
    
    # Enable debug logging
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Your test code here
    result = some_function()
    
    # Check logs
    assert "expected log message" in caplog.text
    
    # Add breakpoint for interactive debugging
    import pdb; pdb.set_trace()

# Use pytest markers for selective testing
@pytest.mark.slow
def test_slow_operation():
    """Mark slow tests for optional execution."""
    pass

@pytest.mark.integration
def test_external_api():
    """Mark integration tests."""
    pass
```

### Running Specific Tests

```bash
# Run specific test file
pytest tests/unit/test_auth.py

# Run specific test method
pytest tests/unit/test_auth.py::TestAuthentication::test_login_success

# Run tests with specific marker
pytest -m "not slow"

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x

# Run tests in parallel
pytest -n auto
```

## Next Steps

- **[Architecture](architecture.md)** - Understand system architecture
- **[Deployment](deployment.md)** - Learn about deployment strategies
- **[Contributing](contributing.md)** - Contribution guidelines and setup

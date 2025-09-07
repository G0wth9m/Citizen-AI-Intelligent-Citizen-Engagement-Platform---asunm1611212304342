# Frequently Asked Questions

Find answers to common questions about CitizenAI installation, configuration, and usage.

## General Questions

### What is CitizenAI?

CitizenAI is an intelligent citizen engagement platform designed to revolutionize how governments interact with the public. It uses AI technologies like IBM Granite models and Watson to provide real-time, intelligent responses to citizen inquiries.

### What are the main features?

!!! info "Core Features"
    - **AI Chat Assistant**: Real-time conversational AI
    - **Sentiment Analysis**: Automatic feedback classification
    - **Analytics Dashboard**: Real-time visualizations and insights
    - **Concern Reporting**: Issue submission and tracking
    - **User Authentication**: Secure session management
    - **Responsive Design**: Works on all devices

### Is CitizenAI free to use?

Yes, CitizenAI is open-source and free to use under the MIT License. However, some AI features require IBM Watson API credentials, which may have associated costs depending on usage.

## Installation & Setup

### What are the system requirements?

**Minimum Requirements:**
- Python 3.11 or higher
- 4GB RAM
- 1GB free disk space
- Modern web browser

**Recommended:**
- Python 3.11+
- 8GB RAM
- SSD storage
- Chrome, Firefox, Safari, or Edge (latest versions)

### I'm getting a "Python not found" error

??? question "Python Installation Issues"
    **On Windows:**
    ```bash
    # Check if Python is installed
    python --version
    
    # If not found, download from python.org
    # Make sure to check "Add to PATH" during installation
    ```
    
    **On macOS:**
    ```bash
    # Install using Homebrew
    brew install python
    
    # Or download from python.org
    ```
    
    **On Linux:**
    ```bash
    # Ubuntu/Debian
    sudo apt update
    sudo apt install python3 python3-pip
    
    # CentOS/RHEL
    sudo yum install python3 python3-pip
    ```

### How do I fix "Module not found" errors?

This usually means dependencies aren't installed correctly:

```bash
# Ensure you're in the project directory
cd Citizen-AI

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### The application won't start - what should I check?

1. **Check Python version**:
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Verify virtual environment**:
   ```bash
   # Should show the virtual environment path
   which python  # macOS/Linux
   where python  # Windows
   ```

3. **Check for port conflicts**:
   ```bash
   # Check if port 5000 is in use
   netstat -an | grep 5000
   ```

4. **Review error messages**:
   ```bash
   # Run with verbose output
   python app_demo.py --debug
   ```

## Configuration

### How do I get IBM Watson credentials?

1. **Create IBM Cloud account** at [cloud.ibm.com](https://cloud.ibm.com)
2. **Create Watson Assistant service**:
   - Navigate to Catalog > AI > Watson Assistant
   - Create a new instance (Lite plan is free)
3. **Get credentials**:
   - Go to your Watson Assistant instance
   - Click "Service credentials" > "New credential"
   - Copy the API key and URL

### Can I run CitizenAI without IBM Watson?

Yes! Use the demo version which provides full functionality with mock AI responses:

```bash
# Run demo version (no Watson required)
python app_demo.py
```

The demo version includes:
- Complete UI experience
- Sample data and analytics
- Mock chat responses
- All features except live AI

### How do I configure the application for production?

1. **Create production environment file**:
   ```bash title=".env.production"
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=your-very-secure-secret-key
   
   # Watson credentials
   WATSON_API_KEY=your-production-api-key
   WATSON_URL=your-watson-url
   
   # Security settings
   SESSION_COOKIE_SECURE=True
   SESSION_COOKIE_HTTPONLY=True
   ```

2. **Set up reverse proxy** (nginx/Apache)
3. **Configure SSL/TLS certificates**
4. **Set up monitoring and logging**

## Usage

### How do I log in to the application?

Default credentials for the demo:
- **Username**: `admin`
- **Password**: `password`

!!! warning "Security Note"
    Change these credentials before deploying to production!

### The chat isn't responding - what's wrong?

**For Demo Version:**
- Demo responses should work immediately
- Check browser console for JavaScript errors

**For AI Version:**
- Verify Watson credentials in `.env` file
- Check network connectivity
- Review application logs for API errors

### How do I export analytics data?

1. **Via Web Interface**:
   - Go to Dashboard
   - Click "Export" button
   - Choose format (CSV, JSON, PDF)

2. **Via API**:
   ```python
   import requests
   
   response = requests.get(
       'http://localhost:5000/api/v1/analytics/export',
       params={'format': 'csv', 'date_range': '30d'}
   )
   ```

### Can I customize the appearance?

Yes! You can customize:

- **Colors and themes** in `static/css/styles.css`
- **Layout** in template files (`templates/`)
- **Logo and branding** by replacing image files
- **Content** by editing template text

## Troubleshooting

### The application is slow - how can I improve performance?

**Common Solutions:**

1. **Enable caching**:
   ```python
   # Add to your configuration
   CACHE_TYPE = 'simple'
   CACHE_DEFAULT_TIMEOUT = 300
   ```

2. **Use production WSGI server**:
   ```bash
   # Install gunicorn
   pip install gunicorn
   
   # Run with gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Optimize database queries**
4. **Enable gzip compression**
5. **Use CDN for static assets**

### I'm getting "413 Request Entity Too Large" errors

This happens when uploading large files. Increase the upload limit:

```python
# In your Flask configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Sessions aren't persisting across requests

Check session configuration:

```python
# Ensure these are set
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
```

### The analytics dashboard isn't loading

1. **Check browser console** for JavaScript errors
2. **Verify API endpoints** are responding
3. **Check data permissions**
4. **Clear browser cache**

## API Questions

### How do I get an API key?

Currently, API access uses session-based authentication. For programmatic access:

1. **Login via API**:
   ```python
   response = requests.post(
       'http://localhost:5000/api/v1/auth/login',
       json={'username': 'admin', 'password': 'password'}
   )
   ```

2. **Use session cookies** for subsequent requests

### What's the API rate limit?

Default limits:
- **Authenticated requests**: 1000/hour
- **Chat API**: 500/hour
- **Analytics API**: 200/hour

### How do I integrate CitizenAI with my existing system?

1. **Use the REST API** for data exchange
2. **Implement webhooks** for real-time notifications
3. **Use embedded chat widget**
4. **Import/export data** via API endpoints

## Development

### How do I contribute to the project?

1. **Fork the repository** on GitHub
2. **Set up development environment**
3. **Create feature branch**
4. **Make changes and add tests**
5. **Submit pull request**

See the [Contributing Guide](../development/contributing.md) for detailed instructions.

### How do I report bugs or request features?

1. **Check existing issues** on GitHub
2. **Create new issue** with detailed description
3. **Use appropriate templates** (bug report/feature request)
4. **Provide reproduction steps** for bugs

### Can I use CitizenAI as a library in my Python project?

While primarily designed as a web application, you can import and use specific components:

```python
from src.chat.engine import ChatEngine
from src.analytics.processor import AnalyticsProcessor

# Use individual components
chat_engine = ChatEngine(api_key='your-key')
response = chat_engine.process_message('Hello')
```

## Deployment

### How do I deploy CitizenAI to production?

**Recommended Production Setup:**

1. **Application Server**: Gunicorn or uWSGI
2. **Web Server**: Nginx (reverse proxy)
3. **Database**: PostgreSQL (for large deployments)
4. **Caching**: Redis
5. **Monitoring**: Prometheus + Grafana

See [Deployment Guide](../development/deployment.md) for detailed instructions.

### Can I deploy on cloud platforms?

Yes! CitizenAI can be deployed on:

- **Heroku**: Using Git-based deployment
- **AWS**: EC2, Elastic Beanstalk, or ECS
- **Google Cloud**: App Engine or Compute Engine
- **Microsoft Azure**: App Service or Container Instances
- **DigitalOcean**: Droplets or App Platform

### How do I set up SSL/HTTPS?

**Using nginx:**

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Support

### Where can I get help?

1. **Documentation**: This documentation site
2. **GitHub Issues**: Bug reports and feature requests
3. **GitHub Discussions**: General questions and community help
4. **Community**: Join project discussions

### How do I contact the development team?

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and community support
- **Email**: Check repository README for contact information

### Is commercial support available?

Currently, CitizenAI is a community-driven open-source project. For commercial support or custom development, you can:

1. **Create GitHub issue** describing your needs
2. **Contact contributors** directly
3. **Hire consultants** familiar with the codebase

---

!!! question "Question Not Answered?"
    If you can't find the answer to your question here, please:
    
    1. Search [GitHub Issues](https://github.com/AkhileshMalthi/Citizen-AI/issues)
    2. Create a new [GitHub Discussion](https://github.com/AkhileshMalthi/Citizen-AI/discussions)
    3. Check the [Troubleshooting Guide](troubleshooting.md)

# Deployment

This guide covers deployment strategies and procedures for CitizenAI in different environments.

## Overview

CitizenAI supports multiple deployment scenarios:

- **Local Development**: For testing and development
- **Production Server**: Full-scale deployment
- **Docker Containers**: Containerized deployment
- **Cloud Platforms**: AWS, Azure, Google Cloud deployment

## Prerequisites

Before deploying CitizenAI, ensure you have:

- Python 3.8 or higher
- Required dependencies installed
- Database configured
- Environment variables set
- SSL certificates (for production)

## Local Development Deployment

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-org/citizen-ai.git
cd citizen-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## Production Deployment

### Server Requirements

- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 20GB minimum
- **OS**: Ubuntu 20.04+ or CentOS 7+

### Installation Steps

1. **Prepare the server**:
```bash
sudo apt update
sudo apt install python3 python3-pip nginx
```

2. **Clone and setup application**:
```bash
git clone https://github.com/your-org/citizen-ai.git
cd citizen-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
sudo nano /etc/environment
# Add your environment variables
```

4. **Setup systemd service**:
```bash
sudo nano /etc/systemd/system/citizen-ai.service
```

Service file content:
```ini
[Unit]
Description=CitizenAI Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/citizen-ai
Environment="PATH=/path/to/citizen-ai/venv/bin"
ExecStart=/path/to/citizen-ai/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start the service**:
```bash
sudo systemctl daemon-reload
sudo systemctl start citizen-ai
sudo systemctl enable citizen-ai
```

### Nginx Configuration

Create nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/citizen-ai
```

Configuration content:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/citizen-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Docker Deployment

### Dockerfile

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  citizen-ai:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/citizenai
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=citizenai
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Cloud Platform Deployment

### AWS Deployment

#### Using EC2

1. Launch EC2 instance (Ubuntu 20.04)
2. Configure security groups (ports 22, 80, 443)
3. Follow production deployment steps
4. Configure Load Balancer if needed

#### Using Elastic Beanstalk

1. Create `application.py` (entry point)
2. Package application
3. Deploy through EB console
4. Configure environment variables

### Azure Deployment

#### Using App Service

1. Create Azure App Service
2. Configure Python runtime
3. Deploy via Git or Azure CLI
4. Set application settings

### Google Cloud Deployment

#### Using App Engine

Create `app.yaml`:

```yaml
runtime: python39

env_variables:
  FLASK_ENV: production
  DATABASE_URL: your-database-url

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

Deploy:
```bash
gcloud app deploy
```

## Environment Configuration

### Environment Variables

Required environment variables:

```bash
# Application
FLASK_ENV=production
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# AI Services
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key

# Security
JWT_SECRET_KEY=your-jwt-secret
CORS_ORIGINS=https://your-domain.com
```

### Configuration Management

Use different configuration files for different environments:

- `config/development.py`
- `config/production.py`
- `config/testing.py`

## Database Setup

### PostgreSQL

1. **Install PostgreSQL**:
```bash
sudo apt install postgresql postgresql-contrib
```

2. **Create database and user**:
```sql
CREATE DATABASE citizenai;
CREATE USER citizenai_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE citizenai TO citizenai_user;
```

3. **Run migrations**:
```bash
python manage.py db upgrade
```

## SSL/TLS Configuration

### Using Let's Encrypt

1. **Install Certbot**:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain certificate**:
```bash
sudo certbot --nginx -d your-domain.com
```

3. **Auto-renewal**:
```bash
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### Application Logging

Configure logging in your application:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/citizenai.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### System Monitoring

Use tools like:
- **htop** for system resources
- **nginx access logs** for web traffic
- **systemd journal** for service logs

## Backup and Recovery

### Database Backup

```bash
# Create backup
pg_dump citizenai > backup_$(date +%Y%m%d).sql

# Restore backup
psql citizenai < backup_20231201.sql
```

### Application Backup

```bash
# Backup application files
tar -czf citizen-ai-backup-$(date +%Y%m%d).tar.gz /path/to/citizen-ai
```

## Performance Optimization

### Application Level

1. **Use caching** (Redis/Memcached)
2. **Optimize database queries**
3. **Implement connection pooling**
4. **Use CDN for static assets**

### Server Level

1. **Configure Gunicorn** for production:
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

2. **Optimize Nginx**:
```nginx
worker_processes auto;
worker_connections 1024;
```

## Security Considerations

### Application Security

- Use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Use secure session management
- Regular security updates

### Server Security

- Configure firewall (ufw)
- Disable root SSH access
- Use SSH key authentication
- Regular system updates
- Monitor access logs

## Troubleshooting

### Common Issues

1. **Port conflicts**: Check if port 5000 is available
2. **Permission errors**: Verify file permissions
3. **Database connection**: Check database credentials
4. **Environment variables**: Verify all required vars are set

### Debug Commands

```bash
# Check service status
sudo systemctl status citizen-ai

# View logs
sudo journalctl -u citizen-ai -f

# Check ports
sudo netstat -tlnp | grep :5000

# Test database connection
psql -h localhost -U citizenai_user -d citizenai
```

## Maintenance

### Regular Tasks

1. **Update dependencies**:
```bash
pip install --upgrade -r requirements.txt
```

2. **Database maintenance**:
```bash
# Vacuum database
psql citizenai -c "VACUUM ANALYZE;"
```

3. **Log rotation**:
```bash
# Configure logrotate
sudo nano /etc/logrotate.d/citizen-ai
```

4. **Security updates**:
```bash
sudo apt update && sudo apt upgrade
```

## Scaling

### Horizontal Scaling

- Use load balancers (nginx, HAProxy)
- Deploy multiple application instances
- Implement session storage (Redis)
- Use database replication

### Vertical Scaling

- Increase server resources
- Optimize database configuration
- Use application profiling
- Implement caching strategies

## Support

For deployment issues:

- Check the [Troubleshooting Guide](../support/troubleshooting.md)
- Review [FAQ](../support/faq.md)
- Contact support team
- File issues on GitHub

## Next Steps

After successful deployment:

1. Set up monitoring and alerts
2. Configure automated backups
3. Implement CI/CD pipeline
4. Plan disaster recovery
5. Document operational procedures

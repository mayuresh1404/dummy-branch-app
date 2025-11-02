# 🏦 Microloans API - Branch Assignment

A production-ready containerized Flask API for managing microloans with automated CI/CD pipeline, multi-environment support, and comprehensive security scanning.

[![CI/CD Pipeline](https://github.com/mayuresh1404/dummy-branch-app/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/mayuresh1404/dummy-branch-app/actions)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Running Locally](#running-locally)
- [Environment Configuration](#environment-configuration)
- [API Endpoints](#api-endpoints)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This application provides a RESTful API for managing microloans with the following features:

- ✅ **Multi-environment support** (Development, Staging, Production)
- ✅ **Containerized with Docker** for consistent deployments
- ✅ **Automated CI/CD pipeline** with GitHub Actions
- ✅ **Security scanning** with Trivy
- ✅ **HTTPS/SSL support** with Nginx reverse proxy
- ✅ **PostgreSQL database** with automated migrations
- ✅ **Resource limits** for each environment
- ✅ **Health checks** and monitoring

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIENT                                  │
│                     (Browser/API Client)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTPS (443) / HTTP (80)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NGINX REVERSE PROXY                         │
│                   (SSL Termination + Load Balancing)             │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP (8000)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FLASK API                                 │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Routes     │  │   Business   │  │   Database   │          │
│  │  /api/loans  │─▶│    Logic     │─▶│    Models    │          │
│  │  /api/stats  │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────┬───────┘          │
│                                              │                   │
└──────────────────────────────────────────────┼───────────────────┘
                                               │ TCP (5432)
                                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    loans     │  │  borrowers   │  │   payments   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│               (Persistent Volume: postgres_data)                 │
└─────────────────────────────────────────────────────────────────┘

                    GitHub Actions CI/CD Pipeline
┌─────────────────────────────────────────────────────────────────┐
│  Push to main → Test → Build → Security Scan → Deploy           │
│                   ↓      ↓          ↓             ↓             │
│               pytest  Docker   Trivy Scan   GitHub Packages     │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Client Request** → Nginx (Port 443/80)
2. **Nginx** → Forwards to Flask API (Port 8000)
3. **Flask API** → Processes request, queries database
4. **PostgreSQL** → Returns data
5. **Flask API** → Sends JSON response
6. **Nginx** → Returns response to client

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Git installed
- 4GB RAM minimum
- 10GB free disk space

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mayuresh1404/dummy-branch-app.git
cd dummy-branch-app
```

### 2️⃣ Generate SSL Certificates (For HTTPS)

```bash
# Create SSL directory
mkdir -p nginx/ssl

# Generate self-signed certificate (valid for 365 days)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/nginx-selfsigned.key \
  -out nginx/ssl/nginx-selfsigned.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=branchloans.com"

# Verify certificates created
ls -la nginx/ssl/
```

### 3️⃣ Add Domain to Hosts File

**Linux/Mac:**
```bash
sudo nano /etc/hosts
# Add this line:
127.0.0.1    branchloans.com
```

**Windows:**
```powershell
# Run as Administrator
notepad C:\Windows\System32\drivers\etc\hosts
# Add this line:
127.0.0.1    branchloans.com
```

### 4️⃣ Start the Application

```bash
# Start all services
docker-compose up -d

# Wait for services to be healthy (30 seconds)
sleep 30

# Check status
docker-compose ps
```

### 5️⃣ Test the Application

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test with HTTPS (accept security warning in browser)
curl -k https://branchloans.com/health

# Test API endpoints
curl -k https://branchloans.com/api/loans
curl -k https://branchloans.com/api/stats
```

**Open in Browser:** https://branchloans.com (Accept security warning for self-signed certificate)

---

## 💻 Running Locally

### Development Mode

```bash
# Use development environment
cp .env.development .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Staging Mode

```bash
# Use staging environment
cp .env.staging .env

# Start services
docker-compose up -d --build

# Run staging tests
docker-compose exec api pytest
```

### Production Mode

```bash
# Use production environment
cp .env.production .env

# Start services with resource limits
docker-compose up -d --build

# Monitor performance
docker stats
```

### Manual Database Operations

```bash
# Access database
docker-compose exec db psql -U postgres -d microloans

# Run migrations
docker-compose exec api alembic upgrade head

# Seed database
docker-compose exec api python scripts/seed.py

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"
```

### Useful Commands

```bash
# View all containers
docker-compose ps

# View logs for specific service
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f nginx

# Restart a service
docker-compose restart api

# Rebuild and restart
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: deletes data)
docker-compose down -v

# Shell access to container
docker-compose exec api bash
docker-compose exec db psql -U postgres

# Check resource usage
docker stats

# Clean up Docker system
docker system prune -a --volumes
```

---

## ⚙️ Environment Configuration

### Switching Between Environments

The application supports three environments, each with different configurations:

| Environment | Use Case | Resources | Features |
|------------|----------|-----------|----------|
| **Development** | Local development | Low | Debug mode, hot reload |
| **Staging** | Pre-production testing | Medium | Production-like |
| **Production** | Live deployment | High | Optimized, secure |

### Environment Files

Create `.env` file based on your environment:

```bash
# Development
cp .env.development .env

# Staging
cp .env.staging .env

# Production
cp .env.production .env
```

### Environment Variables Explained

#### Database Configuration

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DB_USER` | PostgreSQL username | `postgres` | Yes |
| `DB_PASSWORD` | PostgreSQL password | `secure_password` | Yes |
| `DB_NAME` | Database name | `microloans` | Yes |
| `DB_PORT` | Database port | `5432` | Yes |
| `DATABASE_URL` | Full connection string | `postgresql+psycopg2://user:pass@db:5432/dbname` | Yes |

#### Application Configuration

| Variable | Description | Values | Default |
|----------|-------------|--------|---------|
| `FLASK_ENV` | Flask environment | `development`, `staging`, `production` | `development` |
| `APP_PORT` | Application port | `8000` | `8000` |
| `LOG_LEVEL` | Logging verbosity | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |

#### Resource Limits

| Variable | Description | Development | Staging | Production |
|----------|-------------|-------------|---------|------------|
| `DB_CPU_LIMIT` | Database CPU limit | `1.0` | `1.5` | `2.0` |
| `DB_MEMORY_LIMIT` | Database memory | `512M` | `1G` | `2G` |
| `API_CPU_LIMIT` | API CPU limit | `0.5` | `1.0` | `2.0` |
| `API_MEMORY_LIMIT` | API memory | `512M` | `1G` | `2G` |

#### Volume Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `VOLUME_MOUNT` | Host directory for logs | `./logs` |

#### Docker Configuration

| Variable | Description | Options |
|----------|-------------|---------|
| `RESTART_POLICY` | Container restart behavior | `no`, `always`, `on-failure`, `unless-stopped` |

### Example .env.development

```bash
# Database
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=microloans_dev
DB_PORT=5432

# Application
FLASK_ENV=development
APP_PORT=8000
LOG_LEVEL=DEBUG

# Resources (Low for development)
DB_CPU_LIMIT=1.0
DB_MEMORY_LIMIT=512M
API_CPU_LIMIT=0.5
API_MEMORY_LIMIT=512M

# Volumes
VOLUME_MOUNT=./logs

# Restart Policy
RESTART_POLICY=unless-stopped
```

### Example .env.production

```bash
# Database
DB_USER=prod_user
DB_PASSWORD=super_secure_password_here
DB_NAME=microloans_prod
DB_PORT=5432

# Application
FLASK_ENV=production
APP_PORT=8000
LOG_LEVEL=WARNING

# Resources (High for production)
DB_CPU_LIMIT=2.0
DB_MEMORY_LIMIT=2G
API_CPU_LIMIT=2.0
API_MEMORY_LIMIT=2G

# Volumes
VOLUME_MOUNT=./logs

# Restart Policy
RESTART_POLICY=always
```

---

## 🔌 API Endpoints

### Health Check

```bash
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-11-03T10:30:00Z"
}
```

### Get All Loans

```bash
GET /api/loans
GET /api/loans?limit=10

Response:
[
  {
    "id": 1,
    "amount": 5000.00,
    "term_months": 12,
    "interest_rate": 5.5,
    "status": "active",
    "borrower_id": 1,
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

### Get Loan Statistics

```bash
GET /api/stats

Response:
{
  "total_loans": 150,
  "total_amount": 750000.00,
  "active_loans": 120,
  "default_rate": 2.5
}
```

### Get Borrowers

```bash
GET /api/borrowers

Response:
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "credit_score": 750
  }
]
```

---

## 🔄 CI/CD Pipeline

### Pipeline Overview

The GitHub Actions pipeline automatically runs on every push to `main` or `develop` branches.

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1️⃣ TEST STAGE (2 minutes)                                  │
│     ├─ Setup Python & PostgreSQL                            │
│     ├─ Install dependencies                                 │
│     ├─ Run flake8 linting                                   │
│     ├─ Execute pytest tests                                 │
│     └─ Generate coverage reports                            │
│                                                              │
│  2️⃣ BUILD STAGE (3 minutes)                                 │
│     ├─ Setup Docker Buildx                                  │
│     ├─ Login to GitHub Container Registry                   │
│     ├─ Build Docker image (multi-stage)                     │
│     ├─ Tag image (latest, main-sha)                         │
│     └─ Push to ghcr.io                                      │
│                                                              │
│  3️⃣ SECURITY SCAN STAGE (2 minutes)                         │
│     ├─ Pull built Docker image                              │
│     ├─ Run Trivy vulnerability scanner                      │
│     ├─ Upload results to Security tab                       │
│     └─ Fail on CRITICAL vulnerabilities                     │
│                                                              │
│  4️⃣ DEPLOY STAGE (10 seconds)                               │
│     ├─ Create deployment summary                            │
│     ├─ Generate pull commands                               │
│     └─ Notify deployment ready                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### How It Works

1. **Trigger**: Push to `main` or `develop` branch
2. **Test**: Runs all tests with PostgreSQL service container
3. **Build**: Creates optimized Docker image
4. **Scan**: Checks for security vulnerabilities
5. **Publish**: Pushes image to GitHub Container Registry
6. **Notify**: Creates deployment summary

### Viewing Pipeline Results

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Click on the latest workflow run
4. View each job's logs and status

### Pipeline Configuration

The pipeline is defined in `.github/workflows/ci-cd.yml` and includes:

- **Automatic triggers** on push/PR
- **Manual trigger** via workflow_dispatch
- **Parallel job execution** where possible
- **Caching** for faster builds
- **Failure notifications**

### Accessing Published Images

```bash
# View packages
# Go to: https://github.com/mayuresh1404?tab=packages

# Pull latest image
docker pull ghcr.io/mayuresh1404/dummy-branch-app:latest

# Pull specific version
docker pull ghcr.io/mayuresh1404/dummy-branch-app:main-abc123

# Use in docker-compose
services:
  api:
    image: ghcr.io/mayuresh1404/dummy-branch-app:latest
```

---

## 🧪 Testing

### Run Tests Locally

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Test Structure

```
tests/
├── __init__.py          # Test configuration
├── conftest.py          # Shared fixtures
├── test_api.py          # API endpoint tests

```

### Writing New Tests

```python
# tests/test_example.py
import pytest

def test_example(client):
    """Test example endpoint"""
    response = client.get('/api/example')
    assert response.status_code == 200
    assert 'data' in response.get_json()
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use

**Problem:** 
```
Error: port 5432 already in use
```

**Solution:**
```bash
# Find process using port
lsof -i :5432  # Mac/Linux
netstat -ano | findstr :5432  # Windows

# Stop conflicting service
docker-compose down
# or kill the process

# Use different port
# Edit docker-compose.yml: "5433:5432"
```

#### 2. Database Connection Failed

**Problem:**
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Wait for database to be ready
sleep 10
docker-compose exec api python -c "from app.db import test_connection; test_connection()"
```

#### 3. Permission Denied Errors

**Problem:**
```
Permission denied: '/app/logs'
```

**Solutions:**
```bash
# Fix permissions
chmod -R 777 logs/

# Or run with sudo (not recommended for production)
sudo docker-compose up -d
```

#### 4. SSL Certificate Issues

**Problem:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
```bash
# Regenerate certificates
rm -rf nginx/ssl/*
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/nginx-selfsigned.key \
  -out nginx/ssl/nginx-selfsigned.crt \
  -subj "/C=US/ST=State/L=City/O=Org/CN=branchloans.com"

# Or use curl with -k flag
curl -k https://branchloans.com/health
```

#### 5. Docker Build Fails

**Problem:**
```
ERROR: failed to solve: process "/bin/sh -c pip install..." did not complete
```

**Solutions:**
```bash
# Clean Docker cache
docker builder prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker-compose config
```

#### 6. Migration Errors

**Problem:**
```
alembic.util.exc.CommandError: Can't locate revision identified by 'xxx'
```

**Solutions:**
```bash
# Reset migrations
docker-compose exec api alembic downgrade base
docker-compose exec api alembic upgrade head

# Or start fresh
docker-compose down -v
docker-compose up -d
```

#### 7. Tests Failing in CI/CD

**Problem:**
```
pytest: No module named 'app'
```

**Solutions:**
```bash
# Ensure PYTHONPATH is set
# In docker-compose.yml:
environment:
  - PYTHONPATH=/app

# Or in tests/__init__.py:
import sys
sys.path.insert(0, '/app')
```

### Health Check Commands

```bash
# Check all services
docker-compose ps

# Should show all services as "Up (healthy)"

# Check API health
curl http://localhost:8000/health

# Check database
docker-compose exec db pg_isready -U postgres

# Check Nginx
curl -I http://localhost

# Check logs for errors
docker-compose logs --tail=50 api
docker-compose logs --tail=50 db
docker-compose logs --tail=50 nginx

# Test database connection
docker-compose exec api python -c "
from app.db import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connected!')
"
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Increase resources in .env
DB_CPU_LIMIT=2.0
DB_MEMORY_LIMIT=2G
API_CPU_LIMIT=2.0
API_MEMORY_LIMIT=2G

# Restart with new limits
docker-compose down
docker-compose up -d
```

### Clean Slate Reset

If nothing works, start completely fresh:

```bash
# Stop everything
docker-compose down -v

# Remove all containers and images
docker system prune -a --volumes -f

# Remove logs
rm -rf logs/*

# Rebuild from scratch
docker-compose up -d --build

# Wait for startup
sleep 30

# Test
curl http://localhost:8000/health
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is part of the Branch DevOps Intern assignment.

---

## 📧 Contact

**Mayuresh** - [@mayuresh1404](https://github.com/mayuresh1404)

**Project Link:** [https://github.com/mayuresh1404/dummy-branch-app](https://github.com/mayuresh1404/dummy-branch-app)

---

## ✅ Assignment Checklist

- [x] Containerized Flask application with Docker
- [x] Multi-environment support (dev/staging/prod)
- [x] Automated CI/CD pipeline with GitHub Actions
- [x] HTTPS setup with Nginx reverse proxy
- [x] Security scanning with Trivy
- [x] PostgreSQL database with migrations
- [x] Health checks and monitoring
- [x] Resource limits per environment
- [x] Comprehensive documentation
- [x] Troubleshooting guide

---

**Built with ❤️ for Branch**

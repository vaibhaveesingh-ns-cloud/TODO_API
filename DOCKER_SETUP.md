# PostgreSQL Docker Setup for TaskMaster

This guide will help you set up PostgreSQL using Docker containers for the TaskMaster application.

## 🐳 Prerequisites

- **Docker** and **Docker Compose** installed
- **Git** for cloning the repository

## 🚀 Quick Start

### 1. Start PostgreSQL Container

```bash
# Start PostgreSQL and pgAdmin containers
docker-compose up -d

# Check container status
docker-compose ps
```

### 2. Install Python Dependencies

```bash
# Install PostgreSQL driver and other dependencies
pip install -r requirements.txt
```

### 3. Start FastAPI Application

```bash
# The app will automatically connect to PostgreSQL
uvicorn app.main:app --reload
```

### 4. Verify Connection

Visit `http://localhost:8000/health` to check database connection status.

## 📊 Database Access

### Default Credentials

- **Database**: `taskmaster`
- **Username**: `taskmaster_user`
- **Password**: `taskmaster_password`
- **Host**: `localhost`
- **Port**: `5432`

### pgAdmin Web Interface

Access pgAdmin at `http://localhost:8080`:

- **Email**: `admin@taskmaster.com`
- **Password**: `admin123`

#### Adding Server in pgAdmin

1. Right-click "Servers" → "Create" → "Server"
2. **General Tab**:
   - Name: `TaskMaster PostgreSQL`
3. **Connection Tab**:
   - Host: `postgres` (container name)
   - Port: `5432`
   - Database: `taskmaster`
   - Username: `taskmaster_user`
   - Password: `taskmaster_password`

## 🗄️ Database Schema

The database is automatically initialized with:

### Tables
- **users**: User accounts with authentication
- **todos**: Task items linked to users

### Sample Data
- Admin user: `admin` / `admin123`
- Sample todos for testing

### Indexes
- Optimized indexes for common queries
- Foreign key relationships with cascading deletes

## 🔧 Docker Commands

### Container Management

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs postgres
docker-compose logs pgadmin

# Restart containers
docker-compose restart

# Remove containers and volumes (⚠️ DATA LOSS)
docker-compose down -v
```

### Database Operations

```bash
# Connect to PostgreSQL container
docker exec -it taskmaster_postgres psql -U taskmaster_user -d taskmaster

# Backup database
docker exec taskmaster_postgres pg_dump -U taskmaster_user taskmaster > backup.sql

# Restore database
docker exec -i taskmaster_postgres psql -U taskmaster_user -d taskmaster < backup.sql
```

## 🔄 Environment Configuration

### Using Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
DATABASE_URL=postgresql://taskmaster_user:taskmaster_password@localhost:5432/taskmaster
SECRET_KEY=your-super-secret-jwt-key
```

### Production Configuration

For production, update `docker-compose.yml`:

```yaml
environment:
  POSTGRES_DB: ${POSTGRES_DB}
  POSTGRES_USER: ${POSTGRES_USER}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

## 🔍 Troubleshooting

### Common Issues

1. **Port 5432 already in use**
   ```bash
   # Check what's using the port
   lsof -i :5432
   
   # Stop local PostgreSQL service
   sudo service postgresql stop
   ```

2. **Connection refused**
   ```bash
   # Check container status
   docker-compose ps
   
   # Check container logs
   docker-compose logs postgres
   ```

3. **Permission denied**
   ```bash
   # Fix volume permissions
   sudo chown -R 999:999 postgres_data/
   ```

### Health Checks

```bash
# Check database health
curl http://localhost:8000/health

# Test database connection
docker exec taskmaster_postgres pg_isready -U taskmaster_user
```

## 📈 Performance Tuning

### PostgreSQL Configuration

For production, consider adding to `docker-compose.yml`:

```yaml
command: >
  postgres
  -c shared_preload_libraries=pg_stat_statements
  -c max_connections=200
  -c shared_buffers=256MB
  -c effective_cache_size=1GB
```

### Connection Pooling

Consider using pgBouncer for connection pooling in production:

```yaml
pgbouncer:
  image: pgbouncer/pgbouncer:latest
  environment:
    DATABASES_HOST: postgres
    DATABASES_PORT: 5432
    DATABASES_USER: taskmaster_user
    DATABASES_PASSWORD: taskmaster_password
    DATABASES_DBNAME: taskmaster
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Change default passwords
- [ ] Use environment variables for secrets
- [ ] Enable SSL/TLS connections
- [ ] Configure firewall rules
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor access logs

### SSL Configuration

For production SSL, add to PostgreSQL:

```yaml
volumes:
  - ./ssl/server.crt:/var/lib/postgresql/server.crt
  - ./ssl/server.key:/var/lib/postgresql/server.key
command: >
  postgres
  -c ssl=on
  -c ssl_cert_file=/var/lib/postgresql/server.crt
  -c ssl_key_file=/var/lib/postgresql/server.key
```

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [FastAPI Database Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## 🆘 Support

If you encounter issues:

1. Check container logs: `docker-compose logs`
2. Verify network connectivity: `docker network ls`
3. Test database connection: `docker exec -it taskmaster_postgres psql -U taskmaster_user -d taskmaster`
4. Check FastAPI health endpoint: `curl http://localhost:8000/health`

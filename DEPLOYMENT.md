# 🚀 TaskMaster Backend Deployment Guide

## Free Hosting Options (Always-On)

### 🥇 **Railway (Recommended)**
**Why Railway?**
- ✅ Always-on (no sleep mode)
- ✅ 500 hours/month + $5 credit
- ✅ Built-in PostgreSQL database
- ✅ Automatic HTTPS
- ✅ Git-based deployment

**Steps:**
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Sign up with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository
6. Railway will auto-detect FastAPI and deploy

**Environment Variables to Set:**
```
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=https://your-frontend-domain.com
```

### 🥈 **Koyeb (Great Alternative)**
**Why Koyeb?**
- ✅ Always-on free tier
- ✅ 2 services included
- ✅ Global edge locations
- ✅ No cold starts

**Steps:**
1. Go to [koyeb.com](https://www.koyeb.com)
2. Sign up with GitHub
3. Create new app from GitHub repository
4. Set environment variables
5. Deploy

### 🥉 **Fly.io (Advanced)**
**Why Fly.io?**
- ✅ 3 shared VMs free
- ✅ Global deployment
- ✅ Always-on
- ✅ Great performance

**Steps:**
1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `flyctl auth signup`
3. In your project: `flyctl launch`
4. Deploy: `flyctl deploy`

## 📋 Pre-Deployment Checklist

### 1. Update Requirements
Make sure your `requirements.txt` includes production dependencies:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
sqlalchemy>=2.0.0
alembic>=1.12.0
email-validator>=2.1.0
python-multipart>=0.0.6
slowapi
itsdangerous
python-dotenv>=1.0.0
pydantic-settings>=2.1.0
psycopg2-binary>=2.9.0  # For PostgreSQL
```

### 2. Environment Variables
Set these in your hosting platform:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Random secret key (generate with `openssl rand -hex 32`)
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30
- `FRONTEND_URL`: Your frontend domain

### 3. Database Migration
Your app will automatically create tables, but for production use Alembic:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 🔧 Production Optimizations

### 1. Health Check Endpoint
Your app already has `/health` endpoint for monitoring.

### 2. Database Connection Pooling
Already configured in `database.py` for PostgreSQL.

### 3. CORS Configuration
Updated to support production frontend URLs.

## 🌐 Database Options

### Free PostgreSQL:
1. **Railway**: Built-in PostgreSQL (recommended)
2. **Supabase**: 500MB free PostgreSQL
3. **Neon**: 3GB free PostgreSQL
4. **ElephantSQL**: 20MB free PostgreSQL

## 📱 Frontend Deployment
Deploy your React frontend to:
- **Netlify**: Free static hosting
- **Vercel**: Free with great performance
- **GitHub Pages**: Free for public repos

## 🚀 Quick Deploy Commands

### Railway:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### Render:
```bash
# Just push to GitHub and connect in Render dashboard
git add .
git commit -m "Deploy to production"
git push origin main
```

## 🔒 Security Checklist
- ✅ Use strong SECRET_KEY
- ✅ Enable HTTPS (automatic on most platforms)
- ✅ Set proper CORS origins
- ✅ Use environment variables for secrets
- ✅ Enable database SSL in production

## 📊 Monitoring
- Check `/health` endpoint regularly
- Monitor database connections
- Set up uptime monitoring (UptimeRobot, etc.)

## 🆘 Troubleshooting

### Common Issues:
1. **Database connection errors**: Check DATABASE_URL format
2. **CORS errors**: Add your frontend URL to FRONTEND_URL env var
3. **Module import errors**: Ensure all dependencies in requirements.txt
4. **Port binding**: Use `0.0.0.0:$PORT` for hosting platforms

### Logs:
- Railway: `railway logs`
- Render: Check dashboard logs
- Fly.io: `flyctl logs`

---

**Recommendation**: Start with Railway for the easiest deployment experience with always-on hosting.

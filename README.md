# TaskMaster - Full-Stack Todo Application

A modern, collaborative todo application built with **React** frontend and **FastAPI** backend. TaskMaster helps teams organize their work with beautiful UI, real-time collaboration, and powerful task management features.

![TaskMaster](https://img.shields.io/badge/TaskMaster-Full--Stack-blue)
![React](https://img.shields.io/badge/React-18-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![Python](https://img.shields.io/badge/Python-3.11+-3776ab)

## 🚀 Features

### Frontend (React)
- **Modern UI/UX**: Clean, professional design with responsive layout
- **Authentication**: Secure login, registration, and email verification
- **Task Management**: Create, edit, delete, and organize todos
- **Real-time Search**: Find tasks instantly with search and filtering
- **Statistics Dashboard**: Track productivity with visual metrics
- **Protected Routes**: Secure navigation with authentication guards

### Backend (FastAPI)
- **RESTful API**: Clean, documented API endpoints
- **JWT Authentication**: Secure token-based authentication
- **Email Verification**: User account activation via email
- **Database Integration**: SQLAlchemy ORM with SQLite
- **Admin Panel**: User management and administrative functions
- **CORS Support**: Cross-origin requests for React frontend

## 🏗️ Architecture

```
TaskMaster/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── contexts/        # React contexts
│   │   ├── services/        # API service layer
│   │   └── ...
│   └── package.json
├── app/                     # FastAPI application
│   ├── routers/            # API route handlers
│   ├── models.py           # Database models
│   ├── auth.py             # Authentication logic
│   ├── crud.py             # Database operations
│   └── main.py             # FastAPI app entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons
- **Custom CSS** - Utility-first styling

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (easily replaceable)
- **JWT** - JSON Web Tokens for authentication
- **Pydantic** - Data validation
- **Passlib** - Password hashing
- **python-jose** - JWT handling

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **Node.js 16+** with npm
- **Git** for version control

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd TODO_fastapi
```

### 2. Setup Backend (FastAPI)

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server:**
   ```bash
   # Option 1: Direct uvicorn command
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Option 2: Use the local development script
   python run_local.py
   ```

   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### 3. Setup Frontend (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The React app will be available at `http://localhost:3000`

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get access token
- `GET /auth/verify-email` - Verify email address

### Todo Endpoints
- `GET /todos/` - List user's todos
- `POST /todos/` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

### Admin Endpoints
- `GET /admin/users` - List all users (admin only)
- `POST /admin/users/{id}/promote` - Promote user to admin
- `DELETE /admin/users/{id}` - Delete user

## 🔧 Development Tools

The project includes several utility scripts:

- `check_users.py` - View database users and statistics
- `debug_auth.py` - Debug authentication issues
- `generate_verification_token.py` - Generate email verification tokens

### Running Development Tools
```bash
# Check database and list users
python check_users.py

# Debug authentication
python debug_auth.py

# Generate verification tokens
python generate_verification_token.py
```

## 🗄️ Database

The application uses SQLite by default with the following models:

### User Model
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `hashed_password` - Bcrypt hashed password
- `is_active` - Email verification status
- `is_admin` - Admin privileges flag
- `created_at` - Account creation timestamp

### Todo Model
- `id` - Primary key
- `title` - Task title
- `description` - Task description (optional)
- `completed` - Completion status
- `owner_id` - Foreign key to User
- `created_at` - Task creation timestamp

## 🔐 Authentication Flow

1. **User Registration**
   - User submits registration form
   - Account created with `is_active=False`
   - Verification email sent (console output in development)

2. **Email Verification**
   - User clicks verification link
   - Token validated and account activated
   - User can now login

3. **Login Process**
   - User submits credentials
   - JWT token generated and returned
   - Token stored in localStorage (frontend)

4. **Authenticated Requests**
   - Token included in Authorization header
   - Backend validates token on protected routes
   - Auto-logout on token expiration

## 🎨 UI/UX Design

The frontend follows modern design principles:

- **Clean Interface**: Minimal, distraction-free design
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Intuitive Navigation**: Clear user flows and interactions
- **Visual Feedback**: Loading states, success/error messages
- **Accessibility**: Semantic HTML and keyboard navigation

## 🚀 Deployment

### Backend Deployment
1. Update database URL for production
2. Set secure JWT secret key
3. Configure email service (SMTP/SendGrid)
4. Deploy to cloud platform (AWS, Heroku, DigitalOcean)

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Deploy to static hosting (Netlify, Vercel, S3)
3. Update API base URL for production

## 🧪 Testing

### Backend Testing
```bash
# Run with pytest (when tests are added)
pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Development Guidelines
- Follow existing code style and patterns
- Add proper error handling and validation
- Include appropriate comments and documentation
- Test authentication flows thoroughly
- Ensure responsive design for frontend changes

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend CORS is configured for frontend URL
   - Check that both servers are running

2. **Authentication Issues**
   - Verify email before attempting login
   - Check JWT token expiration
   - Clear localStorage if needed

3. **Database Issues**
   - Database is created automatically on first run
   - Use debug scripts to inspect database state

4. **Email Verification**
   - Check console output for verification links in development
   - Configure proper email service for production

### Getting Help

- Check the API documentation at `/docs`
- Use browser dev tools for frontend debugging
- Check server logs for backend issues
- Run the included debug scripts

---

**TaskMaster** - Organize your life, together. 🎯

# TaskMaster Frontend

A modern React frontend for the TaskMaster collaborative todo application, built with React 18 and designed to match the TaskMaster UI/UX specifications.

## Features

- **Modern UI/UX**: Clean, professional design inspired by TaskMaster
- **Authentication**: Login, registration, and email verification
- **Task Management**: Create, read, update, delete todos with real-time updates
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Protected Routes**: Secure navigation with authentication guards
- **Search & Filter**: Find tasks quickly with search and filter functionality
- **Real-time Statistics**: Track completed vs pending tasks

## Tech Stack

- **React 18** - Modern React with hooks
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API communication
- **Lucide React** - Beautiful icons
- **CSS3** - Custom styling with utility classes

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Dashboard.js       # Main task management interface
│   │   ├── LandingPage.js     # Marketing landing page
│   │   ├── Login.js           # User login form
│   │   ├── Register.js        # User registration form
│   │   └── EmailVerification.js # Email verification handler
│   ├── contexts/
│   │   └── AuthContext.js     # Authentication state management
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── App.js                 # Main app component with routing
│   ├── index.js               # React app entry point
│   └── index.css              # Global styles
├── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- FastAPI backend running on `http://localhost:8000`

### Installation

1. **Navigate to the frontend directory:**
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

4. **Open your browser:**
   Navigate to `http://localhost:3000`

The React app will automatically proxy API requests to the FastAPI backend running on port 8000.

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (not recommended)

## API Integration

The frontend communicates with the FastAPI backend through the API service layer (`src/services/api.js`). Key endpoints:

- **Authentication:**
  - `POST /auth/register` - User registration
  - `POST /auth/token` - User login
  - `GET /auth/verify-email` - Email verification

- **Todos:**
  - `GET /todos/` - List user's todos
  - `POST /todos/` - Create new todo
  - `PUT /todos/{id}` - Update todo
  - `DELETE /todos/{id}` - Delete todo

## Authentication Flow

1. **Registration**: User creates account → Email verification required
2. **Email Verification**: User clicks link in email → Account activated
3. **Login**: User logs in → JWT token stored in localStorage
4. **Protected Access**: Token automatically included in API requests
5. **Auto-logout**: Invalid/expired tokens trigger automatic logout

## Component Overview

### LandingPage
- Marketing page with hero section and feature highlights
- Responsive design with call-to-action buttons
- Redirects authenticated users to dashboard

### Login/Register
- Form validation and error handling
- Loading states and success messages
- Automatic redirection after successful authentication

### Dashboard
- Main application interface
- Task creation, editing, and deletion
- Search and filter functionality
- Statistics sidebar with task counts
- Responsive layout with mobile support

### EmailVerification
- Handles email verification tokens from URL parameters
- Shows verification status with appropriate UI feedback
- Redirects to login after successful verification

## Styling

The application uses a custom CSS utility system inspired by Tailwind CSS, providing:

- Consistent color palette and typography
- Responsive design utilities
- Component-based styling
- Smooth transitions and hover effects

## Environment Configuration

The frontend is configured to work with:
- **Development API**: `http://localhost:8000`
- **Production API**: Configure in `src/services/api.js`

## Building for Production

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Serve the built files:**
   The `build` folder contains the production-ready files that can be served by any static file server.

## Troubleshooting

### Common Issues

1. **API Connection Errors:**
   - Ensure FastAPI backend is running on port 8000
   - Check CORS configuration in backend

2. **Authentication Issues:**
   - Clear localStorage if experiencing login problems
   - Verify email before attempting to login

3. **Build Issues:**
   - Delete `node_modules` and run `npm install` again
   - Ensure Node.js version is 16+

### Development Tips

- Use browser dev tools to inspect network requests
- Check console for error messages
- Use React Developer Tools extension for debugging

## Contributing

1. Follow the existing code style and component structure
2. Add proper error handling and loading states
3. Ensure responsive design for all new components
4. Test authentication flows thoroughly

## License

This project is part of the TaskMaster application suite.

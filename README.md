# 🚀 IQAutoJobs - Modern Job Platform

A comprehensive job platform built with modern technologies, connecting talented professionals with top companies worldwide.

## ✨ Technology Stack

### 🎯 Frontend
- **⚡ Next.js 15** - React framework with App Router
- **📘 TypeScript 5** - Type-safe JavaScript
- **🎨 Tailwind CSS 4** - Utility-first CSS framework
- **🧩 shadcn/ui** - High-quality, accessible components
- **🎯 Lucide React** - Beautiful icon library
- **🔄 TanStack Query** - Data synchronization
- **🐻 Zustand** - State management

### 🚀 Backend
- **⚡ FastAPI** - Modern, fast web framework
- **🐍 Python 3.11** - Robust programming language
- **🗄️ SQLAlchemy** - SQL toolkit and ORM
- **🐘 PostgreSQL** - Powerful open source database
- **🔐 JWT Authentication** - Secure token-based auth
- **⚡ Redis** - In-memory data structure store

### 🛠️ DevOps & Deployment
- **🐳 Docker** - Containerization
- **🚀 Railway** - Cloud deployment platform
- **☁️ Cloudflare R2** - Object storage
- **🔍 SEO Optimized** - Sitemap, robots.txt, structured data

## 🎯 Features

### 👥 User Management
- **Multi-role System**: Candidates, Employers, and Administrators
- **Secure Authentication**: JWT-based with refresh tokens
- **Profile Management**: Complete user profiles with skills and experience
- **Resume Upload**: File storage with Cloudflare R2

### 🏢 Company Management
- **Company Profiles**: Detailed company information and branding
- **Job Posting**: Create and manage job listings
- **Application Management**: Review and manage candidate applications
- **Analytics Dashboard**: Track job performance and applicant metrics

### 💼 Job Platform
- **Advanced Search**: Search by title, location, category, and skills
- **Job Filters**: Comprehensive filtering options
- **Application Tracking**: Real-time application status updates
- **Saved Jobs**: Bookmark interesting opportunities

### 📊 Admin Panel
- **System Dashboard**: Overview of platform statistics
- **User Management**: Manage all user accounts and roles
- **Content Moderation**: Monitor and manage platform content
- **Audit Logs**: Complete activity tracking and compliance

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/iqautojobs.git
cd iqautojobs
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up the frontend**
```bash
cd ..
npm install
```

4. **Configure environment variables**
```bash
# Backend (.env)
DATABASE_URL=postgresql://username:password@localhost/iqautojobs
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=your-super-secret-jwt-key
ENVIRONMENT=development

# Cloudflare R2 (Required)
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key-id
R2_SECRET_ACCESS_KEY=your-r2-secret-access-key
R2_BUCKET=your-r2-bucket-name
R2_PUBLIC_BASE=your-r2-public-base-url

# Frontend (.env.local)
# The custom server in `server.ts` uses the BACKEND_URL variable to proxy API requests.
# Ensure this is set correctly for your local environment.
BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. **Set up the database**
```bash
# Create database and run migrations
cd backend
python -c "from app.db.base import Base, engine; Base.metadata.create_all(engine)"
```

6. **Create sample data (optional)**
```bash
cd backend
python create_sample_data.py
```

7. **Start the development servers**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
npm run dev
```

8. **Open your browser**
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Using Docker

1. **Development with Docker Compose**
```bash
docker-compose up -d
```

2. **Production Build**
```bash
# Build frontend
npm run build

# Build backend
cd backend
docker build -t iqautojobs-backend .

# Run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 Project Structure

```
iqautojobs/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── core/              # Core configuration
│   │   ├── db/                # Database models
│   │   ├── domain/            # Pydantic schemas
│   │   ├── repositories/      # Data access layer
│   │   └── services/          # Business logic
│   ├── main.py               # Application entry point
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Backend container
├── src/                      # Next.js frontend
│   ├── app/                  # App Router pages
│   ├── components/           # React components
│   ├── hooks/                # Custom hooks
│   └── lib/                  # Utilities
├── docker-compose.yml        # Development environment
├── Dockerfile               # Frontend container
└── README.md               # This file
```

## 🌟 Key Components

### 🔐 Authentication System
- JWT-based authentication with refresh tokens
- Role-based access control (Candidate, Employer, Admin)
- Secure password hashing
- Session management

### 📊 Repository Pattern
- Clean separation of concerns
- Testable data access layer
- Consistent error handling
- Transaction management

### 🎨 UI Components
- Modern, responsive design
- Accessible components with ARIA support
- Dark/light theme support
- Mobile-first approach

### 🔄 API Design
- RESTful API endpoints
- Comprehensive error handling
- Request validation with Pydantic
- Rate limiting and security

## 🚀 Deployment

### Railway Deployment

This application is deployed as a single container on Railway. The following environment variables **must be set** in the Railway project settings for the application to start correctly.

#### **Required Environment Variables**

The backend will fail to start if these variables are not provided:

- `DATABASE_URL`: This is typically managed by Railway when you provision a PostgreSQL database.
- `JWT_SECRET_KEY`: A long, random, and secret string used for signing authentication tokens.
- `R2_ACCOUNT_ID`: Your Cloudflare R2 account ID.
- `R2_ACCESS_KEY_ID`: Your Cloudflare R2 access key ID.
- `R2_SECRET_ACCESS_KEY`: Your Cloudflare R2 secret access key.
- `R2_BUCKET`: The name of your R2 bucket.
- `R2_PUBLIC_BASE`: The public base URL for your R2 bucket.

#### **Optional Environment Variables**

These variables have default values but can be customized:

- `ENVIRONMENT`: Set to `production` for deployed environments.
- `DEBUG`: Set to `False` in production.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Defaults to `30`.
- `REFRESH_TOKEN_EXPIRE_DAYS`: Defaults to `7`.
- `GOOGLE_OAUTH_CLIENT_ID`: For enabling Google Sign-In.
- `GOOGLE_OAUTH_CLIENT_SECRET`: For enabling Google Sign-In.

### Manual Deployment

1. **Build Frontend**
```bash
npm run build
```

2. **Deploy Backend**
```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Configure Reverse Proxy**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost/iqautojobs
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=your-super-secret-jwt-key
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000

# Cloudflare R2 (Required)
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key-id
R2_SECRET_ACCESS_KEY=your-r2-secret-access-key
R2_BUCKET=your-r2-bucket-name
R2_PUBLIC_BASE=your-r2-public-base-url
```

#### Frontend (.env.local)
```env
# Note: For the custom server, you may need to set BACKEND_URL
# See server.ts for more details.
BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 📊 Monitoring & Analytics

### Application Monitoring
- Error tracking with Sentry (optional)
- Performance monitoring
- User activity analytics
- System health checks

### Database Monitoring
- Query performance tracking
- Connection pool monitoring
- Backup and recovery procedures

## 🔒 Security Features

- **Authentication**: JWT with refresh tokens
- **Authorization**: Role-based access control
- **Input Validation**: Comprehensive data validation
- **Rate Limiting**: API endpoint protection
- **CORS**: Cross-origin resource sharing
- **Security Headers**: HTTP security headers
- **Data Encryption**: Sensitive data protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the [documentation](docs/)
- Join our community discussions

---

Built with ❤️ for the job-seeking community. Connecting talent with opportunity. 🚀

# Pro Prime Series Systems LLC Website

A professional CMS-driven website for Pro Prime Series Systems LLC, showcasing their ecosystem of technologies and subsystems.

## 🚀 Tech Stack

- **Frontend**: React + Vite, TailwindCSS, Framer Motion
- **Backend**: FastAPI, SQLAlchemy, JWT Authentication
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Docker, Fly.io, Render compatible

## 📋 Features

- Modern, enterprise-grade design with futuristic accents
- Fully responsive layout
- CMS admin panel for content management
- JWT authentication for admin access
- CRUD operations for subsystems, social links, and pages
- 14 subsystem pages with detailed information
- Social media integration
- Dark theme optimized UI

## 🏗️ Project Structure

```
pro-prime-website/
├── backend/           # FastAPI application
├── frontend/          # React application
├── docker-compose.yml # Docker composition
├── Dockerfile.*       # Docker configurations
└── README.md
```

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pro-prime-website.git
   cd pro-prime-website
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   python seed.py  # Seed the database
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Admin Login: http://localhost:3000/login (admin/changeme123)

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed the database
docker-compose exec backend python seed.py
```

## 🚢 Deployment Options

### Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch the application
fly launch
fly deploy
```

### Render

1. Push code to GitHub
2. Connect repository to Render
3. Use provided `render.yaml` for infrastructure as code
4. Deploy automatically

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway up
```

## 🔐 Admin Access

Default credentials (change in production):
- Username: `admin`
- Password: `changeme123`

## 📝 API Endpoints

### Public Endpoints
- `GET /api/systems` - List all subsystems
- `GET /api/systems/{slug}` - Get specific subsystem
- `GET /api/social` - List social media links
- `GET /api/pages/{name}` - Get page content

### Admin Endpoints (JWT Protected)
- `POST /api/systems` - Create subsystem
- `PUT /api/systems/{id}` - Update subsystem
- `DELETE /api/systems/{id}` - Delete subsystem
- `POST /api/social` - Create social link
- `PUT /api/social/{id}` - Update social link
- `DELETE /api/social/{id}` - Delete social link
- `PUT /api/pages/{id}` - Update page content

### Auth Endpoints
- `POST /api/auth/login` - Get JWT token
- `POST /api/auth/refresh` - Refresh access token

## 🎨 Subsystems

1. True Mark Mint
2. Alpha CertSig Mint
3. GOAT
4. APEX Doc
5. Vault Forge
6. CALI Cognitive Systems
7. Kay Gee 1.0
8. Cali X One
9. ECM
10. UCM
11. Caleon 4 Core
12. Orb Assistant
13. CALI ORB
14. Orb-UI

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configured for production
- Environment variables for sensitive data
- SQL injection protection via SQLAlchemy
- XSS protection via React

## 📦 Production Considerations

1. Change default admin credentials
2. Set strong SECRET_KEY
3. Use PostgreSQL instead of SQLite
4. Enable HTTPS
5. Configure proper CORS origins
6. Set up database backups
7. Monitor with logging
8. Use CDN for static assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

Copyright © 2024 Pro Prime Series Systems LLC. All rights reserved.

## 🆘 Support

For support, email info@spruked.com or visit https://spruked.com
# 🕉️ Punyaka MVP - Spiritual Services Platform

A full-stack platform for priest booking, consultations, and spiritual e-commerce built with Django, Next.js, and PostgreSQL.

## 🚀 Quick Start (One Command!)

```bash
docker-compose up --build
```

Then visit **http://localhost:3000** 🎉

### Access Points
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Django Admin:** http://localhost:8000/admin
- **API Docs:** http://localhost:8000/api/swagger/

## 👥 Demo Credentials

### Admin
- Email: `admin@punyaka.com`
- Password: `admin123`

### Priests
- Email: `priest1@punyaka.com` / Password: `priest123`
- Email: `priest2@punyaka.com` / Password: `priest123`

### Customers
- Email: `customer1@punyaka.com` / Password: `customer123`
- Email: `customer2@punyaka.com` / Password: `customer123`

## 📦 What's Included

### Working Features
- ✅ User Authentication (Login/Signup)
- ✅ Role-based access (Customer, Priest, Admin)
- ✅ Priest Listings with verification status
- ✅ Priest Booking System
- ✅ E-commerce (Products, Cart, Checkout)
- ✅ Admin Dashboard (Priest Verification, Product Management)
- ✅ Demo Data (Users, Priests, Products, Bookings)

### Tech Stack
- **Frontend**: Next.js 14 + Tailwind CSS
- **Backend**: Django 5 + Django REST Framework
- **Database**: PostgreSQL 15
- **Containerization**: Docker + Docker Compose

## 🛠️ Development

### Backend Commands
```bash
# Enter backend container
docker-compose exec backend sh

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Load demo data
python manage.py loaddata demo_data.json
```

### Frontend Commands
```bash
# Enter frontend container
docker-compose exec frontend sh

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📁 Project Structure

```
punyaka-mvp/
├── backend/           # Django REST API
│   ├── core/          # Authentication & User models
│   ├── bookings/      # Priest booking system
│   ├── ecommerce/     # Products & Orders
│   └── manage.py
├── frontend/          # Next.js React app
│   ├── pages/         # Routes
│   ├── components/    # React components
│   └── services/      # API clients
└── docker-compose.yml
```

## 🔧 Configuration

Environment variables are set in `docker-compose.yml` for demo purposes.
For production, use proper `.env` files and secure secrets.

## 📝 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/swagger/
- ReDoc: http://localhost:8000/api/redoc/

## 🎯 Next Steps

1. Integrate payment gateway (Razorpay)
2. Add WebRTC for consultations
3. Implement horoscope module
4. Add digital library
5. Set up CI/CD pipeline

# 🕉️ Punyaka MVP - Quick Setup Guide

## Prerequisites
- Docker Desktop installed and running
- Git (optional, for version control)

## Quick Start (Under 5 minutes)

### 1. Start the Application
```bash
cd /workspaces/codespaces-blank
docker-compose up --build
```

This will:
- Build the Django backend
- Build the Next.js frontend
- Start PostgreSQL database
- Load demo data automatically
- Create admin user

### 2. Access the Application

**Frontend (Main App):** http://localhost:3000
**Backend API:** http://localhost:8000/api
**Django Admin:** http://localhost:8000/admin
**API Documentation:** http://localhost:8000/api/swagger/

### 3. Demo Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@punyaka.com | admin123 |
| **Priest** | priest1@punyaka.com | priest123 |
| **Customer** | customer1@punyaka.com | customer123 |

## What's Working

✅ **Authentication System**
- Login/Signup with email
- Role-based access (Customer, Priest, Admin)
- Session management

✅ **Priest Module**
- Verified priest listings
- Priest profiles with ratings
- Service offerings

✅ **Booking System**
- Browse services
- Book priests for ceremonies
- View booking history

✅ **E-Commerce**
- Product catalog (10+ demo products)
- Shopping cart
- Checkout process
- Order history

✅ **Admin Dashboard**
- Priest verification workflow
- Product management
- Order management
- Django admin panel

## Demo Data Included

### Users
- 1 Admin user
- 3 Verified Priests (with profiles, ratings)
- 3 Customer users

### Products
- 10 spiritual products
- Categories: Pooja Samagri, Idols, Incense
- Featured products
- Stock management

### Services
- 6 types of poojas/homas
- Pricing and duration info

## Testing the Features

### Test Customer Journey
1. Go to http://localhost:3000
2. Login as: customer1@punyaka.com / customer123
3. Browse priests at /priests
4. Shop products at /products
5. Add items to cart
6. View dashboard at /dashboard

### Test Priest Features
1. Login as: priest1@punyaka.com / priest123
2. View your bookings
3. See your profile information

### Test Admin Features
1. Login as: admin@punyaka.com / admin123
2. Access Django admin: http://localhost:8000/admin
3. Verify priests
4. Manage products
5. View all bookings and orders

## API Endpoints

### Authentication
- POST `/api/auth/login/` - Login
- POST `/api/auth/register/` - Register
- POST `/api/auth/logout/` - Logout
- GET `/api/auth/me/` - Current user

### Priests
- GET `/api/priests/` - List verified priests
- GET `/api/priests/{id}/` - Priest detail

### Services
- GET `/api/services/` - List services
- GET `/api/services/{id}/` - Service detail

### Bookings
- GET `/api/bookings/` - User's bookings
- POST `/api/bookings/` - Create booking
- POST `/api/bookings/{id}/confirm/` - Confirm booking
- POST `/api/bookings/{id}/complete/` - Mark complete
- POST `/api/bookings/{id}/rate/` - Rate service

### Products
- GET `/api/products/` - List products
- GET `/api/products/{id}/` - Product detail
- GET `/api/categories/` - Product categories

### Cart
- GET `/api/cart/` - Get cart
- POST `/api/cart/add_item/` - Add to cart
- POST `/api/cart/update_item/` - Update quantity
- POST `/api/cart/remove_item/` - Remove item
- POST `/api/cart/clear/` - Clear cart

### Orders
- GET `/api/orders/` - User's orders
- POST `/api/orders/checkout/` - Create order

## Troubleshooting

### Port Already in Use
```bash
# Stop other services using ports 3000, 8000, or 5432
docker-compose down
```

### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild Everything
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## Stop the Application

```bash
docker-compose down
```

To also remove volumes (database data):
```bash
docker-compose down -v
```

## Development

### Backend Development
```bash
# Enter backend container
docker-compose exec backend sh

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### Frontend Development
```bash
# Enter frontend container
docker-compose exec frontend sh

# Install new packages
npm install <package-name>
```

## Next Steps for Production

1. **Security**
   - Change SECRET_KEY
   - Set DEBUG=False
   - Use environment variables for secrets
   - Configure ALLOWED_HOSTS

2. **Payment Integration**
   - Integrate Razorpay
   - Implement split payment logic

3. **Additional Features**
   - Email notifications
   - SMS OTP authentication
   - Google Maps integration
   - Real-time slot availability
   - WebRTC for consultations

4. **Deployment**
   - Frontend: Vercel/Netlify
   - Backend: Render/Railway
   - Database: Neon/Supabase
   - Setup CI/CD pipeline

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Rebuild: `docker-compose up --build`
- Reset: `docker-compose down -v && docker-compose up --build`

---

**Built with:** Django 5.0, Next.js 14, PostgreSQL, Tailwind CSS, Docker

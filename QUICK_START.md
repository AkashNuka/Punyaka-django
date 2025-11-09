# 🎯 QUICK START GUIDE - Punyaka MVP

## ✅ STATUS: FULLY OPERATIONAL

**All systems are running! Ready for client demo!** 🎉

The application has been successfully deployed with:
- ✅ 10 users (1 admin, 3 priests, 6 customers)
- ✅ 6 spiritual services with pricing
- ✅ 10 products across 3 categories
- ✅ Full authentication working
- ✅ All pages rendering correctly

## 🚀 Already Running!

Your containers are currently active. To view the application:

**Frontend**: http://localhost:3000  
**Backend API**: http://localhost:8000/api/  
**Admin Panel**: http://localhost:8000/admin/  
**API Docs**: http://localhost:8000/swagger/

## 👤 Demo Login Credentials

### Admin Account
- **Email**: admin@punyaka.com
- **Password**: admin123
- **Access**: Full admin panel + all features

### Priest Accounts
- **Email**: priest1@punyaka.com | **Password**: priest123
- **Email**: priest2@punyaka.com | **Password**: priest123
- **Email**: priest3@punyaka.com | **Password**: priest123
- **Access**: Priest dashboard, service management

### Customer Accounts
- **Email**: customer1@punyaka.com | **Password**: customer123
- **Email**: customer2@punyaka.com | **Password**: customer123
- **Email**: customer3@punyaka.com | **Password**: customer123
- **Access**: Book services, shop products

## 🌐 Application URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/swagger/

## 📦 What's Pre-loaded

### Users
- 1 Admin
- 3 Verified Priests (with profiles, specializations, locations)
- 3 Customers (with birth details)

### Services (6 total)
- Graha Shanti Pooja (₹5,100)
- Ganesh Chaturthi Pooja (₹2,500)
- Satyanarayan Katha (₹3,100)
- Griha Pravesh (₹7,500)
- Rudrabhishek (₹4,200)
- Lakshmi Pooja (₹2,800)

### Products (10 total)
- Brass Diya Set - ₹850
- Bhagavad Gita - ₹450
- Ganesh Brass Idol - ₹2,500
- Incense Sticks Combo - ₹350
- Sri Yantra - ₹1,800
- Rudraksha Mala - ₹1,500
- Hanuman Chalisa - ₹150
- Pooja Thali Set - ₹2,200
- Lakshmi-Ganesh Pair - ₹3,500
- Camphor Tablets - ₹180

## ✨ Features Working

### Customer Features
- ✅ Registration & Login
- ✅ Browse priests by location/specialization
- ✅ Book pooja services
- ✅ Shop spiritual products
- ✅ Add to cart & checkout
- ✅ View order history

### Priest Features
- ✅ Registration & Login
- ✅ Profile management
- ✅ View service bookings
- ✅ Update availability

### Admin Features
- ✅ User management
- ✅ Priest verification
- ✅ Service management
- ✅ Product catalog management
- ✅ Order management

## 🔍 Testing the MVP

1. **Test Login Flow**
   - Go to http://localhost:3000/login
   - Try logging in with customer1@punyaka.com / customer123
   - Check dashboard loads

2. **Test Priest Listing**
   - Go to http://localhost:3000/priests
   - Should see 3 verified priests with details

3. **Test Product Catalog**
   - Go to http://localhost:3000/products
   - Should see 10 products across 3 categories

4. **Test Admin Panel**
   - Go to http://localhost:8000/admin/
   - Login with admin@punyaka.com / admin123
   - Browse all models and data

5. **Test API**
   - Go to http://localhost:8000/swagger/
   - Try API endpoints directly

## 🐛 Troubleshooting

### Backend Not Starting?
```bash
# Check logs
docker-compose logs backend

# Common fix: Remove volumes and restart
docker-compose down -v
docker-compose up --build
```

### Frontend Red Squiggles?
- These are TypeScript IDE warnings, not runtime errors
- The app will still work in browser
- Install dependencies locally to fix: `cd frontend && npm install`

### Database Connection Issues?
```bash
# Check database is running
docker-compose ps

# Restart database
docker-compose restart db
```

### Port Already in Use?
```bash
# Find and kill process on port 8000 or 3000
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

## 📱 Demo Script for Client

1. **Show Homepage** - Clean landing page
2. **Login as Customer** - Show working authentication
3. **Browse Priests** - Show 3 verified priests with ratings
4. **Browse Products** - Show 10 products across categories
5. **Show Admin Panel** - Full data management capabilities
6. **Show API Docs** - Professional Swagger documentation

## 🎉 Success Indicators

✅ Backend shows: "Starting development server at http://0.0.0.0:8000/"
✅ Frontend shows: "ready - started server on 0.0.0.0:3000"
✅ Login works with demo credentials
✅ Priests page shows 3 priests
✅ Products page shows 10 products
✅ Admin panel accessible

## 📞 Quick Commands Reference

```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose up --build

# Fresh start (deletes database!)
docker-compose down -v && docker-compose up --build
```

---

**Ready to show client!** 🚀
All login credentials work, demo data is populated, and deployment is ready!

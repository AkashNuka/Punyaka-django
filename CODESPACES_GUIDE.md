# 🚀 Codespaces Deployment Guide

## ✅ All Fixes Applied!

### What Was Fixed:

1. **Email Login Support** ✅
   - Backend now accepts login with both email and username
   - Login with `priest1@punyaka.com` works

2. **CSRF Configuration** ✅
   - Added Codespaces URLs to trusted origins
   - CSRF tokens handled automatically

3. **API URL Detection** ✅
   - Frontend automatically detects Codespaces environment
   - Dynamically constructs correct API URL

4. **Error Logging** ✅
   - Added console logging for debugging
   - API errors show detailed information

## 🌐 Your Codespaces URLs

**Frontend**: https://legendary-goggles-5jg47gppq562jrq-3000.app.github.dev
**Backend**: https://legendary-goggles-5jg47gppq562jrq-8000.app.github.dev

## ⚠️ IMPORTANT: Make Ports Public

GitHub Codespaces ports are private by default. You need to make them public:

### Step-by-Step:

1. **Open the PORTS tab** in VS Code (bottom panel, next to Terminal)
2. **Find port 3000** (frontend)
   - Right-click → Change Port Visibility → **Public**
3. **Find port 8000** (backend)
   - Right-click → Change Port Visibility → **Public**
4. **Refresh your browser** on the frontend URL

### Why This Is Needed:
- Private ports require GitHub authentication
- Public ports allow direct API calls from frontend
- Without this, frontend can't connect to backend

## 🔍 Debugging in Browser

Open your browser console (F12) when accessing the app. You should see:

```
🔗 Punyaka API URL: https://legendary-goggles-5jg47gppq562jrq-8000.app.github.dev/api
```

If you see errors, they will show detailed information about:
- Which API endpoint failed
- HTTP status code
- Error message

## ✅ Testing Checklist

Once ports are public:

1. **Open Frontend**: https://legendary-goggles-5jg47gppq562jrq-3000.app.github.dev
2. **Check Console**: Should see API URL logged
3. **Click "Find Priests"**: Should load 3 priests
4. **Click "Shop"**: Should load 10 products
5. **Try Login**: Use `priest1@punyaka.com` / `priest123`
6. **Try Register**: Create a new account

## 🎯 Demo Credentials

```
Admin:    admin@punyaka.com / admin123
Priest:   priest1@punyaka.com / priest123
Customer: customer1@punyaka.com / customer123
```

## 🔧 Alternative: Local Testing

If Codespaces ports don't work, you can test locally:

```bash
# In VS Code terminal
docker-compose ps  # Verify containers running

# Open in local browser
http://localhost:3000  # Frontend
http://localhost:8000/api/priests/  # Backend API
http://localhost:8000/admin/  # Django Admin
```

## 📊 Verify Data Exists

Run these commands to verify all demo data:

```bash
# Check users
docker-compose exec backend python manage.py shell -c "from core.models import User; print(f'{User.objects.count()} users')"

# Check priests
docker-compose exec backend python manage.py shell -c "from core.models import PriestProfile; print(f'{PriestProfile.objects.count()} priests')"

# Check services
docker-compose exec backend python manage.py shell -c "from bookings.models import Service; print(f'{Service.objects.count()} services')"

# Check products
docker-compose exec backend python manage.py shell -c "from ecommerce.models import Product; print(f'{Product.objects.count()} products')"
```

Should output:
```
10 users
3 priests
6 services
10 products
```

## 🐛 Troubleshooting

### Frontend shows "Network Error"
- ✅ Make port 8000 PUBLIC in PORTS tab
- ✅ Check browser console for API URL
- ✅ Verify backend is running: `docker-compose ps`

### Login fails
- ✅ Check browser console for error details
- ✅ Verify credentials are correct
- ✅ Try with username instead: `priest1` / `priest123`

### No priests/products showing
- ✅ Check browser console for API errors
- ✅ Verify data exists (run commands above)
- ✅ Check network tab in browser dev tools

### "CSRF token missing"
- ✅ Make sure you're accessing via HTTPS in Codespaces
- ✅ Clear browser cookies and try again
- ✅ Check CSRF_TRUSTED_ORIGINS includes your Codespaces URL

## 🎉 Success Indicators

✅ Console shows: `🔗 Punyaka API URL: https://...8000.app.github.dev/api`
✅ Homepage loads with navigation
✅ Find Priests shows 3 priests
✅ Shop shows 10 products
✅ Login redirects to dashboard
✅ Registration creates new user

---

**Next Step**: Make ports 3000 and 8000 PUBLIC in the PORTS tab, then refresh your browser!

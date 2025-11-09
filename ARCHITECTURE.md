# 🏗️ Punyaka MVP Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                           │
│                      http://localhost:3000                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        FRONTEND (Next.js)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Pages: Home, Login, Register, Priests, Products,        │  │
│  │         Dashboard, Cart                                   │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  Components: Layout, Navigation, Forms                    │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  Context: AuthContext (user state)                        │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  Services: API client (axios)                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                    Port 3000 (Docker)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST API
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      BACKEND (Django REST)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Apps:                                                    │  │
│  │  ├─ core/        - Users, Auth, Priest Profiles         │  │
│  │  ├─ bookings/    - Services, Bookings                    │  │
│  │  └─ ecommerce/   - Products, Cart, Orders               │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  API Endpoints (25+):                                     │  │
│  │  ├─ /api/auth/   - Authentication                        │  │
│  │  ├─ /api/priests/- Priest listings                       │  │
│  │  ├─ /api/bookings/ - Booking management                  │  │
│  │  ├─ /api/products/ - Product catalog                     │  │
│  │  ├─ /api/cart/   - Shopping cart                         │  │
│  │  └─ /api/orders/ - Order processing                      │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  Admin Panel: /admin                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                    Port 8000 (Docker)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ PostgreSQL Protocol
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     DATABASE (PostgreSQL)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Tables:                                                  │  │
│  │  ├─ core_user            - Users (all roles)            │  │
│  │  ├─ core_priestprofile   - Priest profiles             │  │
│  │  ├─ bookings_service     - Service catalog             │  │
│  │  ├─ bookings_booking     - Bookings                    │  │
│  │  ├─ ecommerce_category   - Product categories          │  │
│  │  ├─ ecommerce_product    - Products                    │  │
│  │  ├─ ecommerce_cart       - Shopping carts              │  │
│  │  ├─ ecommerce_cartitem   - Cart items                  │  │
│  │  ├─ ecommerce_order      - Orders                      │  │
│  │  └─ ecommerce_orderitem  - Order items                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                    Port 5432 (Docker)                            │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### User Authentication Flow
```
User Browser
    │
    ├─→ POST /api/auth/login/
    │        {username, password}
    │
    └─→ Django Authentication
            │
            ├─→ Validate credentials
            ├─→ Create session
            └─→ Return user data
                    │
                    └─→ Store in AuthContext
                            │
                            └─→ Redirect to dashboard
```

### Booking Flow
```
Customer                    Backend                    Database
   │                           │                           │
   ├─→ Browse priests          │                           │
   │   GET /api/priests/       │                           │
   │                           ├─→ Query priestprofile     │
   │                           │   WHERE is_verified=true  │
   │   ←─────────────────────┤                           │
   │   (List of priests)       │                           │
   │                           │                           │
   ├─→ Create booking          │                           │
   │   POST /api/bookings/     │                           │
   │   {priest, service, ...}  │                           │
   │                           ├─→ Create booking record   │
   │                           │   25% advance payment     │
   │   ←─────────────────────┤   Payment status: partial │
   │   (Booking created)       │                           │
   │                           │                           │
Priest                         │                           │
   │                           │                           │
   ├─→ Confirm booking         │                           │
   │   POST /api/bookings/1/   │                           │
   │        confirm/           │                           │
   │                           ├─→ Update status:          │
   │                           │   confirmed               │
```

### E-Commerce Flow
```
Customer                    Backend                    Database
   │                           │                           │
   ├─→ Browse products         │                           │
   │   GET /api/products/      │                           │
   │                           ├─→ Query products          │
   │   ←─────────────────────┤   WHERE is_active=true    │
   │                           │                           │
   ├─→ Add to cart             │                           │
   │   POST /api/cart/         │                           │
   │        add_item/          │                           │
   │                           ├─→ Get/Create cart         │
   │                           ├─→ Create cart item        │
   │   ←─────────────────────┤                           │
   │                           │                           │
   ├─→ Checkout                │                           │
   │   POST /api/orders/       │                           │
   │        checkout/          │                           │
   │                           ├─→ Create order            │
   │                           ├─→ Create order items      │
   │                           ├─→ Update stock            │
   │                           ├─→ Clear cart              │
   │   ←─────────────────────┤                           │
   │   (Order created)         │                           │
```

## Component Relationships

### User Model Hierarchy
```
User (core_user)
├─ Customer (role='customer')
├─ Priest (role='priest')
│  └─ PriestProfile (one-to-one)
│     ├─ specializations
│     ├─ experience_years
│     ├─ is_verified
│     └─ average_rating
└─ Admin (role='admin')
```

### E-Commerce Models
```
Category
└─ Products (many)
   ├─ Product details
   ├─ Stock
   └─ Pricing

User
└─ Cart (one-to-one)
   └─ CartItems (many)
      └─ Product reference

User
└─ Orders (many)
   └─ OrderItems (many)
      └─ Product snapshot
```

### Booking Models
```
Service (catalog)
├─ name
├─ duration
└─ base_price

Booking
├─ Customer (FK to User)
├─ Priest (FK to PriestProfile)
├─ Service (FK to Service)
├─ date & time
├─ status workflow
└─ payment split (25/75)
```

## Technology Stack

### Frontend
```
Next.js 14
├─ React 18
├─ TypeScript
├─ Tailwind CSS
├─ Axios (API client)
└─ React Context (state management)
```

### Backend
```
Django 5.0
├─ Django REST Framework
├─ PostgreSQL (psycopg2)
├─ CORS Headers
├─ drf-yasg (API docs)
└─ Django Admin
```

### DevOps
```
Docker Compose
├─ Backend container (Python)
├─ Frontend container (Node)
└─ Database container (PostgreSQL)
```

## Security Layers

```
┌─────────────────────────────────────┐
│  Frontend Validation                │
│  ├─ Form validation                 │
│  └─ Client-side checks              │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│  Django Middleware                  │
│  ├─ CORS validation                 │
│  ├─ CSRF protection                 │
│  └─ Session management              │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│  Django ORM                         │
│  ├─ SQL injection protection        │
│  ├─ Query parameterization          │
│  └─ Type validation                 │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│  PostgreSQL                         │
│  └─ Data persistence                │
└─────────────────────────────────────┘
```

## API Architecture

### RESTful Endpoints
```
Authentication
├─ POST   /api/auth/register/
├─ POST   /api/auth/login/
├─ POST   /api/auth/logout/
└─ GET    /api/auth/me/

Priests
├─ GET    /api/priests/
├─ GET    /api/priests/{id}/
└─ GET    /api/priests/{id}/availability/

Bookings
├─ GET    /api/bookings/
├─ POST   /api/bookings/
├─ GET    /api/bookings/{id}/
├─ POST   /api/bookings/{id}/confirm/
├─ POST   /api/bookings/{id}/complete/
├─ POST   /api/bookings/{id}/rate/
└─ POST   /api/bookings/{id}/cancel/

Products
├─ GET    /api/products/
├─ GET    /api/products/{id}/
└─ GET    /api/categories/

Cart
├─ GET    /api/cart/
├─ POST   /api/cart/add_item/
├─ POST   /api/cart/update_item/
├─ POST   /api/cart/remove_item/
└─ POST   /api/cart/clear/

Orders
├─ GET    /api/orders/
├─ GET    /api/orders/{id}/
└─ POST   /api/orders/checkout/
```

## Deployment Architecture (Future)

```
┌──────────────────────┐
│  Vercel (Frontend)   │
│  - Next.js app       │
│  - Static assets     │
│  - CDN               │
└──────────┬───────────┘
           │
           ├─→ API calls
           │
┌──────────▼───────────┐
│  Render (Backend)    │
│  - Django REST API   │
│  - Gunicorn          │
│  - WhiteNoise        │
└──────────┬───────────┘
           │
           ├─→ Database queries
           │
┌──────────▼───────────┐
│  Neon/Supabase       │
│  - PostgreSQL        │
│  - Automated backups │
│  - Connection pool   │
└──────────────────────┘
```

## Scaling Considerations

### Current (MVP)
- Single server setup
- ~100 concurrent users
- ~1000 requests/minute

### Future Scaling
```
Load Balancer
├─ Frontend Cluster (Vercel CDN)
│  ├─ Region: US
│  ├─ Region: EU
│  └─ Region: Asia
│
├─ Backend Cluster
│  ├─ Web Server 1
│  ├─ Web Server 2
│  └─ Web Server N
│
├─ Redis Cache
│  └─ Session store
│
└─ Database
   ├─ Primary (write)
   └─ Replicas (read)
```

---

**This architecture supports:**
- ✅ 3 user roles (Customer, Priest, Admin)
- ✅ RESTful API design
- ✅ Modular code structure
- ✅ Easy to scale horizontally
- ✅ Docker-based deployment
- ✅ Clear separation of concerns

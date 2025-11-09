# 🕉️ Punyaka MVP Specification

### Version: 1.0
**Document Date:** November 2025  
**Purpose:** Copilot-ready MVP spec for the Punyaka Spiritual Services Platform

---

## ⚙️ Tech Stack

| Layer | Technology | Notes |
|--------|-------------|--------|
| Frontend | React (Next.js + Tailwind CSS) | SEO-friendly, fast, deploy to Vercel |
| Backend | Django REST Framework (Python) | API-first backend with admin support |
| Database | PostgreSQL | Use on Render, Supabase, or Neon |
| Auth | Django AllAuth + Twilio/Firebase OTP + OAuth | Multi-factor login for all roles |
| Payment | Razorpay Split Payments | 25%-75% mandate for Priest Booking |
| Video/Audio | WebRTC (Jitsi SDK / Agora) | For online consultations |
| Notifications | Firebase Cloud Messaging (FCM) | Daily horoscope + status alerts |
| DRM/Content | Cloudflare Stream / Vimeo API | Secure video/audio content |
| Hosting | Vercel (Frontend), Render (Backend) | Scalable and low-cost setup |
| Cron Jobs | Celery + Redis | For daily horoscope push |

---

## 🧱 Folder Structure

### Frontend (`/frontend`)
```
/frontend
 ├── pages/
 ├── components/
 ├── services/
 ├── context/
 ├── hooks/
 ├── public/
 └── styles/
```

### Backend (`/backend`)
```
/backend
 ├── core/
 ├── users/
 ├── bookings/
 ├── consultations/
 ├── ecommerce/
 ├── gifting/
 ├── horoscope/
 ├── digital_library/
 ├── virtual_poojas/
 └── api/
```

---

## 🧩 Core Modules and Requirements

### 1. Core & Authentication
- Roles: `Customer`, `Priest`, `Admin`
- Authentication via:
  - Phone (OTP)
  - Email/Password
  - OAuth (Google/Facebook)
- Store: DOB, Time of Birth, Place of Birth (mandatory for horoscope)
- **Priest Verification Pipeline:**
  - Requires Aadhaar, PAN, Bank Details upload
  - Admin verification → sets `is_verified = True`
  - Only verified priests visible in listings

---

### 2. Priest Booking System
**Purpose:** Physical pooja/homa booking at customer’s location  
**Payment Model:** 25% upfront, 75% after completion  

**Features:**
- Dynamic slot engine → service duration + 15min buffer + Google Maps travel time
- Google Maps Distance Matrix API for travel buffer
- Split payment architecture via Razorpay
- Service closure flow:
  - Priest submits completion checklist
  - Customer confirms → triggers balance payment + optional Dakshina
  - Rating + feedback required post-service

**Endpoints Example:**
```
POST /bookings/create/
GET /bookings/user/:id/
PATCH /bookings/:id/status/
```

---

### 3. Consultation Services
**Purpose:** Online/Offline advisory sessions (Astrology, Remedies, Vastu)

**Features:**
- Online: WebRTC video/audio call  
- Offline: GPS check-in for priest  
- 100% payment upfront  
- Refund logic: 50% refund if canceled <48 hrs before slot  

**Endpoints:**
```
POST /consultation/request/
GET /consultation/history/
POST /consultation/complete/
```

---

### 4. E-Commerce & Bundled Services

#### E-Commerce (Samagri & Gifting)
- Inventory logic:
  - Kit stock = min(stock of all items)
  - Buying a Kit → decrement all component items
- Custom Quote Flow:
  - Upload Image → Admin creates manual quote (temporary product)
- Gift Options:
  - Gift Wrap (paid add-on)
  - Gift Message (free text)

**Endpoints:**
```
GET /products/
POST /cart/add/
POST /checkout/
```

#### Bundled Service (Priest + Samagri)
- Unified checkout:
  - Combine 25% priest payment + 100% samagri price
- Triggers:
  - Booking pipeline
  - Samagri delivery pipeline
- Logistics: priority delivery before pooja date

---

### 5. Engagement Modules

#### Horoscope
- Use Vedic Astrology API (e.g., Aztro)
- Cron job → daily personalized horoscope at 7:00 AM
- Push via Firebase Cloud Messaging

**Endpoints:**
```
GET /horoscope/daily/?sign=aries
```

---

#### Digital Library
- Subscription system:
  - Google Play + Apple In-App Purchases
- DRM content:
  - Secure URL/time-limited access for video/audio/ePub
- Categories: Bhajans, Puranas, Yoga, Meditation

---

#### Virtual Poojas & Temple Sevas
- Paid/free live event scheduling
- “Join Stream” button (private URL)
- Daily temple seva report generation for partners
- Option for Prasad delivery tracking

---

## 🧮 Payment Flows

| Type | Upfront | Post-Service | Notes |
|------|----------|---------------|--------|
| Priest Booking | 25% | 75% after confirmation | Split payment logic |
| Consultation | 100% | N/A | Video call / GPS check-in |
| E-Commerce | 100% | N/A | Standard Razorpay checkout |
| Bundled Service | 25% (Priest) + 100% (Samagri) | N/A | Unified checkout |

---

## 🧰 Environment Variables

```
DATABASE_URL=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
FIREBASE_KEY=
GOOGLE_MAPS_API_KEY=
CLOUDFLARE_STREAM_KEY=
ASTROLOGY_API_KEY=
```

---

## 🕓 Project Timeline

| Phase | Modules | Duration |
|--------|----------|-----------|
| Phase 1 | Core + Auth + Priest Booking | 3 weeks |
| Phase 2 | Consultation + E-commerce | 3 weeks |
| Phase 3 | Horoscope + Library + Virtual Poojas | 4 weeks |
| **Total Duration** |  | **10 weeks** |

---

## 🧾 Deliverables
- Full-stack web app (Next.js + Django)
- Admin dashboard for priest verification & product management
- API documentation (Swagger)
- PostgreSQL schema dump
- Dockerized deployment setup
- CI/CD pipeline via GitHub Actions

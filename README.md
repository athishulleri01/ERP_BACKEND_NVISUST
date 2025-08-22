# ERP User & Role Management System

A Role-Based Access Control (RBAC) system for an **ERP platform** built with **Django REST Framework (DRF)**, PostgreSQL, and JWT authentication. This project enables **Admins, Managers, and Employees** to access resources based on their roles.

---
🔗 Frontend (Live): https://erp-frontend-nvisust.vercel.app/

🔗 Backend API (AWS EC2 with SSL & domain): https://www.athishulleri.online/api/

🔗 Frontend git repo: https://github.com/athishulleri01/ERP_FRONTEND_NVISUST.git

## 🚀 Features

* **JWT Authentication** (Login, Logout, Token Refresh)
* **Role-Based Access Control (RBAC)**

  * **Admin**: Full user management (Create, Update, Delete)
  * **Manager**: View all employees, restricted from editing Admins
  * **Employee**: Access only their own profile
* **Secure API Endpoints** with DRF Permissions
* **PostgreSQL Database Schema** for user roles
* **Frontend Deployed on Vercel**
* **Backend Deployed on AWS EC2** with domain & SSL
* **Static Files on Cloudinary**

---

## 📂 Project Structure

```
ERP_BACKEND_NVISUST/
├── authentication/          # Authentication & RBAC logic
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Custom User model with roles
│   ├── permissions.py       # Role-based access permissions
│   ├── serializers.py       # Serializers for User & Auth
│   ├── urls.py              # App-specific routes
│   ├── views.py             # API Views
│
├── config/                  # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Django settings (ENV support)
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py
│
├── manage.py                # Django CLI entry point
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (local)
├── .env.sample              # Example env file
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/athishulleri01/ERP_BACKEND_NVISUST.git
cd ERP_BACKEND_NVISUST
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Copy `.env.sample` to `.env` and configure values:

```env
DJANGO_SECRET_KEY='django-insecure-5%&q=6_*ltvjslaq=$75s0g)0f30mu)*gf4jizbedbsfx+u-s^'
DEBUG=True
POSTGRES_HOST=""
POSTGRES_PORT=""
POSTGRES_DB=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""

```

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Start Server

```bash
python manage.py runserver
```

Backend will run on: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🌐 Deployment

### Backend (AWS EC2)

* Hosted on **Ubuntu 22.04 AWS EC2**
* Gunicorn + Nginx setup with **SSL (Certbot)**
* Domain: `https://www.athishulleri.online`

### Frontend (Vercel)

* React.js frontend deployed on **Vercel**
* Connected to backend API `https://www.athishulleri.online`

### Static Files (Cloudinary)

* Images & static files are served via **Cloudinary CDN**

---

## 🔑 API Endpoints

### Authentication

* `POST /api/auth/register/` → Register a new user
* `POST /api/auth/login/` → Authenticate & get JWT token
* `POST /api/auth/logout/` → Logout user
* `POST /api/token/refresh/` → Refresh JWT token

### User Management

* `GET /api/auth/users/` → List all users (**Admin, Manager only**)
* `GET /api/auth/users/<id>/` → Get user details (**Admin only**)
* `PUT /api/auth/users/<id>/` → Update user (**Admin only**)
* `DELETE /api/auth/users/<id>/` → Delete user (**Admin only**)

### Profile

* `GET /api/auth/profile/` → View logged-in user profile (**All roles**)

---

## 🔒 Role-Based Access Control (RBAC)

### Admin

✅ Create, Update, Delete Users
✅ View All Users
✅ Full Access

### Manager

✅ View All Employees
❌ Cannot Edit/Delete Admins

### Employee

✅ View Own Profile Only
❌ No Access to Other Users

---

## 🛠️ Tech Stack

* **Backend**: Django, Django REST Framework
* **Database**: PostgreSQL / MySQL
* **Authentication**: JWT (djangorestframework-simplejwt)
* **Frontend**: React.js (Vercel)
* **Deployment**: AWS EC2, Nginx, Gunicorn
* **Static Files**: Cloudinary

---


## 👨‍💻 Author

**Athish Ulleri**

* 🌐 [www.athishulleri.online](https://www.athishulleri.online)
* 📧 Contact: athishulleri@gmail.com

# 🏔️ Trekking Management App V2

A full-stack Trekking Management Application developed as part of the IIT Madras BS Degree in Data Science — Modern Application Development II (MAD2) course.

The application provides a complete platform for managing treks, trekkers, staff, and bookings with separate workflows for Admin, Staff, and Trekker users.

## 📌 Project Overview

The Trekking Management App is designed to simplify the management of trekking activities and bookings. 

The application supports:
* Trekker registration and authentication
* Browsing and filtering available treks
* Trek booking and booking management
* Staff management and trek assignment
* Participant management
* Trek management
* User management and blacklisting
* Role-based access control
* Redis-based API caching
* Celery-based background tasks

The project follows a frontend-backend architecture, with a Vue.js frontend communicating with a Flask REST API backend.

## ✨ Features

### 👤 Trekker
* Register as a new trekker
* Login and logout
* Browse available treks
* Filter treks
* View trek information
* Book treks
* View booking history
* View booking status
* Manage profile

### 👨‍💼 Staff
* Staff dashboard
* View assigned treks
* View trek participants
* Manage participant-related information
* Update trek status

### 👑 Admin
* Admin dashboard
* Manage staff
* Create, update and delete treks
* Manage users
* Blacklist/deactivate users
* View and manage system information

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Vue 3 |
| **Build Tool** | Vite |
| **UI Framework** | Bootstrap |
| **Backend** | Flask |
| **API** | Flask REST API |
| **Database** | SQLite |
| **ORM** | SQLAlchemy |
| **Authentication**| JWT |
| **Caching** | Redis |
| **Background Tasks**| Celery |
| **Version Control** | Git & GitHub |

## 🏗️ Application Architecture

```text
                    ┌─────────────────────┐
                    │     Vue 3 Frontend  │
                    │   Vite + Bootstrap  │
                    └──────────┬──────────┘
                               │
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │     Flask Backend   │
                    │    REST API / JWT   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌────────────┐ ┌────────────┐ ┌────────────┐
        │ SQLAlchemy │ │   Redis    │ │   Celery   │
        │    ORM     │ │   Cache    │ │ Background │
        └─────┬──────┘ └────────────┘ │   Tasks    │
              │                       └──────┬─────┘
              ▼                              │
        ┌────────────┐                       ▼
        │   SQLite   │                    Redis
        │  Database  │
        └────────────┘
```
# 📂 Project Structure

```text
trekking-management-app-v2/
│
├── backend/
│   │
│   ├── instance/
│   │   └── trekking.sqlite3
│   │
│   ├── routes/
│   │   ├── admin_routes.py
│   │   ├── admin_user_routes.py
│   │   ├── auth_routes.py
│   │   ├── staff_routes.py
│   │   ├── test_routes.py
│   │   ├── trek_routes.py
│   │   └── user_routes.py
│   │
│   ├── static/
│   │   └── exports/
│   │       └── trek_history_user_11.csv
│   │
│   ├── tasks/
│   │
│   ├── app.py
│   ├── celery_worker.py
│   ├── celerybeat-schedule
│   ├── extensions.py
│   ├── models.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── public/
│   │
│   └── src/
│       ├── assets/
│       │
│       ├── components/
│       │   ├── AdminDashboard.vue
│       │   ├── AdminSummary.vue
│       │   ├── BookingHistory.vue
│       │   ├── Login.vue
│       │   ├── StaffDashboard.vue
│       │   ├── StaffManagement.vue
│       │   ├── TrekManagement.vue
│       │   ├── UserDashboard.vue
│       │   ├── UserManagement.vue
│       │   └── UserRegister.vue
│       │
│       ├── router/
│       │   └── index.js
│       │
│       ├── views/
│       │   ├── AdminView.vue
│       │   ├── LandingView.vue
│       │   ├── LoginView.vue
│       │   ├── RegisterView.vue
│       │   ├── StaffView.vue
│       │   └── UserView.vue
│       │
│       ├── App.vue
│       └── main.js
│
└── README.md
```
<img width="1312" height="1199" alt="ChatGPT Image Sep 20, 2026, 09_08_48 AM" src="https://github.com/user-attachments/assets/aaabde84-661d-4249-a94d-3f409c112695" />

# 🗄️ Database Design
The application uses SQLite as the database with SQLAlchemy ORM.

Main Entities:

* User — Stores user authentication and role information.

* StaffProfile — Stores staff-specific information.

* Trek — Stores trek details and management information.

* Booking — Stores trek booking information and relationships between users and treks.

The database design was created using an ER diagram to represent the relationships between the application's main entities.

# ER-Diagram:
<img width="940" height="627" alt="image" src="https://github.com/user-attachments/assets/b1f33019-272d-42e1-9ed4-d6e958741bd7" />

# 🔐 Authentication & Authorization

The application uses JWT-based authentication. Users are assigned roles such as:

* Admin

* Staff

* Trekker

Role-based access control ensures that users can access only the features available to their respective roles. For example:

* Trekkers can make bookings.

* Staff can manage their assigned treks and participants.

* Admins have access to overall application management.

# ⚡ Redis & Celery

Redis:
Redis is used in the application for API caching to improve the efficiency of frequently accessed data.

Celery:
Celery is used to handle background tasks so that time-consuming operations can be processed asynchronously instead of blocking the main Flask application. Redis acts as the supporting service for the Celery task system.

# 🚀 Running the Project

Prerequisites
Make sure the following are installed:

* Python

* Node.js

* npm

* Redis

* Git
```text
1. Clone the Repository
git clone <(https://github.com/samprikta1507/trekking-management-app-v2.git)>
cd trekking-management-app-v2

2. Start the Backend
Open the backend directory:
cd backend

Activate the Python virtual environment:
source env/bin/activate

Run the Flask application:
python app.py

3. Start Redis
Make sure the Redis server is running. You can verify the Redis connection using:
redis-cli ping
A successful setup should return: PONG

4. Start the Frontend
Open a new terminal and navigate to the frontend directory:
cd frontend

Install the required packages:
npm install

Start the Vue development server:
npm run dev
The frontend will then be available at the local development URL provided by Vite.
```

# 🧪 Testing

The application was tested during development to verify important functionality including:

* User authentication

* Role-based access

* Trek CRUD operations

* User management

* Staff management

* Trek bookings

* Dashboard functionality

* API functionality

* Redis connectivity

* Background task functionality

# 📚 Academic Project
```text
This project was developed as part of:
Indian Institute of Technology Madras
BS Degree in Data Science and Applications
Modern Application Development II (MAD2)
```

# ✅ Project Status
```text
Completed
The Trekking Management App V2 was developed, tested, and submitted as the MAD2 project.
```

# 👩‍💻 Author
```text
SAMPRIKTA MALIK
IIT Madras — BS Degree in Data Science and Applications
```

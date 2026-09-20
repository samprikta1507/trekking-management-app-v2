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

# 🚗 Vehicle Rental Service (Django)

A web-based **Vehicle Rental Management System** built with **Django**, designed to handle vehicle listings, bookings, owner approvals, service timers, and notifications.  
This project is currently **under active development**.

---

## 📌 Project Status

> **Development Phase (Demo / Academic / Learning Project)**  
Core booking workflows are implemented. Additional features are planned.

---

## ✨ Key Features (Implemented)

### 👤 Authentication
- User registration & login
- Role-based behavior (User / Vehicle Owner / Admin)

### 🚙 Vehicles
- Vehicle listing and detail pages
- Vehicle owners can add their own vehicles
- Ownership-based access control

### 📅 Booking System
- Hourly and daily bookings
- Booking lifecycle:
  - `Pending` → `Confirmed` → `On Service` → `Completed`
- Owners can:
  - Accept or reject incoming bookings
  - Confirm pickup
  - Confirm return
- Users can:
  - Confirm pickup
  - Confirm return

### ⏱️ Service Timer
- Timer starts **only after both user and owner confirm pickup**
- Timer duration is based on:
  - Hourly or daily service selected during booking
- Live countdown shown on:
  - **My Bookings (User)**
  - **Incoming Bookings (Owner)**

### 🔔 Notifications
- Notification created when a booking is made
- Notification badge shown in navbar for vehicle owners
- Read/unread notification tracking

### 📄 UI
- Responsive UI using **Bootstrap 5**
- Navbar with dropdowns for bookings, vehicles, and notifications
- AlertifyJS used for success/error notifications

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Bootstrap 5, JavaScript
- **Database:** SQLite (development)
- **Auth:** Django built-in authentication
- **Notifications:** Custom Django app

---

## 📂 Project Structure (Simplified)

vehicle_system/
├── bookings/
│ ├── models.py
│ ├── views.py
│ └──  urls.py
│
├── vehicles/
│ ├── models.py
│ └── views.py
│
├── rentals/
│ ├── models.py
│ └── views.py
│
├── templates/
│ ├── base.html
| ├── bookings/
| ├── rentals/
| ├── vehicles/
│
└── manage.py



## 📸 Screenshots : 


## ⚙️ Setup Instructions (Development)

1️⃣ Clone the repository
    $ Terminal:
    git clone <https://github.com/pznkc7/Vehicle_Rent.git>
    cd vehicle_system

2️⃣ Create virtual environment
    python -m venv rental_sys
    rental_sys\Scripts\activate   # Windows

3️⃣ Install dependencies
    pip install django
    pip install pillow


4️⃣ Run migrations
    python manage.py makemigrations
    python manage.py migrate

5️⃣ Create superuser
    python manage.py createsuperuser

6️⃣ Run development server
    python manage.py runserver



🚧 Planned Enhancements (Future Work)

1. Payment integration

2. Better map integration to show real time location of the vehicle

3. Chat system between vehicle owner and user 💬

4. Late return handling & penalty calculation ⏳

5. Owner dashboard 📊

6. Better permission handling 🔐

7. Improved mobile UI 📱

8. Deployment configuration 📦

⚠️ Notes
This project uses SQLite for development only.

Database resets are expected during development.

Not production-ready yet.

👨‍💻 Author
Pujan Khatri
Learning Project
Vehicle Rental Service – Django

📜 License
This project is for educational and demonstration purposes.


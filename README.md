<<<<<<< HEAD
# BookMySeat
=======
# BookMyShow Clone - Movie Ticket Booking Platform

## 1. Project Overview

This project is a movie ticket booking platform developed as part of a NullClass internship. It replicates core functionalities of a real-world ticketing system like BookMyShow, handling seat reservations, secure payments, and booking confirmations.

The application has been engineered for **reliability, concurrency safety, and user experience**, moving beyond a simple CRUD app to a production-grade system capable of handling real-world edge cases.

**High-Level Summary:**
A Django-based full-stack web application that allows users to browse movies, select seats with real-time locking, pay securely via Stripe, and receive email confirmations. It features a **premium dark-themed UI** and a comprehensive admin dashboard for business analytics.

---

## 2. Key Features

### 🎨 User Interface & Experience
- **Premium Dark Theme:** A sleek, Netflix-inspired dark aesthetic (`#141414`) with glassmorphism effects and smooth transitions.
- **Interactive Seat Map:** Visual cinema layout where users can select individual seats.
- **Responsive Design:** Fully responsive layout optimized for desktop and mobile devices.
- **Dynamic Filtering:** Filter movies by multiple Genres and Languages instantly.

### 🛠 Core Implementation
- **User Authentication:** Secure Registration and Login with custom dark-themed forms.
- **Movie Management:** Browse "Now Showing" movies with rich details and artwork.
- **Booking Lifecycle:** Complete flow from Seat Selection -> Temporary Lock -> Payment -> Confirmation.

### 🚀 Production-Grade Enhancements
- **Atomic Seat Locking:** Implements a strict "check-then-lock" mechanism within database transactions to prevent double-booking.
- **Concurrency Safety:** Handles race conditions where multiple users try to book the same seat simultaneously using `select_for_update`.
- **Stripe Payment Integration:** Secure handling of payments with server-side webhook verification.
- **Idempotency:** System handles duplicate webhook events gracefully to prevent duplicate processing.
- **Async Notifications:** Sends booking confirmation emails asynchronously (post-transaction commit).
- **Smart Cleanup:** Automatically cleans up expired locks to free seats for other users.
- **Admin Dashboard:** Visual analytics on revenue, occupancy, and booking trends using Chart.js.

---

## 3. System Architecture

The application follows a standard Django MTV (Model-Template-View) architecture but separates business logic into a dedicated service layer for maintainability.

### Seat State Machine
- **Available:** Default state. Open for selection.
- **Locked:** Temporarily reserved for a user (5-minute TTL). Not bookable by others.
- **Booked:** Permanently assigned after successful payment.

### Concurrency Handling
- **Database Transactions:** Critical operations (booking, locking) run inside `transaction.atomic()` blocks.
- **Row-Level Locking:** Uses `select_for_update()` to lock database rows, ensuring sequential access to seat data during high traffic.

### Payment & Verification Flow
1. **Initiate:** User requests checkout -> System creates Stripe Session.
2. **Process:** User pays on Stripe -> Stripe sends `checkout.session.completed` webhook.
3. **Verify:** Webhook Handler receives event -> Verifies Signature -> Confirms Booking -> Sends Email.

---

## 4. Security & Stability Considerations

- **Race Condition Prevention:** The use of `select_for_update` ensures database-level locking.
- **Idempotency:** A `StripeWebhookEvent` model tracks processed event IDs to prevent duplicate booking actions.
- **Data Integrity:** Database constraints (`unique_together`) on Seat models prevent duplicate seat creation at the schema level.
- **Failure Safety:**
  - Email sending is decoupled logic using `transaction.on_commit`.
  - If payment fails or is cancelled, seats are immediately released.

---

## 5. Tech Stack

- **Backend:** Django 5 (Python)
- **Database:** SQLite (Development) / PostgreSQL (Production ready)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla + jQuery)
- **Styling:** Bootstrap 4 + Custom Dark Theme (CSS Variables)
- **Payment Gateway:** Stripe
- **Email Service:** Django SMTP Backend (Gmail)
- **Visualization:** Chart.js (Admin Dashboard)

---

## 6. Setup & Run Instructions

### Prerequisites
- Python 3.10+
- Stripe Account (for Test keys)

### 1. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create a `.env` file or configure your `settings.py` with:
- `SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `EMAIL_HOST_USER` & `EMAIL_HOST_PASSWORD`

### 3. Database Initialization
Run the included setup script to apply migrations and fixes:
```bash
python setup_project.py
```
*Note: If you encounter migration issues, try `python manage.py migrate --fake`.*

### 4. Run Server
Activate the virtual environment and start the server:

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

**Mac/Linux:**
```bash
source .venv/bin/activate
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`

---

## 7. Admin Dashboard

Access: `/movies/admin-dashboard/` (Staff only)

The dashboard provides read-only analytics:
- **Total Bookings & Revenue:** Real-time financial tracking.
- **Occupancy Rate:** Capacity utilization metrics.
- **Popular Movies:** Aggregated booking counts.

---

## 8. Conclusion

This project demonstrates the application of sound software engineering principles to a common problem. By prioritizing data consistency, handling edge cases, and implementing secure patterns, the system moves beyond a simple prototype to a reliability-focused application suitable for real-world usage.

**Submission for NullClass Internship**
**Developer:** Senior Backend Engineer (Intern)
>>>>>>> 4427f0e (Complete BookMySeat project with Stripe integration, email confirmations, and organized structure)
# BookMySeat-Django
# BookMySeat-Django

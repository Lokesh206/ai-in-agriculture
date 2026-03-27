🌾 Krishi Sarathi – Smart Agriculture Transport System
A full-stack web application designed to connect Farmers, Traders, and Transporters for efficient agricultural logistics and real-time tracking.

📌 Project Overview
Krishi Sarathi is a smart logistics platform that helps farmers transport crops easily by:

Connecting farmers with transporters 🚚

Allowing traders to place bids 💰

Providing real-time shipment tracking 📍

Ensuring transparency and efficiency in agriculture supply chain

🚀 Features
👨‍🌾 Farmer
Book transport for crops

View booking status (Pending / Accepted)

Check trader bids

Track shipment live

👉 Example UI: 


🛒 Trader
View available farmer bookings

Place bids on crops

Compete for best pricing

👉 Example UI: 


🚚 Transporter
Accept transport requests

View pending & accepted deliveries

Live GPS tracking updates

👉 Example UI: 


📍 Live Tracking
Real-time vehicle tracking using map

Location updated continuously

👉 Tracking Page: 


🔐 Authentication
Login / Register system

Role-based access (Farmer, Trader, Transporter)

👉 Login Page: 


🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Database: SQLite (krishi.db)

Maps: Leaflet.js (OpenStreetMap – no API key required)

📂 Project Structure
krishi-sarathi/
│
├── app.py                # Main Flask application
├── krishi.db            # SQLite database
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── selection.html
│   ├── farmer.html
│   ├── trade.html
│   ├── transporter.html
│   ├── my_bookings.html
│   ├── all_bids.html
│   ├── track.html
│   └── admin.html
│
└── README.md

🧠 How It Works
Farmers create bookings → stored in database

Traders place bids → updates booking price

Transporters accept bookings → change status

GPS updates → live location tracking

👉 Backend logic handled in: 

Bids Table
booking_id, trader_id, price

💡 Unique Features
✔ Role-based dashboards
✔ Real-time tracking (FREE map, no API key)
✔ Live bidding system
✔ Auto-refresh UI updates
✔ Clean modern UI design
✔ Multi-language support (English + Kannada)

🔮 Future Enhancements
📍 Real GPS tracking with IoT
🔔 Push notifications
📊 Admin analytics dashboard
🤖 AI-based price prediction

💳 Online payment integration


# 🌐 Global Scholar: International Exchange Housing & Buddy Finder

Global Scholar is a comprehensive, Object-Oriented web platform built specifically for university students participating in international exchange programs. It serves as a one-stop portal to find compatible campus buddies, organize secure group chats, and navigate a verified student marketplace for housing and essentials.

Built as a Final Project by Informatics students at **Telkom University**.

## ✨ Core Features
- **🤝 Buddy Finder (Smart Matching):** Connects incoming exchange students with local buddies based on a calculated compatibility score (sleep schedules, study habits, and cleanliness).
- **💬 Secure Messaging:** Encapsulated in-app group chats to facilitate safe, seamless communication for organizing off-campus housing.
- **🛒 Student Marketplace (P2P):** A dynamic, verified ecosystem to sublet apartments or sell pre-loved items like textbooks and electronics. Features a live Drag & Drop image preview.

## 🏗️ Architecture & OOP Design
This project heavily utilizes Object-Oriented Programming (OOP) paradigms modeled in Python (Flask backend):
- **Inheritance:** The base `Listing` class is extended by `HousingListing` (adds rent price, location) and `ItemListing` (adds item price, condition).
- **Composition:** Strong ownership modeling. A `User` directly owns a `MatchProfile`. A `ChatGroup` owns multiple `Message` objects.
- **Encapsulation:** Private states for sensitive data (e.g., `__password`) and internal logic like the `__match_score` calculator.

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript
- **Icons & UI:** Lucide Icons, Custom CSS Animations

---
*© 2026 Global Scholar Platform. Built with OOP Architecture.*
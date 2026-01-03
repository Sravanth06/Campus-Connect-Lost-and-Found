# 🎓 Campus Connect: Intelligent Lost & Found Portal

A centralized web platform designed for GIET University to help students report and recover lost belongings. The system uses **AI (Fuzzy Logic)** to automatically match "Lost" items with "Found" items and notifies users via email.

## 🚀 Key Features
* **AI Matching Engine:** Uses the Levenshtein Distance algorithm to handle typos (e.g., matching "Blue Bag" with "Navy Backpack").
* **Dual Notification System:** Automatically emails both the Finder and the Owner when a match (>70%) is found.
* **Secure Authentication:** Restricted to university students.
* **Image Verification:** Users can upload photos for visual proof.

## 🛠️ Tech Stack
* **Backend:** Django 5.0 (Python)
* **Frontend:** HTML5, Bootstrap 5
* **Database:** SQLite
* **AI Logic:** `TheFuzz` Library

## ⚙️ How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Sravanth06/Campus-Connect-Lost-and-Found.git](https://github.com/Sravanth06/Campus-Connect-Lost-and-Found.git)
   cd Campus-Connect-Lost-and-Found

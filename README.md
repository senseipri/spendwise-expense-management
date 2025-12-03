# 💸 SpendWise – Expense Management System

A modern and intuitive expense tracking platform featuring:

✔ Streamlit frontend with premium dark UI theme  
✔ FastAPI backend with MySQL database  
✔ Analytics dashboard with pie charts & summaries  
✔ Fully documented GitHub-ready structure

SpendWise turns daily expenses into smart money insights.

---

## ✨ Features

- ➕ Add / Update expenses per day
- 🧾 Category-wise breakdown with totals
- 📊 Interactive visual analytics
- 🚀 Fast backend APIs (FastAPI)
- 🗄 Persistent MySQL data storage

---

## 🧱 Project Structure

```bash
SpendWise/
│
├─ backend/               # FastAPI server & DB operations
│  ├─ server.py           # API entrypoint
│  └─ ...                 # Models, controllers, configs
│
├─ frontend/              # Streamlit user interface
│  ├─ app.py              # Main UI flow
│  ├─ add_update_ui.py    # Add/Update page
│  ├─ analytics_ui.py     # Analytics page
│
├─ tests/                 # (optional) test scripts
│
├─ README.md              # Documentation (this file)
├─ requirements.txt       # Python dependencies
└─ .gitignore             # Files excluded from Git versioning
```

---

## 🛠 Installation Guide

### 1️⃣ Clone repository

```bash
git clone https://github.com/yourusername/spendwise-expense-management.git
cd spendwise-expense-management
```

### 2️⃣ Install dependencies

pip install -r requirements.txt

### 3️⃣ MySQL Setup
CREATE DATABASE expense_db;

Update DB credentials in backend/server.py.

### ▶️ Running the Application
### Start backend
-- cd backend

-- uvicorn server:app --reload

API Docs: http://127.0.0.1:8000/docs

### Start frontend
-- cd frontend

-- streamlit run app.py


UI: http://localhost:8501/

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/expenses/{date}` | Fetch daily expenses |
| POST   | `/expenses/{date}` | Add/update daily expenses |
| POST   | `/analytics` | Category analytics |


## 🧑‍💻 Author

Made by Priyansh

## 📄 License

Open-sourced under MIT License.

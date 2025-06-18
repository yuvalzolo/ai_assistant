# AI Assistant API

A simple FastAPI-based backend for managing AI assistants and chat interactions using Google's Gemini API.

## 📦 Features

- Create and manage assistants with system prompts  
- Start chats with a specific assistant  
- Send and receive messages  
- Stores history of assistant and user messages  
- Uses Google Gemini (`gemini-1.5-flash`) via `google.generativeai`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12  
- Poetry (https://python-poetry.org/)  
- Git  
- A Google API Key (https://makersuite.google.com/app/apikey)

---

### 🛠 Installation

git clone https://github.com/yuvalzolo/ai_assistant.git
cd ai_assistant
poetry install

---

### 🔐 Environment Setup

Create a `.env` file in the root with your Gemini API key:

GEMINI_API_KEY=your_google_gemini_api_key_here

---

### ⚙️ Running the API

poetry run uvicorn app.main:app --reload

- Server: http://127.0.0.1:8000  
- Swagger UI: http://127.0.0.1:8000/docs

---

## 🧪 Running Tests

poetry run pytest
This runs the test suite located in the `tests/` directory.

---

## 🧱 Project Structure

ai_assistant/
├── app/
│ ├── init.py
│ ├── main.py # App entrypoint
│ ├── db.py # Database setup
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── services.py # Gemini integration
│ └── routers/ # API routes
│ ├── assistants.py
│ └── chats.py
├── tests/
│ └── test_chat_flow.py # Main test
├── .gitignore
├── pyproject.toml
└── README.md


---

## ✅ Example Flow

1. Create an Assistant via `POST /assistants`  
2. Start a Chat via `POST /chats` with the assistant ID  
3. Send a Message via `POST /chats/{chat_id}/messages`  
4. Get All Messages via `GET /chats/{chat_id}/messages`

---

## ✍️ Author

Made by Yuval Zolo for an assignment project.
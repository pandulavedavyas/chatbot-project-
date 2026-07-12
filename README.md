# Veda AI Assistant

A full-stack AI chatbot web application built with **React** and **Flask**, powered by **Groq** (Llama 3.3 70B). Veda AI provides real-time conversations with context retention, conversation history management, and a modern dark-themed responsive interface.

---

## Live Demo

| Page | Preview |
|------|---------|
| Welcome Screen | Animated SVG robot with floating animation, gradient background, and "Start Chat" CTA |
| Chat Interface | Split layout with sidebar + message thread + input area |
| History | Conversation list with titles, timestamps, and delete actions |

---

## Features

### Core
- **Streaming Responses** — AI tokens stream in real-time for instant feedback
- **Real-time Chat** — Send messages, get instant AI responses
- **Context Retention** — Full conversation history is sent to the AI on every message, so it remembers previous context
- **Auto-titled Conversations** — AI generates a short title for each new conversation automatically
- **Conversation History** — Browse, resume, and delete past conversations from the sidebar

### UI / UX
- **Dark Futuristic Theme** — Custom dark color palette with gradient accents
- **Animated Robot** — SVG robot with breathing and floating animations on the welcome page
- **Markdown Rendering** — AI responses display with formatted headings, bold, italic, lists, etc.
- **Code Block Highlighting** — Syntax-highlighted code blocks with one-click copy
- **Responsive Design** — Works on desktop, tablet, and mobile (sidebar collapses on mobile)
- **Smooth Animations** — Page transitions, message entrance animations via Framer Motion
- **Glass Morphism** — Backdrop blur effects on the header bar
- **Auto-scroll** — Chat automatically scrolls to the latest message
- **Error Display** — Backend errors shown as dismissible banner above the input

---

## Tech Stack

### Frontend
| Library | Version | Purpose |
|---------|---------|---------|
| React | 19.1 | UI library |
| Vite | 6.3 | Build tool and dev server |
| Tailwind CSS | 3.4 | Utility-first CSS framework |
| Framer Motion | 11.18 | Page and element animations |
| Axios | 1.7 | HTTP client for API calls |
| React Router | 7.6 | Client-side routing (`/` and `/chat`) |
| React Markdown | 9.0 | Renders markdown in AI responses |
| React Syntax Highlighter | 15.6 | Code block syntax highlighting |

### Backend
| Library | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Runtime |
| Flask | 3.1 | Web framework |
| Flask-CORS | 5.0 | Cross-origin request handling |
| Groq SDK | 0.13 | AI inference (Llama 3.3 70B) |
| python-dotenv | 1.1 | Loads `.env` variables |

### Database
| Engine | Purpose |
|--------|---------|
| SQLite | Stores conversations and messages (auto-created at project root as `database.db`) |

---

## Folder Structure

```
project/
│
├── backend/
│   ├── app.py                      # Flask entry point — registers blueprints, CORS, DB init
│   ├── config.py                   # Loads .env, exposes GROQ_API_KEY and DATABASE_PATH
│   ├── database.py                 # Creates SQLite tables (conversations, messages)
│   ├── models.py                   # Conversation and Message CRUD classes
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # API key and port (NOT committed to git)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py                 # POST /api/chat — main chat endpoint
│   │   └── conversation.py         # GET/POST/DELETE /api/conversations
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py           # Groq API integration (generate_response, generate_title, streaming)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py              # format_conversation_title, validate_message, validate_conversation_id
│
├── frontend/
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── MessageBubble.jsx   # Individual message (user or AI) with markdown + copy
│   │   │   ├── Sidebar.jsx         # Conversation history list, new chat, delete
│   │   │   └── RobotAnimation.jsx  # Animated SVG robot for the welcome page
│   │   ├── pages/
│   │   │   ├── Welcome.jsx         # Landing page with gradient, robot, and CTA
│   │   │   └── Chat.jsx            # Main chat layout (sidebar + messages + input)
│   │   ├── hooks/
│   │   │   └── useChat.js          # Input state, send logic, auto-scroll, clipboard
│   │   ├── context/
│   │   │   └── ChatContext.jsx     # Global state: messages, conversations, actions
│   │   ├── services/
│   │   │   └── api.js              # Axios instance hitting /api endpoints
│   │   ├── App.jsx                 # Router: / → Welcome, /chat → Chat
│   │   ├── main.jsx                # React DOM entry point
│   │   └── index.css               # Tailwind directives, scrollbar styles, markdown styles
│   ├── package.json
│   ├── vite.config.js              # Dev server proxy: /api → localhost:5000
│   ├── tailwind.config.js          # Custom primary/dark colors, animations
│   └── postcss.config.js
│
├── database.db                     # SQLite database (created at runtime)
└── README.md
```

---

## Getting Started

### Prerequisites

- **Node.js** 18+ and **npm**
- **Python** 3.8+
- **Groq API key** — get one free at https://console.groq.com/keys

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo GROQ_API_KEY=your_groq_api_key_here > .env
echo PORT=5000 >> .env

# Start the server
python app.py
```

Backend runs at **http://localhost:5000**

### 2. Frontend Setup

```bash
# Navigate to frontend (in a second terminal)
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at **http://localhost:5173**

### 3. Open

Visit **http://localhost:5173** in your browser, click **Start Chat**, and begin talking to Veda AI.

---

## How It Works

### Request Flow

```
User types message
       │
       ▼
React frontend (POST /api/chat)
       │
       ▼
Flask backend receives request
       │
       ▼
SQLite: saves user message to messages table
       │
       ▼
SQLite: loads full conversation history
       │
       ▼
Groq API (Llama 3.3 70B): generates AI response using full context
       │
       ▼
SQLite: saves AI response to messages table
       │
       ▼
Flask returns { reply, conversation_id } to frontend
       │
       ▼
React renders AI message with markdown + animation
```

### Context Retention

On every message, the backend loads **all previous messages** in that conversation from SQLite and sends them to Groq as a multi-turn conversation. This means the AI maintains full context:

```
User: "What is Python?"
AI:   "Python is a high-level programming language..."
User: "Now multiply that by 10"
AI:   "4 × 10 = 40"   ← AI knows "that" refers to 4 (but here it would know Python)
```

### Auto-titling

When a new conversation is created (first message, no `conversation_id`), the backend sends the first message to the AI with a prompt to generate a short title (max 50 chars). If title generation fails, the first 50 characters of the user's message are used as a fallback.

---

## API Documentation

All endpoints accept and return JSON. Base URL: `http://localhost:5000`

### POST /api/chat

Send a message and get an AI response.

**Request body:**
```json
{
  "message": "What is machine learning?",
  "conversation_id": 5
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | The user's message |
| `conversation_id` | integer | No | ID of existing conversation. Omit to create a new one |

**Success response (200):**
```json
{
  "reply": "Machine learning is a subset of artificial intelligence...",
  "conversation_id": 5
}
```

**Error responses:**
| Status | Meaning |
|--------|---------|
| 400 | Missing or empty `message` field |
| 404 | `conversation_id` does not exist |
| 500 | AI service error (invalid key, quota exceeded, etc.) |

---

### GET /api/conversations

List all conversations, newest first.

**Response (200):**
```json
[
  {
    "id": 5,
    "title": "Machine Learning Basics",
    "created_at": "2026-07-12 10:30:00",
    "updated_at": "2026-07-12 10:35:00"
  }
]
```

---

### GET /api/conversations/:id

Get a single conversation with all its messages.

**Response (200):**
```json
{
  "id": 5,
  "title": "Machine Learning Basics",
  "created_at": "2026-07-12 10:30:00",
  "updated_at": "2026-07-12 10:35:00",
  "messages": [
    {
      "id": 12,
      "conversation_id": 5,
      "role": "user",
      "content": "What is machine learning?",
      "timestamp": "2026-07-12 10:30:00"
    },
    {
      "id": 13,
      "conversation_id": 5,
      "role": "assistant",
      "content": "Machine learning is a subset of AI...",
      "timestamp": "2026-07-12 10:30:05"
    }
  ]
}
```

---

### POST /api/conversations

Create a new empty conversation.

**Response (201):**
```json
{
  "id": 6,
  "title": "New Chat",
  "created_at": "2026-07-12 11:00:00",
  "updated_at": "2026-07-12 11:00:00"
}
```

---

### DELETE /api/conversations/:id

Delete a conversation and all its messages.

**Response (200):**
```json
{
  "message": "Conversation deleted"
}
```

---

## Database Schema

Two tables in SQLite (`database.db`):

### conversations
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `title` | TEXT | Auto-generated conversation title |
| `created_at` | DATETIME | Timestamp of creation |
| `updated_at` | DATETIME | Timestamp of last activity |

### messages
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `conversation_id` | INTEGER | Foreign key → conversations.id |
| `role` | TEXT | `"user"` or `"assistant"` |
| `content` | TEXT | Message body |
| `timestamp` | DATETIME | When the message was sent |

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | — | Your Groq API key from https://console.groq.com/keys |
| `PORT` | No | `5000` | Port the Flask backend listens on |
| `FLASK_DEBUG` | No | `true` | Set to `false` in production |
| `MAX_MESSAGE_LENGTH` | No | `10000` | Maximum characters per message |

### Vite Proxy

In `frontend/vite.config.js`, the dev server proxies `/api` requests to `localhost:5000` so no CORS issues arise during development.

### `.env.example`

A template `.env.example` file is provided in the `backend/` directory. Copy it to create your `.env`:

```bash
cp backend/.env.example backend/.env
# Then edit backend/.env and add your GROQ_API_KEY
```

---

## Technical Decisions

### Why Groq?
Groq was chosen over OpenAI, Anthropic, and Google Gemini for three reasons:
1. **Free tier** — 30 RPM on Llama 3.3 70B with no credit card required
2. **Speed** — Groq's custom LPU hardware delivers faster inference than traditional GPU providers
3. **OpenAI-compatible API** — The `groq` Python SDK mirrors OpenAI's interface, making future provider switches trivial

### Why SQLite?
For a single-user educational project, SQLite provides zero-configuration storage with full SQL support. No server process, no connection strings — the database is a single file. The schema uses foreign keys with `ON DELETE CASCADE` and indexed columns for query performance.

### Why Server-Sent Events (SSE) for streaming?
SSE was chosen over WebSockets for simplicity. It's unidirectional (server-to-client), works over standard HTTP, requires no special libraries, and reconnects automatically. The Groq SDK's `stream=True` parameter integrates naturally with Flask's `Response` generator pattern.

### System prompt
The AI uses the system prompt: *"You are Veda, a helpful and intelligent AI assistant. Be concise, clear, and friendly. Format responses using markdown when appropriate."* This gives the chatbot a consistent personality across all conversations.

---

## Future Scope

- **User Authentication** — Login/signup for private conversations
- **Export Conversations** — Download chat history as PDF or JSON
- **Voice Input** — Speech-to-text for hands-free use
- **Image Generation** — Generate images via AI on request
- **Dark / Light Theme Toggle** — User-selectable theme
- **Conversation Search** — Full-text search through chat history
- **Keyboard Shortcuts** — Customizable shortcuts for power users

---

## License

This project is for educational purposes.

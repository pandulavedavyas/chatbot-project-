# Veda AI Assistant

A full-stack AI chatbot web application built with **React** and **Flask**, powered by **Groq** (Llama 3.3 70B). Features real-time streaming responses, context retention across sessions, conversation history management, and a professional dark-themed responsive interface.

![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-FF6B00?style=for-the-badge&logo=groq&logoColor=white)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Technical Decisions](#technical-decisions)
- [Future Scope](#future-scope)

---

## Features

### Core
- **Streaming Responses** — AI tokens arrive in real-time via Server-Sent Events (SSE) for instant feedback
- **Context Retention** — Full conversation history is sent to the AI on every message, enabling natural multi-turn conversations
- **Auto-titled Conversations** — AI generates a short, descriptive title for each new conversation automatically
- **Conversation History** — Browse, resume, and delete past conversations from the sidebar
- **New Conversation** — Start fresh chats anytime with the "New chat" button

### UI / UX
- **Professional Blue Theme** — Clean navy background with bright blue gradient accents
- **Suggested Prompts** — Clickable example prompts on the empty chat screen for quick onboarding
- **Markdown Rendering** — AI responses display with formatted headings, bold, italic, lists, and tables
- **Code Block Highlighting** — Syntax-highlighted code blocks with language label and one-click copy
- **Responsive Design** — Works on desktop, tablet, and mobile (sidebar collapses to overlay on mobile)
- **Smart Auto-scroll** — Chat scrolls to the latest message unless you've scrolled up to read history
- **Loading Skeletons** — Animated placeholders while conversation list loads
- **Streaming Indicator** — Animated dots show when AI is generating tokens
- **Dismissible Error Banners** — Backend errors shown as inline banners above the input area
- **Keyboard Navigation** — All interactive elements accessible via Tab and Enter

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
| Flask-CORS | 5.0 | Cross-origin resource sharing |
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
│   ├── app.py                    # Flask entry point — registers blueprints, CORS, DB init
│   ├── config.py                 # Loads .env, exposes GROQ_API_KEY, PORT, DEBUG, MAX_MESSAGE_LENGTH
│   ├── database.py               # Creates SQLite tables with foreign keys, indexes, PRAGMA
│   ├── models.py                 # Conversation and Message CRUD with try/finally connection management
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # API key and config (NOT committed to git)
│   ├── .env.example              # Template for .env setup
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py               # POST /api/chat — chat endpoint with streaming (SSE) support
│   │   └── conversation.py       # GET/POST/DELETE /api/conversations
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py         # Groq API: generate_response, generate_title, generate_response_stream
│   └── utils/
│       ├── __init__.py
│       └── helpers.py            # format_conversation_title, validate_message, validate_conversation_id
│
├── frontend/
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── MessageBubble.jsx # Individual message (user or AI) with markdown, copy, streaming dots
│   │   │   └── Sidebar.jsx       # Conversation history with loading skeleton, keyboard accessible
│   │   ├── pages/
│   │   │   ├── Welcome.jsx       # Landing page with gradient, icon, suggested prompts, and CTA
│   │   │   └── Chat.jsx          # Main chat layout (sidebar + messages + streaming input)
│   │   ├── hooks/
│   │   │   └── useChat.js        # Input state, streaming send, smart auto-scroll, clipboard
│   │   ├── context/
│   │   │   └── ChatContext.jsx   # Global state: messages, conversations, streaming, actions
│   │   ├── services/
│   │   │   └── api.js            # Axios (60s timeout) + fetch streaming client
│   │   ├── App.jsx               # Router: / → Welcome, /chat → Chat
│   │   ├── main.jsx              # React DOM entry point
│   │   └── index.css             # Tailwind directives, Inter font, markdown styles
│   ├── package.json
│   ├── vite.config.js            # Dev server proxy: /api → localhost:5000
│   ├── tailwind.config.js        # Custom primary/surface color scales
│   └── postcss.config.js
│
├── database.db                   # SQLite database (created at runtime)
├── .gitignore                    # Excludes node_modules, venv, .env, database.db
└── README.md
```

---

## Getting Started

### Prerequisites

- **Node.js** 18+ and **npm**
- **Python** 3.8+
- **Groq API key** — get one free at https://console.groq.com/keys (no credit card required)

### 1. Clone the Repository

```bash
git clone https://github.com/pandulavedavyas/chatbot-project-.git
cd chatbot-project-
```

### 2. Backend Setup

```bash
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

# Create .env from template and add your API key
cp .env.example .env
# Edit .env and set GROQ_API_KEY=your_key_here

# Start the server
python app.py
```

Backend runs at **http://localhost:5000**

### 3. Frontend Setup

```bash
# Open a second terminal
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at **http://localhost:5173**

### 4. Use

Visit **http://localhost:5173**, click **Start a new chat**, and begin talking to Veda AI.

---

## How It Works

### Request Flow

```
User types message → clicks Send (or presses Enter)
       │
       ▼
React frontend (POST /api/chat { message, conversation_id, stream: true })
       │
       ▼
Flask backend validates input (length, type, conversation existence)
       │
       ▼
SQLite: saves user message to messages table
       │
       ▼
SQLite: loads full conversation history for this conversation
       │
       ▼
Groq API (Llama 3.3 70B): streams AI response token-by-token via SSE
       │
       ▼
Each token → frontend appends to the AI message bubble in real-time
       │
       ▼
Final token → SQLite saves complete AI response to messages table
       │
       ▼
Frontend shows streaming indicator → then full rendered markdown response
```

### Context Retention

On every message, the backend loads **all previous messages** in that conversation from SQLite and sends them to Groq as a multi-turn conversation. This means the AI maintains full context:

```
User: "What is Python?"
AI:   "Python is a high-level programming language known for its simplicity..."
User: "Now write a function in it"
AI:   [writes a Python function]  ← AI knows "it" refers to Python
```

### Auto-titling

When a new conversation is created (first message, no `conversation_id`), the backend sends the first message to the AI with a prompt to generate a short title (max 50 characters). If title generation fails, the first 50 characters of the user's message are used as a fallback.

---

## API Documentation

All endpoints accept and return JSON. Base URL: `http://localhost:5000`

### POST /api/chat

Send a message and get an AI response (supports streaming).

**Request body:**
```json
{
  "message": "What is machine learning?",
  "conversation_id": 5,
  "stream": true
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `message` | string | Yes | — | The user's message (max 10,000 chars) |
| `conversation_id` | integer | No | `null` | ID of existing conversation. Omit to create a new one |
| `stream` | boolean | No | `false` | Set `true` for SSE streaming response |

**Non-streaming response (200):**
```json
{
  "reply": "Machine learning is a subset of artificial intelligence...",
  "conversation_id": 5
}
```

**Streaming response (stream: true):**
Returns `text/event-stream` with SSE events:
```
data: {"token": "Machine", "done": false}
data: {"token": " learning", "done": false}
data: {"token": " is", "done": false}
...
data: {"token": "", "done": true, "conversation_id": 5}
```

**Error responses:**
| Status | Meaning |
|--------|---------|
| 400 | Missing/empty `message`, invalid type, or message exceeds 10,000 chars |
| 404 | `conversation_id` does not exist |
| 500 | AI service error (returned as generic message, details logged server-side) |

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

Delete a conversation and all its messages (cascade delete).

**Response (200):**
```json
{
  "message": "Conversation deleted"
}
```

**Error:**
| Status | Meaning |
|--------|---------|
| 404 | Conversation not found |

---

## Database Schema

Two tables in SQLite (`database.db`) with foreign key constraints and indexes:

### conversations
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `title` | TEXT NOT NULL | Auto-generated conversation title |
| `created_at` | TIMESTAMP | Defaults to current timestamp |
| `updated_at` | TIMESTAMP | Updated on each new message |

**Index:** `idx_conversations_updated` on `updated_at DESC`

### messages
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `conversation_id` | INTEGER NOT NULL | Foreign key → `conversations.id` ON DELETE CASCADE |
| `role` | TEXT NOT NULL | `"user"` or `"assistant"` |
| `content` | TEXT NOT NULL | Message body |
| `timestamp` | TIMESTAMP | When the message was sent |

**Index:** `idx_messages_conversation` on `conversation_id`

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | — | Your Groq API key from https://console.groq.com/keys |
| `PORT` | No | `5000` | Port the Flask backend listens on |
| `FLASK_DEBUG` | No | `true` | Set to `false` in production to disable debug mode |
| `MAX_MESSAGE_LENGTH` | No | `10000` | Maximum characters allowed per message |

### `.env.example`

A template file is provided at `backend/.env.example`. To set up:

```bash
# macOS/Linux
cp backend/.env.example backend/.env

# Windows
copy backend\.env.example backend\.env

# Then edit backend/.env and add your GROQ_API_KEY
```

### Vite Proxy

In `frontend/vite.config.js`, the dev server proxies `/api` requests to `localhost:5000` so no CORS issues arise during development.

---

## Technical Decisions

### Why Groq?

Groq was chosen over OpenAI, Anthropic, and Google Gemini for three reasons:

1. **Free tier** — 30 requests per minute on Llama 3.3 70B with no credit card required
2. **Speed** — Groq's custom LPU (Language Processing Unit) hardware delivers significantly faster inference than traditional GPU providers
3. **OpenAI-compatible API** — The `groq` Python SDK mirrors OpenAI's interface format, making future provider switches trivial (change one import line)

### Why SQLite?

For a single-user educational project, SQLite provides zero-configuration storage with full SQL support:
- No server process to install or manage
- No connection strings — the database is a single `database.db` file
- Full foreign key support with `ON DELETE CASCADE` for automatic cleanup
- Indexed columns for query performance as data grows

### Why Server-Sent Events (SSE) for streaming?

SSE was chosen over WebSockets for streaming AI responses:
- **Simpler** — Unidirectional (server-to-client), works over standard HTTP
- **No special libraries** — Uses the browser's native `EventSource` / `fetch` API
- **Natural fit** — The Groq SDK's `stream=True` parameter integrates directly with Flask's `Response` generator pattern
- **Auto-reconnect** — SSE connections automatically reconnect if dropped

### System Prompt

The AI uses a consistent system prompt across all conversations:

> *"You are Veda, a helpful and intelligent AI assistant. Be concise, clear, and friendly. Format responses using markdown when appropriate."*

This ensures the chatbot maintains a consistent personality while adapting its responses to the conversation context.

### Error Handling Strategy

- **User messages are never silently deleted** — If the AI fails to respond, the user's message stays visible and an error banner appears
- **Internal errors are not leaked** — The backend logs full exception details server-side but returns generic messages to the client (e.g., "Failed to generate response")
- **Dangling messages are cleaned up** — If the AI call fails after the user message is saved, the user message is automatically rolled back to prevent orphaned messages that would corrupt context

---

## Future Scope

- **User Authentication** — Login/signup for private, per-user conversations
- **Export Conversations** — Download chat history as PDF or JSON
- **Voice Input** — Speech-to-text for hands-free interaction
- **Image Generation** — Generate images via AI on request
- **Dark / Light Theme Toggle** — User-selectable theme preference
- **Conversation Search** — Full-text search through chat history
- **Keyboard Shortcuts** — Customizable shortcuts for power users
- **Multi-language Support** — Interface and AI responses in multiple languages

---

## License

This project is for educational purposes.

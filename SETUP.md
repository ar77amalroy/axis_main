# AXIS AI

**AXIS AI** is an agentic office workflow automation platform. It transforms natural language commands into structured multi-step execution plans dispatched across specialized productivity agents (Documents, Spreadsheets, Presentations).

---

## Key Features

- **Google OAuth 2.0 & JWT Authentication**: Secure one-click Google Sign-in with session-based JWT tokens.
- **LLM-Powered Task Planner**: Analyzes user commands and attached files to decompose complex requests into up to 5 discrete agent actions.
- **Specialized Multi-Agent System**:
  - `document`: Drafts documents, reports, summaries, and meeting notes.
  - `spreadsheet`: Generates financial models, tabular datasets, formulas, and data analysis.
  - `presentation`: Builds slide decks, outlines, speaker notes, and presentation structures.
  - `none`: Handles unsupported, ambiguous, or out-of-scope requests gracefully.
- **Background Orchestrator**: Executes workflow steps sequentially with real-time database state tracking.
- **Interactive React Dashboard**: Clean UI for command inputs, file attachments, and step-by-step live status & output tracking.

---

## Architecture Overview

```
User Command (Frontend / Dashboard)
        │
        ▼ (POST /tasks)
FastAPI Backend (BackgroundTasks)
        │
        ▼
   LLM Planner  ──(Gemini / OpenAI API)──> JSON Action Plan
        │
        ▼
Orchestrator Pipeline
   ├── Step 1 ──> [ Document Agent ]     ──> Result / Artifact
   ├── Step 2 ──> [ Spreadsheet Agent ]  ──> Result / Artifact
   └── Step 3 ──> [ Presentation Agent ] ──> Result / Artifact
        │
        ▼
MongoDB Storage (`users`, `tasks`, `workflow_steps`)
```

---

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn, Motor (Async MongoDB), Pydantic v2, `python-jose`, Google Auth, OpenAI SDK
- **Frontend**: React 18, Vite, React Router v6, Axios, `@react-oauth/google`, Vanilla CSS
- **Database**: MongoDB 6.0+

---

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** & **npm**
- **MongoDB** running locally on `localhost:27017` (or MongoDB Atlas connection string)
- **Google Cloud Console OAuth 2.0 Web Client ID**
- **LLM API Key** (Google Gemini API key or OpenAI-compatible key)

---

## Google OAuth 2.0 Setup

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Navigate to **APIs & Services** > **OAuth consent screen**:
   - Select **External** user type and click **Create**.
   - Fill in **App Name** (`AXIS AI`), **User support email**, and **Developer contact email**.
   - Save and complete the wizard.
4. Navigate to **APIs & Services** > **Credentials**:
   - Click **+ CREATE CREDENTIALS** > **OAuth client ID**.
   - Select Application type: **Web application**.
   - Under **Authorized JavaScript origins**, add:
     - `http://localhost:5173`
     - `http://localhost`
   - Click **Create** and copy your **Client ID** (e.g., `xxxxxxxxxxxx-xxxxxxxxxxxxxxxx.apps.googleusercontent.com`).
5. Use this Client ID in your backend and frontend `.env` configurations.

---

## Configuration & Environment Variables

### 1. Backend (`axis-ai/backend/.env`)

Copy the template:
```bash
# Windows
copy axis-ai\backend\.env.example axis-ai\backend\.env

# macOS / Linux
cp axis-ai/backend/.env.example axis-ai/backend/.env
```

| Variable | Description | Default / Example |
|---|---|---|
| `MONGO_URI` | MongoDB connection URI | `mongodb://localhost:27017` |
| `JWT_SECRET` | Secret key for JWT signing | Long random string (`openssl rand -hex 32`) |
| `GOOGLE_CLIENT_ID` | OAuth 2.0 Client ID | `your-google-client-id.apps.googleusercontent.com` |
| `LLM_API_KEY` | Gemini or OpenAI API Key | `AIza...` / `sk-...` |
| `LLM_BASE_URL` | Base URL for OpenAI-compatible endpoint | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| `LLM_MODEL` | LLM model identifier | `gemini-2.5-flash` |

### 2. Frontend (`axis-ai/frontend/.env`)

Copy the template:
```bash
# Windows
copy axis-ai\frontend\.env.example axis-ai\frontend\.env

# macOS / Linux
cp axis-ai/frontend/.env.example axis-ai/frontend/.env
```

| Variable | Description | Default / Example |
|---|---|---|
| `VITE_GOOGLE_CLIENT_ID` | OAuth 2.0 Client ID (matches backend) | `your-google-client-id.apps.googleusercontent.com` |

---

## Getting Started

### 1. Start MongoDB

Ensure MongoDB is running locally on port 27017:
```bash
mongod --dbpath <path-to-data-dir>
```

### 2. Run the Backend

```bash
cd axis-ai/backend

# 1. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start development server
uvicorn app.main:app --reload --port 8000
```

- API Base URL: **http://localhost:8000**
- Interactive Swagger Docs: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

### 3. Run the Frontend

In a separate terminal:

```bash
cd axis-ai/frontend

# 1. Install dependencies
npm install

# 2. Start Vite dev server
npm run dev
```

- Web App: **http://localhost:5173**

---

## API Reference

### Authentication (`/auth`)
- `POST /auth/google` – Authenticate with Google ID token, returns JWT session token and user profile.
- `GET /auth/me` – Fetch authenticated user profile.

### Tasks & Workflows (`/tasks`)
- `POST /tasks` – Create a new workflow task. Launches background orchestrator pipeline immediately.
- `GET /tasks` – List all tasks for current authenticated user.
- `GET /tasks/{task_id}` – Retrieve details of a specific task.
- `GET /tasks/{task_id}/steps` – Fetch chronological workflow execution steps, status, and agent outputs.

---

## Project Structure

```
axis-ai/
├── .gitignore                   # Ignored files (secrets, venv, node_modules, logs)
├── README.md                    # Project documentation
├── backend/
│   ├── .env.example             # Backend environment template
│   ├── requirements.txt         # Python dependencies
│   └── app/
│       ├── main.py              # FastAPI entrypoint, CORS configuration
│       ├── config.py            # Pydantic Settings configuration loader
│       ├── db.py                # Motor MongoDB connection & collection handles
│       ├── deps.py              # Auth dependency (JWT verification)
│       ├── models/              # Pydantic schemas
│       │   ├── user.py          # User models & auth tokens
│       │   ├── task.py          # Task creation & responses
│       │   ├── workflow_step.py # Step execution tracking models
│       │   └── output.py        # Output schemas
│       ├── routers/
│       │   ├── auth.py          # /auth Google OAuth login & profile
│       │   └── tasks.py         # /tasks CRUD & step progression
│       └── services/
│           ├── llm.py           # LLM client & structured JSON caller
│           ├── planner.py       # LLM task planning & agent step generation
│           ├── orchestrator.py  # Background workflow pipeline engine
│           └── agents/          # Specialized agent implementations
│               ├── base.py      # Base agent protocol
│               ├── registry.py  # Agent resolver
│               ├── document.py  # Document generation agent
│               ├── spreadsheet.py # Spreadsheet & tabular agent
│               ├── presentation.py # Presentation deck agent
│               └── none.py      # Fallback unhandled agent
└── frontend/
    ├── .env.example             # Frontend environment template
    ├── index.html               # Vite HTML entrypoint
    ├── package.json             # NPM dependencies & scripts
    ├── vite.config.js           # Vite build & proxy settings
    └── src/
        ├── main.jsx             # React root mount
        ├── App.jsx              # GoogleOAuthProvider & route setup
        ├── App.css              # Custom styling & animations
        ├── api.js               # Axios instance with JWT interceptor
        ├── pages/
        │   ├── Login.jsx        # Google Sign-In view
        │   └── Dashboard.jsx    # Main workflow workspace
        └── components/
            ├── TaskInput.jsx    # Command text input component
            ├── FileUpload.jsx   # File attachment uploader
            └── TaskList.jsx     # Real-time task & step output display
```

---

## License

Internal / Proprietary.

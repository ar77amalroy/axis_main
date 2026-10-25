# Axis Ai

Axis AI is an intelligent backend service that acts as a bridge between users and Large Language Models (LLMs).
It handles task planning, agent selection, and execution, providing a unified API for AI-powered applications.

## 🚀 Features

- **Smart Task Decomposition**: Breaks down complex user requests into manageable subtasks.
- **Agent Orchestration**: Automatically selects the right AI agent (Document, Presentation, Spreadsheet, or General) for each task.
- **Google Gemini Integration**: Powered by the Gemini API for advanced reasoning and generation capabilities.
- **Clean Architecture**: Modular design with separate layers for routing, services, and models.

## 🛠️ Prerequisites

- Python 3.9+
- MongoDB (running locally or accessible via URL)
- A Google Gemini API key (if using Gemini-based agents)

## 📂 Project Structure

```
axis_main/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Application entry point
│   │   ├── config.py         # Configuration management
│   │   ├── db.py             # Database connection
│   │   ├── deps.py           # Dependency injection
│   │   ├── models/           # Database models (Pydantic)
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── output.py
│   │   ├── routers/          # API endpoints
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   └── services/         # Core logic
│   │       ├── llm.py        # LLM interactions
│   │       ├── planner.py    # Task planning
│   │       └── agents/       # Specialized agents
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variable template
│
└── frontend/
    ├── index.html            # Main HTML file
    ├── package.json          # Frontend dependencies
    ├── vite.config.js        # Vite configuration
    ├── src/
    │   ├── api.js            # API client
    │   ├── App.jsx           # Main application component
    │   ├── main.jsx          # React entry point
    │   ├── pages/            # Page components
    │   │   ├── Login.jsx
    │   │   └── Dashboard.jsx
    │   └── components/       # Reusable components
    │       ├── FileUpload.jsx
    │       ├── TaskInput.jsx
    │       └── TaskList.jsx
    └── .env.example          # Environment variable template
```

## ⚙️ Setup Instructions

### 1. Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Create a `.env` file in the `backend/` directory (or copy `.env.example`):
    ```bash
    cp .env.example .env
    ```

4.  Edit `.env` and fill in your configuration:
    ```ini
    # Database connection
    MONGO_URI=mongodb://localhost:27017

    # Authentication (use a strong random string for production)
    JWT_SECRET=replace-with-a-long-random-string

    # Google AI (Gemini) - Optional if using default agents
    GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
    LLM_API_KEY=your-gemini-api-key
    LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
    LLM_MODEL=gemini-2.5-flash
    ```

5.  Run the backend server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  (Optional) Create a `.env` file if needed, though most configuration is hardcoded or comes from the backend API URL.

4.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## 🧩 How It Works

1.  **User Request**: The frontend sends a task description to the `/tasks` endpoint.
2.  **Planning**: The `Planner` service analyzes the request and breaks it into subtasks.
3.  **Agent Selection**: For each subtask, the `Registry` finds the most appropriate agent (e.g., `DocumentAgent` for text tasks, `SpreadsheetAgent` for data tasks).
4.  **Execution**: The selected agent processes the subtask and generates results.
5.  **Aggregation**: The main task is updated with the results from all subtasks.

## 🔒 Security

-   **JWT Authentication**: The backend uses JSON Web Tokens for secure authentication.
-   **Password Hashing**: Passwords are encrypted using `passlib`.
-   **Environment Variables**: Sensitive data should be stored in `.env` files and should **never** be committed to version control.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

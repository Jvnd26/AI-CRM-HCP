# AI-First CRM HCP Module

This project provides a full-stack CRM experience for healthcare professional (HCP) interactions with:
- a React + Vite frontend
- a FastAPI backend
- SQLAlchemy + MySQL persistence
- LangGraph-powered AI actions using Groq and the gemma2-9b-it model

## Features
- Responsive HCP interaction logging form
- AI chat-style assistant for summaries, search, and follow-up generation
- FastAPI endpoints for CRUD and agent actions
- MySQL-backed storage via SQLAlchemy

## Backend setup
1. Navigate to the backend folder.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a MySQL database named `ai_crm_hcp`.
4. Copy `.env.example` to `.env` and update the values.
5. Start the API:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Frontend setup
1. Navigate to the frontend folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite app:
   ```bash
   npm run dev
   ```

## Notes
- The frontend expects the backend at `http://localhost:8000`.
- Set a valid `GROQ_API_KEY` to enable AI summaries.

# OnboardGit

Understand any codebase's history before you touch it.

OnboardGit analyzes a GitHub repository's full commit history to surface what matters — risky files, hidden knowledge gaps, and dependencies nobody documented. Built for developers joining a new codebase.

## The Problem

Joining a new codebase usually means guessing. Which files are fragile? Who actually understands a given module? Are two unrelated-looking files secretly dependent on each other? Normally you find out the hard way — after breaking something.

## Features

* **Hotspot Detection** — Finds the files that change most often across the project's history, usually the files with the most logic and the highest risk.

* **File Ownership** — Identifies who has made the most changes to each file, so you know exactly who to ask.

* **Bus Factor Risk** — Flags files where a single contributor owns 70%+ of all changes — a risk if that person leaves.

* **Temporal Coupling** — Detects files that consistently change together across commits, even with no visible import between them — revealing hidden dependencies.

* **Saved Analysis History** — Every analysis is saved to your account. Revisit a past report instantly without re-running it.

* **Authentication** — Email/password signup and login, with JWT-based session handling.

## Tech Stack

**Backend:** FastAPI, MongoDB, GitPython, JWT (python-jose), bcrypt (passlib)

**Frontend:** React, TypeScript, Tailwind CSS, React Router, Axios

**Database:** MongoDB Atlas

## How It Works

1. Paste any public GitHub repository URL
2. OnboardGit clones it and reads the full commit history
3. Hotspots, ownership, bus factor risks, and coupling are calculated
4. Results are saved to your account in MongoDB Atlas
5. The analysis is displayed in the dashboard

## Project Structure

```text
onboardgit/

├── backend/
│   ├── app/
│   │   ├── api/              # API routes (auth, analysis)
│   │   ├── core/             # Security and authentication
│   │   ├── db/               # MongoDB connection and collections
│   │   └── services/         # Repository and Git analysis logic
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    └── src/
        ├── pages/             # Landing, Login, Signup, Dashboard, About
        ├── components/        # Reusable UI components
        └── context/           # Auth state management
```

## Running Locally

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
MONGODB_URL=your_mongodb_atlas_connection_string
MONGODB_DB=onboardgit
JWT_SECRET_KEY=your_secret_key
```

Start the backend:

```bash
python -m uvicorn app.main:app --reload
```

```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

## What's Next

* GitHub username resolution for commit authors
* Suggested reading path based on file dependencies
* PDF export for analysis reports
* Repository comparison over time
* AI-powered codebase onboarding recommendations

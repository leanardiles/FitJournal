# FitJournal

A no-frills fitness tracker web application that feels like your paper notebook.

## Project Overview

FitJournal is a fitness tracking application built as a final project for COM5222 Fundamentals of Software Engineering at Yeshiva University (Katz School).

## Features (Planned)

- ✅ User registration and authentication
- ✅ 101 default exercises (copied to each user on registration)
- ✅ Exercise management (view, create, update, delete)
- 🚧 Build workout routines
- 🚧 Track daily workouts
- 🚧 Balanced workout suggestions based on muscle groups
- 🚧 Progress tracking and analytics

## Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **ORM:** SQLAlchemy 2.0
- **Database:** MySQL (hosted on Aiven)
- **Authentication:** Bcrypt password hashing
- **Database Driver:** PyMySQL

### Frontend
- **CSS Framework:** PaperCSS (dark mode)
- **JavaScript:** Vanilla JS (ES6+)
- **HTTP Server:** Python http.server (development)

## Project Structure
```
FitJournal/
├── src/                     # Backend source code
│   ├── main.py              # FastAPI application & routes
│   ├── database.py          # SQLAlchemy database connection
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── .env                 # Environment variables (not in repo)
│   └── venv/                # Virtual environment (not in repo)
├── frontend/
│   ├── index.html           # Landing page
│   ├── login.html           # Login page
│   ├── registration.html    # Registration page
│   ├── dashboard.html       # User dashboard (in progress)
│   ├── exercises.html       # Exercise management (in progress)
│   ├── css/
│   │   ├── paper.css        # PaperCSS framework
│   │   └── style.css        # Custom styles (dark theme)
│   ├── js/
│   │   └── api.js           # Frontend-backend API communication
│   └── images/
│       └── logo_only.png    # FitJournal logo
├── docs/
│   └── ER_diagram.png       # Database ER diagram
├── requirements.txt         # Python dependencies
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL database (or Aiven account)
- Git
- Modern web browser

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/leanardiles/FitJournal.git
cd FitJournal
```

2. Create and activate virtual environment:
```bash
# Create venv
python -m venv venv

# Activate (Git Bash/Linux/Mac)
source venv/Scripts/activate

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in `src/` folder with your database credentials:
```env
DB_HOST=your-aiven-host.aivencloud.com
DB_PORT=12345
DB_USER=avnadmin
DB_PASSWORD=your-password
DB_NAME=fitjournalDB
```

5. Test database connection:
```bash
cd src
python database.py
```

You should see:
```
[SUCCESS] Connected to MySQL database
[INFO] MySQL version: 8.0.35
```

6. Run the FastAPI application:
```bash
cd src
uvicorn main:app --reload
```

7. Access API documentation at: `http://127.0.0.1:8000/docs`

### Frontend Setup

1. Open a **new terminal** (keep backend running in the first one)

2. Start the frontend server:
```bash
cd frontend
python -m http.server 8080
```

3. Access pages at:
   - Registration: `http://localhost:8080/registration.html`
   - Login: `http://localhost:8080/login.html`
   - Dashboard: `http://localhost:8080/dashboard.html`

## API Endpoints

### Authentication
- `POST /register` - Register new user (creates user + copies 101 default exercises)
- `POST /login` - User login (returns user_id and email)

### Exercises
- `GET /exercises?user_id={id}` - Get all exercises for user
- `POST /exercises?user_id={id}` - Create new exercise
- `PUT /exercises/{exercise_id}?user_id={id}` - Update exercise
- `DELETE /exercises/{exercise_id}?user_id={id}` - Delete exercise

### Default Exercises
- `GET /default-exercises` - Get all 101 default exercises (template catalog)

### Routines (Placeholder)
- `GET /routines?user_id={id}` - Get user's routines (to be implemented)

## Database Schema

### Tables

#### `users`
- `user_id` (PK) - Auto-increment user ID
- `user_email` - Unique email address
- `user_password` - Bcrypt hashed password
- `user_first_name`, `user_last_name` - Optional profile fields
- `user_sex` - ENUM('M', 'F', 'NB')
- `user_age` - Integer (0-100)
- `user_unit_preference` - ENUM('metric', 'imperial')
- `user_weight`, `user_height` - Decimal/Integer
- `user_subscription` - TINYINT (0 or 1)
- `user_is_active` - Boolean
- `user_created_at`, `user_updated_at` - Timestamps

#### `default_exercises`
- `default_exercise_id` (PK)
- `exercise_name` - VARCHAR(50)
- `exercise_muscle_group` - ENUM (9 muscle groups)
- `exercise_link` - VARCHAR(500) - URL to exercise demo

**101 exercises across:** Legs, Shoulders, Chest, Glutes, Biceps, Triceps, Back, Calves, Abs

#### `exercises`
- `exercise_id` (PK)
- `exercise_name` - VARCHAR(50)
- `exercise_muscle_group` - ENUM (9 muscle groups)
- `exercise_user_current_weight` - DECIMAL(5,2)
- `user_id` (FK → users.user_id)
- `exercise_is_in_routine` - Boolean
- `exercise_times_performed` - Integer
- `exercise_link` - VARCHAR(500)
- `comments` - VARCHAR(300)
- `exercise_created_at`, `exercise_updated_at` - Timestamps

#### `routine` (Placeholder)
- `routine_id` (PK)
- `user_id` (FK → users.user_id)
- `days_per_week` - Integer (1-7)

## Design Philosophy

### Two-Table Exercise Approach

FitJournal uses a **copy-on-registration** approach:

1. **`default_exercises`** - Template catalog (101 exercises)
2. **`exercises`** - User's personal copy (linked by `user_id`)

**Benefits:**
- Each user has full control over their exercises
- Users can modify/delete without affecting others
- Simple queries (no JOINs needed)
- Easy to add custom exercises

**On Registration:**
- All default exercises are copied to the user's `exercises` table
- User can then modify weights, add comments, delete unwanted exercises
- Each user's data is completely independent

## Current Status

### Completed ✅
- [x] Database schema designed (ER diagram created)
- [x] MySQL database on Aiven with 3 tables
- [x] 101 default exercises imported
- [x] SQLAlchemy ORM models (User, Exercise, DefaultExercise, Routine)
- [x] Pydantic schemas for validation
- [x] User registration endpoint (creates user + copies exercises)
- [x] User login endpoint (authentication with bcrypt)
- [x] Exercise CRUD API endpoints
- [x] CORS configured for frontend-backend communication
- [x] Frontend registration page (dark mode, PaperCSS)
- [x] Frontend login page (dark mode, PaperCSS)
- [x] JavaScript API communication layer
- [x] Virtual environment setup
- [x] Git repository with proper .gitignore

### In Progress 🚧
- [ ] Dashboard page UI
- [ ] Exercises page UI (display, filter, edit)
- [ ] User profile page
- [ ] Routine creation interface

### Planned 📋
- [ ] Routine management system
- [ ] Workout logging functionality
- [ ] Progress tracking (charts/graphs)
- [ ] Balanced workout suggestions algorithm
- [ ] JWT token-based authentication (upgrade from basic auth)
- [ ] Password reset functionality
- [ ] Deployment (Vercel/Netlify frontend + Railway backend)

## Development Workflow

### Starting Work Session

```bash
# Terminal 1: Start backend
cd FitJournal
source venv/Scripts/activate
cd src
uvicorn main:app --reload

# Terminal 2: Start frontend
cd FitJournal/frontend
python -m http.server 8080

# Terminal 3: Git operations
cd FitJournal
git status
git add .
git commit -m "Your message"
git push
```

### Making Changes

- Edit code in VS Code
- Save files (Ctrl+S)
- Backend auto-reloads with `--reload` flag
- Frontend: just refresh browser (Ctrl+R)

## Technologies & Libraries

### Backend Dependencies
- `fastapi` - Modern web framework
- `uvicorn[standard]` - ASGI server
- `sqlalchemy` - ORM for database
- `pymysql` - MySQL driver
- `python-dotenv` - Environment variables
- `passlib[bcrypt]` - Password hashing
- `pydantic[email]` - Data validation

### Frontend Dependencies
- **PaperCSS** - Minimal CSS framework
- **Fetch API** - HTTP requests
- **LocalStorage** - Client-side session management

## Security Notes

- ✅ Passwords are hashed with bcrypt (never stored plain text)
- ✅ `.env` file excluded from Git (contains credentials)
- ✅ CORS configured (currently allows all origins for development)
- ⚠️ TODO: Implement JWT tokens for stateless authentication
- ⚠️ TODO: Add rate limiting on API endpoints
- ⚠️ TODO: Implement HTTPS for production

## Known Issues & TODOs

1. **main.py cleanup needed** - Remove old CLI code (lines 206+)
2. **Dashboard page missing** - Login redirects here but file doesn't exist
3. **No JWT tokens yet** - Using basic session storage
4. **CORS allows all origins** - Need to restrict in production
5. **No input sanitization** - Add XSS protection
6. **No rate limiting** - Vulnerable to brute force attacks

## Testing

### Backend Testing (Swagger UI)
1. Start backend: `uvicorn main:app --reload`
2. Go to: `http://127.0.0.1:8000/docs`
3. Test `/register` endpoint with sample data
4. Test `/login` endpoint
5. Test `/exercises` endpoints

### Frontend Testing
1. Start both servers (backend + frontend)
2. Go to: `http://localhost:8080/registration.html`
3. Create test account
4. Login with test credentials
5. Check browser console (F12) for errors

## Contributing

This is an educational project. Contributions welcome for learning purposes.

## Author

**Leandro Ardiles**
- MS Computer Science, Yeshiva University (Katz School)
- Course: COM5222 Fundamentals of Software Engineering
- Project Timeline: November - December 2024

## Repository

GitHub: [https://github.com/leanardiles/FitJournal](https://github.com/leanardiles/FitJournal)

## License

This project is for educational purposes.

## AI use

This READ ME file has been created with the help of Claude.ai

---

*Last Updated: December 1, 2024*
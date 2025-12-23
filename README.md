# FitJournal

A no-frills fitness tracker web application that feels like your paper notebook.

## Project Overview

FitJournal is a comprehensive fitness tracking application built as a final project for COM5222 Fundamentals of Software Engineering at Yeshiva University (Katz School). The application provides a complete workout management system with routine planning, exercise tracking, and workout history visualization.

## Features

- ✅ User registration and authentication
- ✅ User profile management (age, weight, height, unit preferences)
- ✅ 101 default exercises (copied to each user on registration)
- ✅ Exercise management with muscle group organization
- ✅ Custom routine builder (1-7 days per week, multiple muscle groups per day)
- ✅ Intelligent workout generation algorithm
- ✅ Daily workout tracking (Get WOD - Workout of the Day)
- ✅ Workout history calendar with multi-day filtering
- ✅ Automatic exercise weight tracking and updates
- ✅ Session-based workout logging
- ✅ Progress tracking by exercise frequency

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
- **UI Design:** Custom dark theme (#171717 background)

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
│   ├── dashboard.html       # User dashboard
│   ├── profile.html         # User profile management
│   ├── exercises.html       # Exercise management with muscle group tabs
│   ├── routine.html         # Routine builder (days + muscle groups)
│   ├── calendar.html        # Workout history calendar with filtering
│   ├── getwod.html          # Workout of the Day generation & completion
│   ├── css/
│   │   ├── paper.css        # PaperCSS framework
│   │   └── style.css        # Custom dark theme styles
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

3. Access the application at: `http://localhost:8080/`

### Test User
You can use the following test user credentials:
- Email: test@test.com
- Password: testUSER123!


## Core Workflows

### 1. Registration & Profile Setup
1. Register new account with email/password
2. Set up profile (name, age, weight, height, unit preference)
3. 101 default exercises automatically copied to user account

### 2. Exercise Management
1. View exercises organized by 9 muscle groups (tabs)
2. Update current weight for each exercise
3. Toggle exercises in/out of routine
4. Track exercise performance count

### 3. Routine Creation
1. Select training days per week (1-7)
2. Assign muscle groups to each day
3. System stores routine structure for workout generation

### 4. Workout Selection (Calendar)
1. View calendar with multi-day filtering (Current Day, All Days, Day 1, Day 2, etc.)
2. Manually select exercises or auto-generate based on algorithm
3. Algorithm selects 4 exercises per muscle group (prioritizes least-performed)
4. View workout history with sessions displayed by date

### 5. Workout Execution (Get WOD)
1. Generate Workout of the Day based on current routine day
2. Pre-filled weights from exercise database
3. Enter sets/reps for each exercise
4. Mark as complete to log workout and advance to next day
5. Completed exercises automatically deselected for next planning cycle

### 6. Progress Tracking
1. Calendar displays workout history (last 10 sessions)
2. Track sets completed per exercise per session
3. Exercise performance count auto-increments
4. Weight progression tracked automatically

## API Endpoints

### Authentication
- `POST /register` - Register new user (creates user + copies 101 default exercises)
- `POST /login` - User login (returns user_id and email)

### Profile
- `GET /profile/{user_id}` - Get user profile
- `PUT /profile/{user_id}` - Update user profile

### Exercises
- `GET /exercises?user_id={id}` - Get all exercises for user
- `POST /exercises?user_id={id}` - Create new exercise
- `PUT /exercises/{exercise_id}?user_id={id}` - Update exercise
- `DELETE /exercises/{exercise_id}?user_id={id}` - Delete exercise
- `PATCH /exercises/{exercise_id}/weight` - Update exercise weight

### Routines
- `GET /routine/{user_id}` - Get user's routine
- `POST /routine/{user_id}` - Create/update routine
- `DELETE /routine/{user_id}` - Delete routine

### Workout State
- `GET /workout/state/{user_id}` - Get current workout state (which day user is on)

### Workout Sessions & Logs
- `POST /workout/complete/{user_id}` - Complete workout (creates session, logs exercises, advances day)
- `GET /workout/sessions/{user_id}?limit={n}` - Get last N workout sessions
- `POST /workout/logs-by-sessions/{user_id}` - Get logs for specific sessions
- `GET /workout/logs/{user_id}?limit={n}` - Get workout logs

### Next Workout Management
- `GET /next-workout/selections/{user_id}` - Get selected exercises for next workout
- `POST /next-workout/toggle` - Toggle exercise selection
- `POST /next-workout/generate/{user_id}?day_number={n}` - Auto-generate workout for specific day
- `DELETE /next-workout/clear/{user_id}?day_number={n}` - Clear selections for specific day

### Default Exercises
- `GET /default-exercises` - Get all 101 default exercises (template catalog)

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

#### `exercises`
- `exercise_id` (PK)
- `exercise_name` - VARCHAR(50)
- `exercise_muscle_group` - ENUM (9 muscle groups)
- `exercise_user_current_weight` - DECIMAL(5,2)
- `user_id` (FK → users.user_id)
- `exercise_is_in_routine` - Boolean
- `exercise_times_performed` - Integer (auto-increments on workout completion)
- `exercise_link` - VARCHAR(500)
- `comments` - VARCHAR(300)
- `exercise_created_at`, `exercise_updated_at` - Timestamps

#### `routine_days`
- `routine_id` (PK)
- `user_id` (FK → users.user_id)
- `days_per_week` - Integer (1-7)
- `created_at`, `updated_at` - Timestamps

#### `routine_muscles_per_day`
- `routine_day_id` (PK)
- `user_id` (FK → users.user_id)
- `day_number` - Integer (1-7)
- `muscle_group` - ENUM (Biceps, Back, Triceps, Shoulders, Legs, Glutes, Chest, Calves, Abs)
- `created_at`, `updated_at` - Timestamps

#### `workout_state`
- `state_id` (PK)
- `user_id` (FK → users.user_id) UNIQUE
- `current_day_number` - Integer (which day in routine user is on)
- `last_workout_date` - DATE
- `updated_at` - Timestamp

#### `workout_sessions`
- `session_id` (PK)
- `user_id` (FK → users.user_id)
- `routine_day_number` - Integer
- `workout_date` - DATE
- `session_order` - Integer (1, 2, 3... incrementing order)
- `created_at` - Timestamp

#### `workout_logs`
- `log_id` (PK)
- `user_id` (FK → users.user_id)
- `session_id` (FK → workout_sessions.session_id)
- `routine_day_number` - Integer
- `exercise_id` (FK → exercises.exercise_id)
- `sets_completed` - Integer
- `reps_completed` - Integer
- `weight_used` - DECIMAL(5,2) (snapshot of weight at time of workout)
- `workout_date` - DATE
- `created_at` - Timestamp

#### `next_workout_selections`
- `selection_id` (PK)
- `user_id` (FK → users.user_id)
- `exercise_id` (FK → exercises.exercise_id)
- `is_selected` - Boolean
- `updated_at` - Timestamp
- UNIQUE constraint on (user_id, exercise_id)

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

### Workout Algorithm

The auto-generation algorithm ensures balanced muscle development:

1. Gets muscle groups for current routine day
2. Selects 4 exercises per muscle group
3. Prioritizes exercises with lowest `exercise_times_performed` count
4. Ensures variety and prevents overtraining specific exercises

### Session-Based Logging

Workouts are organized into sessions for clean history tracking:

- Each completed workout creates a `workout_session` entry
- All exercises in that workout link to the same `session_id`
- Sessions have an incrementing `session_order` (1, 2, 3...)
- Calendar displays last 10 sessions with exercise sets completed

## UI/UX Features

### Dark Theme
- Custom dark mode (#171717 background)
- High contrast for readability
- PaperCSS framework with custom overrides

### Calendar Filtering
- **Current Day** - Shows only today's workout (default view)
- **All Days** - Shows all exercises across routine
- **Day 1, Day 2, etc.** - Multi-select specific days (e.g., Day 1 + Day 3)
- Filtered views affect both exercise display and session history

### Responsive Tables
- Fixed columns for exercise names and actions
- Scrollable columns for workout history
- Sticky headers for easy navigation
- White background for calendar (spreadsheet-style)

### Smart Form Behavior
- Auto-save on blur for weight inputs
- Dynamic unit labels (kg/lbs) based on user preference
- Form validation with helpful error messages
- Pre-filled data from database

## Current Status

### Completed ✅
- [x] Database schema with 9 tables
- [x] Complete backend API (20+ endpoints)
- [x] User authentication system
- [x] Profile management page
- [x] Exercise management with muscle group tabs
- [x] Routine builder (days + muscle groups per day)
- [x] Workout calendar with advanced filtering
- [x] Get WOD page with workout generation
- [x] Workout completion and logging
- [x] Session-based workout tracking
- [x] Auto-increment exercise performance counts
- [x] Weight tracking and updates
- [x] Automatic day progression
- [x] Exercise selection system
- [x] Auto-generation algorithm
- [x] Frontend-backend integration
- [x] Dark theme UI/UX
- [x] User logout functionality
- [x] Display user first name in header
- [x] Code refactoring (reduced cyclomatic complexity by 83-92%)

### Known Limitations
- No JWT tokens (using localStorage for session)
- No password reset functionality
- No data export feature
- No analytics/charts visualization
- No mobile-specific optimizations
- CORS allows all origins (development mode)

### To-Do List (High Priority) 🔧
- [ ] **Fix ADD/EDIT/DELETE buttons on Exercises page** - Modal functionality implemented but not displaying correctly (z-index/CSS issue). Buttons are present and functional in code, but modal overlay not visible to user. Backend routes working (`POST /exercises`, `PUT /exercises/{id}`, `DELETE /exercises/{id}`). Requires CSS debugging and testing of modal display.

### Future Enhancements 📋
- [ ] Analytics dashboard (charts, progress graphs)
- [ ] Exercise demo videos/GIFs
- [ ] Rest timer between sets
- [ ] Personal records (PR) tracking
- [ ] Workout notes/comments
- [ ] Social features (share routines)
- [ ] Mobile app (React Native)
- [ ] JWT token authentication
- [ ] Password reset via email
- [ ] Export workout data (CSV/PDF)
- [ ] Deployment (Vercel frontend + Railway backend)

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
- `fastapi==0.115.4` - Modern web framework
- `uvicorn[standard]==0.32.1` - ASGI server
- `sqlalchemy==2.0.36` - ORM for database
- `pymysql==1.1.1` - MySQL driver
- `python-dotenv==1.0.1` - Environment variables
- `passlib[bcrypt]==1.7.4` - Password hashing
- `cryptography==43.0.3` - Security utilities
- `pydantic[email]==2.10.3` - Data validation
- `pydantic-settings==2.6.1` - Settings management

### Frontend Dependencies
- **PaperCSS** - Minimal CSS framework
- **Fetch API** - HTTP requests
- **LocalStorage** - Client-side session management

## Security Notes

- ✅ Passwords are hashed with bcrypt (never stored plain text)
- ✅ `.env` file excluded from Git (contains credentials)
- ✅ CORS configured (currently allows all origins for development)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation (Pydantic schemas)
- ⚠️ TODO: Implement JWT tokens for stateless authentication
- ⚠️ TODO: Add rate limiting on API endpoints
- ⚠️ TODO: Implement HTTPS for production
- ⚠️ TODO: Add CSRF protection

## Code Quality

### Cyclomatic Complexity Improvements
Through systematic refactoring with helper functions:
- `complete_workout()`: CC 12 → 2 (83% reduction)
- `generate_next_workout()`: CC 11 → 1 (91% reduction)
- `create_or_update_routine()`: CC 12 → 1 (92% reduction)

Overall average complexity: **3.2** (excellent maintainability)

## Testing

### Backend Testing (Swagger UI)
1. Start backend: `uvicorn main:app --reload`
2. Go to: `http://127.0.0.1:8000/docs`
3. Test all endpoints with sample data
4. Verify response codes and data structures

### Frontend Testing
1. Start both servers (backend + frontend)
2. Complete user registration
3. Set up profile
4. Add exercises to routine
5. Create routine (select days and muscle groups)
6. Select exercises in calendar
7. Generate WOD
8. Complete workout
9. Verify workout appears in calendar history
10. Test filtering (Current Day, All Days, specific days)

### Test User Flow
```
1. Register → 2. Login → 3. Profile Setup → 
4. View Exercises → 5. Build Routine → 6. Select Exercises → 
7. Generate WOD → 8. Complete Workout → 9. View Calendar History
```

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

## AI Assistance

This project was developed with the assistance of Claude.ai (Anthropic) for:
- Database schema design
- Frontend-backend integration
- Bug fixing and optimization
- Documentation (README.md, code reviews)

---

*Last Updated: December 23, 2024*
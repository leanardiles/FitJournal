# FitJournal

A no-frills fitness tracker web application that feels like your paper notebook.

## Project Overview

FitJournal is a fitness tracking application built as a final project for COM5222 Fundamentals of Software Engineering at Yeshiva University (Katz School).

## Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** MySQL (hosted on Aiven)
- **Authentication:** JWT tokens

### Frontend
- **CSS Framework:** PaperCSS (dark mode)
- **JavaScript:** Vanilla JS

## Features (Planned)

- User registration and authentication
- Create and manage custom exercises
- Build workout routines
- Track daily workouts
- Balanced workout suggestions based on muscle groups

## Project Structure
```
FitJournal/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (not in repo)
├── frontend/
│   ├── index.html           # Landing page
│   ├── login.html           # Login page
│   ├── registration.html    # Registration page
│   ├── exercises.html       # Exercise management
│   └── css/
│       ├── paper.css        # PaperCSS framework
│       └── style.css        # Custom styles
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL database (or Aiven account)
- Git

### Backend Setup

1. Clone the repository:
```bash
   git clone https://github.com/yourusername/FitJournal.git
   cd FitJournal/backend
```

2. Create and activate virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Create `.env` file with your database credentials:
```
   DB_HOST=your-host
   DB_PORT=your-port
   DB_USER=your-user
   DB_PASSWORD=your-password
   DB_NAME=fitjournalDB
   SECRET_KEY=your-secret-key
```

5. Run the application:
```bash
   uvicorn main:app --reload
```

6. Access API documentation at: `http://127.0.0.1:8000/docs`

### Frontend Setup

1. Open any HTML file in a browser, or use a local server:
```bash
   cd frontend
   python -m http.server 8080
```

2. Access at: `http://localhost:8080`

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login

### Exercises
- `GET /exercises` - Get all exercises for user
- `POST /exercises` - Create new exercise
- `PUT /exercises/{id}` - Update exercise
- `DELETE /exercises/{id}` - Delete exercise

### Default Exercises
- `GET /default-exercises` - Get all default exercises

*(More endpoints to be added)*

## Database Schema

- **users** - User accounts
- **default_exercises** - Pre-loaded exercise library
- **user_exercises** - User's custom exercises
- **routines** - Workout routines
- **routine_exercises** - Exercises in routines
- **workout_logs** - Completed workout history

## Current Status

- [x] Database schema designed
- [x] Backend API structure
- [x] User authentication (register/login)
- [x] Default exercises imported
- [ ] Frontend development
- [ ] Exercise CRUD operations
- [ ] Routine management
- [ ] Workout logging
- [ ] Progress tracking

## Author

Leandro - MS Computer Science, Yeshiva University

## License

This project is for educational purposes.
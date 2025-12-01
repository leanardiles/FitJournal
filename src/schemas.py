from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ========== USER SCHEMAS ==========

class UserBase(BaseModel):
    user_email: EmailStr

class UserCreate(UserBase):
    user_password: str

class UserLogin(UserBase):
    user_password: str

class UserResponse(UserBase):
    user_id: int
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_created_at: datetime

    class Config:
        from_attributes = True

# ========== EXERCISE SCHEMAS ==========

class ExerciseBase(BaseModel):
    exercise_name: str
    exercise_muscle_group: str

class ExerciseCreate(ExerciseBase):
    exercise_user_current_weight: Optional[float] = None
    exercise_link: Optional[str] = None
    comments: Optional[str] = None

class ExerciseResponse(ExerciseBase):
    exercise_id: int
    user_id: int
    exercise_user_current_weight: Optional[float] = None
    exercise_is_in_routine: bool
    exercise_times_performed: int
    exercise_created_at: datetime

    class Config:
        from_attributes = True
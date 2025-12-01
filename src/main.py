from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db
from passlib.context import CryptContext


#Legacy modules
import random
import sys
import openai
import os #to interact with the operating system. In this case, it's used to access environment variables
import getpass
import json
from datetime import datetime
from collections import deque


# Create database tables (if they don't exist)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitJournal API")


# ========== CORS CONFIGURATION ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== PASSWORD HASHING ==========
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ========== ROUTES ==========

@app.get("/")
def index():
    return {"message": "Welcome to FitJournal API"}


# ========== USER AUTHENTICATION ROUTES ==========

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user and copy all default exercises to their account
    """
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with hashed password
    hashed_pw = hash_password(user.user_password)
    new_user = models.User(
        user_email=user.user_email,
        user_password=hashed_pw
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Copy all default exercises to user's exercises table
    default_exercises = db.query(models.DefaultExercise).all()
    for default_ex in default_exercises:
        user_exercise = models.Exercise(
            exercise_name=default_ex.exercise_name,
            exercise_muscle_group=default_ex.exercise_muscle_group,
            exercise_link=default_ex.exercise_link,
            user_id=new_user.user_id
        )
        db.add(user_exercise)
    
    db.commit()
    
    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login user with email and password
    """
    # Find user by email
    db_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    
    # Verify user exists and password is correct
    if not db_user or not verify_password(user.user_password, db_user.user_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Check if user is active
    if not db_user.user_is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")
    
    return {
        "message": "Login successful",
        "user_id": db_user.user_id,
        "user_email": db_user.user_email
    }

# ========== EXERCISE ROUTES ==========

@app.get("/exercises", response_model=List[schemas.ExerciseResponse])
def get_exercises(user_id: int, db: Session = Depends(get_db)):
    """
    Get all exercises for a specific user
    """
    exercises = db.query(models.Exercise).filter(models.Exercise.user_id == user_id).all()
    return exercises

@app.post("/exercises", response_model=schemas.ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: schemas.ExerciseCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Create a new custom exercise for a user
    """
    new_exercise = models.Exercise(
        **exercise.dict(),
        user_id=user_id
    )
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise

@app.put("/exercises/{exercise_id}", response_model=schemas.ExerciseResponse)
def update_exercise(exercise_id: int, exercise: schemas.ExerciseCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Update an existing exercise
    """
    db_exercise = db.query(models.Exercise).filter(
        models.Exercise.exercise_id == exercise_id,
        models.Exercise.user_id == user_id
    ).first()
    
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Update exercise fields
    for key, value in exercise.dict().items():
        setattr(db_exercise, key, value)
    
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@app.delete("/exercises/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Delete an exercise
    """
    exercise = db.query(models.Exercise).filter(
        models.Exercise.exercise_id == exercise_id,
        models.Exercise.user_id == user_id
    ).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db.delete(exercise)
    db.commit()
    return None

# ========== DEFAULT EXERCISES ROUTES ==========

@app.get("/default-exercises")
def get_default_exercises(db: Session = Depends(get_db)):
    """
    Get all default exercises (template catalog)
    """
    exercises = db.query(models.DefaultExercise).all()
    return exercises

# ========== ROUTINE ROUTES (PLACEHOLDER) ==========

@app.get("/routines")
def get_routines(user_id: int, db: Session = Depends(get_db)):
    """
    Get all routines for a user (to be implemented)
    """
    routines = db.query(models.Routine).filter(models.Routine.user_id == user_id).all()
    return routines

















#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#///////////////////////////////////////////////////////////// NAVIGATON MENUS ////////////////////////////////////////////////////////////#
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#



# def main_menu():
#     print("MAIN MENU")
#     print("Select from the options below:")
#     print("1. Manage account")
#     print("2. Manage exercises")
#     print("3. Manage routine")
#     print("4. See workout of the day")
#     print("5. Get an AI-generated workout")
#     print("6. Log out")
#     print("7. Close application")

#     while True:
#         try:
#             selection = int(input("Insert here: "))
#             print()
#             if selection == 1:
#                 account_menu()
#             if selection == 3:
#                 routine_menu()
#             elif selection == 2:
#                 exercises_menu()
#             elif selection == 4:
#                 suggest_workout_of_the_day()
#                 mark_workout_as_complete() 
#                 continue_with_another_action()
#             elif selection == 5:
#                 # Check if the unit of measure and routine are set before proceeding
#                 if not unit_of_measure_selected:
#                     print("You haven't selected a unit of measure (pounds/kilograms).")
#                     print("Please go to the Routine Menu to select your unit of measure first.")
#                     continue  # Return to main menu if unit of measure is not set
                
#                 if not user_schedule:
#                     print("You haven't created a training routine yet.")
#                     print("Please go to the Routine Menu to create your schedule first.")
#                     continue  # Return to main menu if routine is not set
                    
#                 get_AI_workout_of_the_day()
#                 continue_with_another_action()
#             elif selection == 6:
#                 print("Logging out. See you next time!")
#                 login_menu()
#             elif selection == 7:
#                 print("Closing application. See you next time!")
#                 exit()
#             else:
#                 print("Invalid option. Please select a number from the list")
#         except ValueError:
#             print("Invalid input. Please select one of the numeric options above.")





# def continue_with_another_action():
#     print("Would you like to perform another action?")
#     print("1. Yes (back to Main Menu)")
#     print("2. No (exit application)")
    
#     while True:
#         answer = int(input("Insert here: "))
#         try:
#             if answer == 1:
#                 print()
#                 main_menu()
#             elif answer == 2:
#                 exit()
#         except ValueError:
#             print("Invalid answer. Please choose one of the options from the menu above")




# def continue_with_another_action_delete_exercise():
#     print()
#     print("Would you like to delete another exercise?")
#     print("1. Yes")
#     print("2. No (back to Main Menu)")
    
#     while True:
#         answer = int(input("Insert here: "))
#         try:
#             if answer == 1:
#                 print()
#                 delete_exercise()
#             elif answer == 2:
#                 main_menu()
#             else:
#                 print("Invalid selection. Please select 1 (Yes) or 2 (No).")
#         except ValueError:
#             print("Invalid selection. Please select 1 (Yes) or 2 (No).")



# def continue_with_another_action_update_weight():
#     print()
#     print("Would you like to update another weight value?")
#     print("1. Yes")
#     print("2. No (back to Main Menu)")
    
#     while True:
#         answer = int(input("Insert here: "))
#         print()
#         try:
#             if answer == 1:
#                 print()
#                 update_weight()
#             elif answer == 2:
#                 main_menu()
#             else:
#                 print("Invalid selection. Please select 1 (Yes) or 2 (No).")
#         except ValueError:
#             print("Invalid selection. Please select 1 (Yes) or 2 (No).")





# def account_menu():
#     print("ACCOUNT MENU")
#     print("Select from the options below:")
#     print("1. Change password")
#     print("2. Set unit of measure (pounds or kilograms)")
#     print("3. Back to Main Menu")
#     print("4. Close Application")

#     while True:
#         selection = int(input("Insert here: "))
#         print()
#         if selection == 1:
#             change_password()
#             print()
#             continue_with_another_action()
#         elif selection == 2:
#             unit_of_measure = get_unit_of_measure()
#             print()
#             continue_with_another_action()    
#         elif selection == 3:
#             main_menu()
#         elif selection == 4:
#             print("Closing application. See you next time!")
#             exit()
#         else:
#             print("Invalid option. Please select a number from the list")





# def exercises_menu():
#     print("EXERCISES MENU")
#     print("Select from the options below:")
#     print("1. See full list of exercises")
#     print("2. Add exercises")
#     print("3. Delete exercises")
#     print("4. Update weight")
#     print("5. Back to Main Menu")
#     print("6. Close Application")

#     while True:
#         selection = int(input("Insert here: "))
#         print()
#         if selection == 1:
#             display_ordered_list()
#         elif selection == 2:
#             add_exercise()                               
#         elif selection == 3:
#             delete_exercise()
#         elif selection == 4:
#             update_weight()
#         elif selection == 5:
#             main_menu()
#         elif selection == 6:
#             print("Closing application. See you next time!")
#             exit()
#         else:
#             print("Invalid option. Please select a number from the list")





# def routine_menu():
#     print("ROUTINE MENU")
#     print("Select from the options below:")
#     print("1. See current routine")
#     print("2. Set/change routine")
#     print("3. Back to Main Menu")
#     print("4. Close Application")

#     while True:
#         selection = int(input("Insert here: "))
#         print()
#         if selection == 1:
#             print_current_routine()
#             print()
#             continue_with_another_action()
#         elif selection == 2:
#             get_days_of_training_for_routine()
#             get_muscle_groups_per_day_for_routine()
#             print_current_routine()
#             print()
#             continue_with_another_action()
#             print()            
#         elif selection == 3:
#             main_menu()
#         elif selection == 4:
#             print("Closing application. See you next time!")
#             exit()
#         else:
#             print("Invalid option. Please select a number from the list")





#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#/////////////////////////////////////////////////////////////// LOGIN MENU ///////////////////////////////////////////////////////////////#
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#



# def login_menu():
#     while True:
#         print("Please sign up or login to your account.")      
#         print("1. Login")
#         print("2. Create an account")
#         print("3. Close Application")
#         try:
#             selection = int(input("Insert here: "))
#             print()
#             if selection == 1:
#                 if verifyLogin():
#                     main_menu()
#             elif selection == 2:
#                 create_account()
#             elif selection == 3:
#                 exit()
#             else:
#                 print("Invalid option. Please try again.")
#                 print()
#                 continue
#         except ValueError:
#             print("Please enter a valid option.")
#             continue    

  



# def create_account():
#     print("CREATING NEW ACCOUNT")

#     file_path = 'usernames_and_passwords.txt'
#     # First check if username already exists
#     existing_usernames = set()
#     try:
#         with open(file_path, "r") as file:
#             for line in file:
#                 if line.strip():  # skip empty lines
#                     username = line.strip().split(",")[0]
#                     existing_usernames.add(username)
#     except FileNotFoundError:
#         pass  # If file doesn't exist, that's fine

#     print("Please enter your desired username:")
#     username = input("Username: ")

#     # If username alreadre exists, it gives an error
#     if username in existing_usernames:
#         print("Username already exists. Please choose a different one.\n")
#         create_account()  # Ask again
#         return
        
#     # If username does not exist, it proceeds with asking their first name:
#     print("Please enter your first name:")
#     user_first_name = input("First name: ")

    
#     # It proceeds with creating it and choosing a password
#     print("Please enter your desired password:")
#     password = getpass.getpass("Password: ")
#     print("Please confirm your password:")
#     confirmed_password = getpass.getpass("Password: ")

#     if password == confirmed_password:
#         needs_newline = os.path.exists(file_path) and os.path.getsize(file_path) > 0 # ensures that new credentials are added on a new line
#         with open(file_path, "a") as file:
#             if needs_newline:
#                 file.write("\n")
#             file.write(f"{username},{password},{user_first_name}\n")
#         print("Account created successfully!")
#         print()
#     else:
#         print("Passwords do not match. Please try again.")
#         print()
#         create_account()





# def verifyLogin():
    
#     file_path = 'usernames_and_passwords.txt'
#     print("LOGGING IN")
#     ask_username = input("Username: ")
#     ask_password = getpass.getpass("Password: ")
    
#     try:
#         #password = password+"\n" # the new line is needed for comparison        
#         with open(file_path, 'r') as file: # this line creates a file object that we can read through from the filepath specified
#             lines = file.readlines()
#             for line in lines:
#                 fields = line.strip().split(",")
#                 if len(fields) == 3:
#                     username, password, user_first_name = fields
#                     if ask_username == username and ask_password == password:
#                         print("Login successful!\n")
#                         return user_first_name
                        
#             print("Invalid credentials. Please try again.")
#             print()
#             return None

                
#     except FileNotFoundError:
#         print("Invalid Credentials. Please try again or create an account first.")

#     return False




#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#/////////////////////////////////////////////////////////////// ACCOUNT ///////////////////////////////////////////////////////////////#
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#



# def change_password():

#     file_path = 'usernames_and_passwords.txt'
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
        
#     print("UPDATING PASSWORD")

#     user_data = {}
#     for line in lines:
#         parts = line.strip().split(',')
#         if len(parts) >= 3:
#             username, password, first_name = parts
#             user_data[username] = [password, first_name]

#     # Select username
#     selected_username = input("Please enter the username for which you want to change the password: ")

#     if selected_username not in user_data:
#         print("Username not found.")
#         return

#     # Verify old password
#     old_password = getpass.getpass("Please enter the current password: ")

#     if old_password != user_data[selected_username][0]:
#         print("Incorrect password. Cannot change password.")
#         return

#     # Get new password
#     new_password = getpass.getpass("Please enter your new password: ")
#     new_confirmed_password = getpass.getpass("Please confirm your new password: ")

#     if new_password != new_confirmed_password:
#         print("Passwords do not match. Please try again.")
#         return

#     # Update password
#     user_data[selected_username][0] = new_password

#     # Write back to file
#     with open(file_path, 'w') as file:
#         for username, (password, first_name) in user_data.items():
#             file.write(f"{username},{password},{first_name}\n")
#     print("Password updated successfully!")
    
    


    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#/////////////////////////////////////////////////////////////// EXERCISES ///////////////////////////////////////////////////////////////#
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#



# class Exercise:
#     def __init__(self, exerciseName: str, MuscleGroup: str, exerciseWeight: float, count: int = 0):
#         self.__name = exerciseName
#         self.muscle_group = MuscleGroup
#         self.__weight = round(exerciseWeight, 1)
#         self.__count = count 


#     @property
#     def name(self):
#         return self.__name

#     @property
#     def weight(self):
#         return self.__weight

#     @weight.setter
#     def weight(self, new_weight):
#         self.__weight = round(new_weight, 1)

#     @property
#     def count(self):
#         return self.__count


#     #Increase the count each time the exercise is done
#     def increment_count(self):
#         self.__count += 1

#     def get_count(self):
#         return self.__count

#     def __str__(self):
#         return f"Exercise: {self.__name}, Muscle Group: {self.muscle_group}, Weight: {self.__weight}kg, Count: {self.__count}"
    

# def add_exercise():
#     print("ADDING A NEW EXERCISE")
#     valid_muscle_groups = list(exercises_dictionary.keys()) #.keys converts the keys of a dictionary into a regular list

#     while True:
#         muscle_group = input("Enter the muscle group of the exercise you want to add: ")
#         if muscle_group in valid_muscle_groups:
#             break
#         print(f"Invalid muscle group. Please choose from: {', '.join(valid_muscle_groups)}")
    
#     exercise_name = input("Enter the exercise name: ")
    
#     while True:
#         try:
#             exercise_weight = float(input("Enter the exercise weight (in pounds): "))
#             break  
#         except ValueError:
#             print("Invalid input. Please enter a valid weight")

#     new_exercise = Exercise(exercise_name, muscle_group, exercise_weight)
#     exercises_dictionary[muscle_group].append(new_exercise)
#     print(f"Exercise '{exercise_name}' added successfully!")
#     continue_with_another_action()
    






# def delete_exercise():
#     global exercises_dictionary
#     print("DELETING AN EXERCISE")
#     valid_muscle_groups = list(exercises_dictionary.keys())

#     while True:
#         muscle_group = input("Enter the muscle group of the exercise you want to delete: ").lower()
#         if muscle_group in valid_muscle_groups:
#             break
#         print(f"Invalid muscle group. Please choose from: {', '.join(valid_muscle_groups)}")

#     exercises = exercises_dictionary[muscle_group]
#     sorted_exercises = sorted(exercises, key=lambda x: x.name)
    
#     print(f"These are the current {muscle_group.upper()} exercises:")
#     print("-" * 40)
#     for exercise in sorted_exercises:
#         print(f"{exercise.name:<30} {exercise.weight:>5} lb")
#     print()
    
#     exercise_name = input("Enter the name of the exercise to delete: ")
    
#     # Find the exercise to delete
#     exercise_to_delete = None
#     for exercise in exercises:
#         if exercise.name.lower() == exercise_name.lower():
#             exercise_to_delete = exercise
#             break
    
#     if exercise_to_delete is None:
#         print("Exercise not found.")
#         continue_with_another_action_delete_exercise()
#         return

#     if len(exercises) == 1:
#         print(f"Cannot delete '{exercise_name}' because it's the only exercise for the '{muscle_group}' muscle group.")
#         continue_with_another_action_delete_exercise()
#         return
        
#     exercises.remove(exercise_to_delete)
#     print(f"Exercise '{exercise_name}' has been deleted successfully!")
#     continue_with_another_action()




    

    
# def update_weight():
#     global exercises_dictionary
#     print("UPDATING WEIGHT")
#     valid_muscle_groups = list(exercises_dictionary.keys())

#     while True:
#         muscle_group = input("Enter the muscle group of the exercise you want to update the weight for: ").lower()
#         if muscle_group in valid_muscle_groups:
#             break
#         print(f"Invalid muscle group. Please choose from: {', '.join(valid_muscle_groups)}")

#     exercises = exercises_dictionary[muscle_group]
#     sorted_exercises = sorted(exercises, key=lambda x: x.name)
    
#     print(f"\nThese are the current {muscle_group.upper()} exercises and weights:")
#     print("-" * 40)
#     for exercise in sorted_exercises:
#         print(f"{exercise.name:<30} {exercise.weight:>5} lb")
#     print()

#     exercise_name = input("Enter the name of the exercise you want to update the weight for: ")
    
#     # Find the exercise by name
#     exercise_to_update = None
#     for exercise in exercises:
#         if exercise.name.lower() == exercise_name.lower():
#             exercise_to_update = exercise
#             break
        
#     if not exercise_to_update:
#         print(f"Exercise '{exercise_name}' not found in {muscle_group}.")
#         continue_with_another_action_update_weight()
#         return

#     # Ask for the new weight
#     while True:
#         try:
#             new_weight = float(input(f"Enter the new weight for '{exercise_to_update.name}' (current: {exercise_to_update.weight} lb): "))

#             if 0 <= new_weight <= 250:
#                 exercise_to_update.weight = new_weight  # Using the setter here
#                 print(f"Successfully updated '{exercise_to_update.name}' to {exercise_to_update.weight} lb")
#                 break
#             else:
#                 print("Invalid weight. Please enter a value between 0 and 250 lb")
                
#         except ValueError:
#             print("Invalid input. Please enter a number.")

#     continue_with_another_action_update_weight()





# exercises_dictionary = {
#     "core": [
#         Exercise("Plank", "core", 0, 1),
#         Exercise("Sit ups", "core", 0, 2),
#         Exercise("Crunches", "core", 0, 3),
#         Exercise("Leg raises", "core", 0, 4),
#         Exercise("Toes to bar", "core", 0, 5),
#     ],
#     "chest": [
#         Exercise("Chest press machine", "chest", 110, 1),
#         Exercise("Fly machine", "chest", 135, 1),
#         Exercise("Bench press w/dumbbell", "chest", 60, 2),
#         Exercise("Cable crossover", "chest", 60, 2),
#         Exercise("Bench press", "chest", 90, 3),
#     ],
#     "shoulders": [
#         Exercise("Lateral raise", "shoulders", 17.5, 1),
#         Exercise("Frontal raise", "shoulders", 15, 1),
#         Exercise("Posterior raise", "shoulders", 15, 1),
#         Exercise("Shoulder press", "shoulders", 50, 1),
#         Exercise("Shrugs", "shoulders", 52.5, 0),
#     ],
#     "triceps": [
#         Exercise("Triceps extension", "triceps", 70, 0),
#         Exercise("Triceps press", "triceps", 110, 0),
#         Exercise("Dips", "triceps", 0, 4),
#         Exercise("Over-head extension", "triceps", 20, 8),
#         Exercise("Cable pushdown", "triceps", 35, 2),
#     ],
#     "back": [
#         Exercise("Row", "back", 115, 0),
#         Exercise("Vertical traction", "back", 115, 1),
#         Exercise("Row rear deltoid", "back", 100, 1),
#         Exercise("Pull-ups", "back", 0, 1),
#         Exercise("Pulldown machine", "back", 200, 3),
#     ],
#     "biceps": [
#         Exercise("Bicep curl machine", "biceps", 125, 0),
#         Exercise("Bicep curl cable", "biceps", 35, 1),
#         Exercise("Bicep curl dumbbell", "biceps", 25, 1),
#         Exercise("Ez bar curl", "biceps", 45, 1),
#     ],
#     "legs": [
#         Exercise("Front squat", "legs", 90, 6),
#         Exercise("Back squat", "legs", 120, 4),
#         Exercise("Leg extension", "legs", 95, 1),
#         Exercise("Leg press", "legs", 180, 3),
#         Exercise("Calf extension", "legs", 110, 0),
#     ],
#     "glutes": [
#         Exercise("Multi-hip", "glutes", 160, 3),
#         Exercise("Abductors", "glutes", 130, 3),
#         Exercise("Bulgarian split squat", "glutes", 40, 2),
#         Exercise("Glute machine", "glutes", 100, 6),
#         Exercise("Hip thrust", "glutes", 100, 2),
#     ],
# }


# def display_ordered_list():
#     print("LIST OF EXERCISES")
#     while True:
#         print("In what order would you like to see the exercices?")
#         print("1. Alphabetical order")
#         print("2. Random order")
#         type_of_order = int(input("Insert here: ").lower())
#         print()

#         try:
#             if type_of_order == 1:
#                 print("Below is the list in ALPHABETICAL order\n")
#                 # Sort muscle group names
#                 for muscle_group in sorted(exercises_dictionary.keys()):
#                     # Sort exercises within each muscle group
#                     sorted_exercises = sorted(exercises_dictionary[muscle_group], key=lambda x: x.name)
#                     print(f"\n{muscle_group.upper()} Exercises")
#                     print("-" * len(f"{muscle_group.upper()} Exercises"))
#                     for exercise in sorted_exercises:
#                         print(f"{exercise.name:<30} {exercise.weight:>7} lb {exercise.get_count():>7}")
#                     print()
#                 break
    
#             elif type_of_order == 2:
#                 print("Below is the list in RANDOM order\n")
#                 for muscle_group in sorted(exercises_dictionary.keys()):
#                     exercises = exercises_dictionary[muscle_group][:]
#                     random.shuffle(exercises)
#                     print(f"\n{muscle_group.upper()} Exercises")
#                     print("-" * len(f"{muscle_group.upper()} Exercises"))
#                     for exercise in exercises:
#                         print(f"{exercise.name:<30} {exercise.weight:>7} lb {exercise.get_count():>7}")
#                 break
    
#             else:
#                 print("Invalid input. Please choose one of the numberic options above.")
#         except ValueError:
#             print("Invalid input. Please choose one of the numberic options above.")
    
#     continue_with_another_action()




# #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
# #/////////////////////////////////////////////////////////////// ROUTINE /////////////////////////////////////////////////////////////////#
# #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#




# # Global variant for storing the unit of measure selected
# unit_of_measure_selected = None

# # Function to have the user select if they want  weight displayed in pounds or kilograms.
# def get_unit_of_measure():
#     global unit_of_measure_selected
#     print("UNIT OF MEASURE")
#     valid_units = ['kilograms', 'pounds']
#     while True:
#         print("Do you want weights displayed in pounds or kilograms? ")
#         unit_of_measure = input("Insert here: ").lower()
#         if unit_of_measure in valid_units:
#             print(f"Succesfully set unit of measure to {unit_of_measure}.")
#             unit_of_measure_selected = unit_of_measure
#             return unit_of_measure
#         else:
#             print("Invalid input. Please enter one of the following: 'kilograms' or 'pounds'.")
    
# #Explanation:
# #- Weight is stored in pounds. If user chooses kilograms, then it later gets converted to kg and rounded to number with zero decimals.
# #- The while True loop: This keeps asking for input until the user provides one of the valid options.
# #- Input validation: The condition if unit_of_measure in valid_units checks whether the user input matches one of the valid options.
# #- Input is limited to 'pounds' or 'kilograms',  capital letters get converted to lower. Other input will not be accepted and will trigger an invalid message.






# # Function to convert pounds to kilograms
# def pounds_to_kilograms_conversion(pounds_amount):
#     pounds_amount = float(pounds_amount)
#     kilogram_conversion = round(pounds_amount * 0.453592, 0)
#     return kilogram_conversion






# #Function to have the user choose how many days per week they want to train.
# days_in_routine = 0

# def get_days_of_training_for_routine():
#     global days_in_routine
#     print("ROUTINE | SETTING DAYS OF TRAINING IN ROUTINE")
#     print("How many days per week do you want to train? (choose from 1 to 7) ")
#     while True:
#         try:
#             days_selected = int(input("Insert here: "))
#             if 1 <= days_selected <=7:
#                 days_in_routine = days_selected
#                 return days_selected
#             else:
#                 print("You entered an invalid number. Please choose between 1 and 7 days.")        #Message to appear if user inputs integer that's not 1 to 7
#         except ValueError: 
#             print("You entered an invalid number. Please choose between 1 and 7 days.")         #Message to appear if user inputs something different than a integer





# #Global variant to store the schedule
# user_schedule = deque()

# def get_muscle_groups_per_day_for_routine():
#     global user_schedule
#     global days_in_routine
#     # Choose what muscles to train
#     muscle_groups = ['core', 'chest', 'shoulders', 'triceps', 'biceps', 'legs', 'back', 'glutes']
#     temp_schedule = []  # initialize an empty list to store the muscle groups that the user selects for each training day. Explained further below.

#     print()
#     print("ROUTINE | SELECTING MUSCLE GROUPS FOR ROUTINE")
#     print("Indicate the muscle groups you want to train each day.")
#     print(f"Options are: {', '.join(muscle_groups)}")
    
#     for i in range(1, days_in_routine + 1):
#         print(f"\nDay {i}")

#         while True:
#             # Get the input for muscle groups
#             selected_groups = input("Enter muscle groups for the day (separate by commas): ").lower().split(',')  # .split() to divide the string into untis with each comma
#             selected_groups = [group.strip() for group in selected_groups]  # .strip() to clean up spaces around input
                
#             # Validate input to ensure user selects only among valid muscle groups
#             if all(group in muscle_groups for group in selected_groups) and len(selected_groups) == len(set(selected_groups)):
#                 temp_schedule.append(selected_groups)
#                 break
#             else:
#                 print("Invalid or duplicate muscle groups. Please try again.")
#     user_schedule = deque(temp_schedule)
#     return user_schedule






# def print_current_routine():
#     global user_schedule
#     global days_in_routine

#     if not user_schedule:
#         print("No routine found. Please set your routine first.")
#         return
    
#     print("\nPRINTING YOUR CURRENT WEEKLY ROUTINE")
#     print(f"Your weekly routine is composed of {days_in_routine} day{'s' if days_in_routine > 1 else ''}:\n")

#     for day, muscle_groups in enumerate(user_schedule, start=1):
#         muscle_group_str = ", ".join([group.capitalize() for group in muscle_groups])
#         print(f"Day {day:<9}| Muscle Groups: {muscle_group_str}")
        




# #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
# #//////////////////////////////////////////////////////// WORKOUT OF THE DAY /////////////////////////////////////////////////////////////#
# #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#


# # Format of the date to include in the workout of the day. E.g. ""Sunday 4 of May"
# now = datetime.now()
# formatted_date = f"{now.strftime('%A')} {now.day} of {now.strftime('%B')}"

# today_selected_exercises = {}

# def suggest_workout_of_the_day():
#     global unit_of_measure_selected, user_schedule, today_selected_exercises
#     today_selected_exercises = {}
    
#     if not unit_of_measure_selected:
#         print("You haven't selected a preferred unit of measure (pounds/kilograms).")
#         print("Go to Account Menu > Set unit of measure and choose this first.")
#         print()
#         return

#     if not user_schedule:
#         print("You haven't created a training routine yet.")
#         print("Go to the Routine Menu to create your schedule first.")
#         print()
#         return

#     print("WORKOUT OF THE DAY 💪")
#     print(f"Here's your workout for today, {formatted_date}: \n") 

#     muscle_groups = user_schedule[0]
#     print(f"Muscle Groups: {', '.join(muscle_groups)}")
#     print('-' * 65)
#     print(f"{'Muscle Group':<20} {'Exercise':<35} {'Weight':<10}")
#     print('-' * 65)
    

#     for group in muscle_groups:
#         if group in exercises_dictionary:
#             exercises = exercises_dictionary[group]

#             # Sort by count (ascending)
#             sorted_exercises = sorted(exercises, key=lambda e: e.get_count())
#             if not sorted_exercises:
#                 continue

#             min_count = sorted_exercises[0].get_count()

#             # Get all exercises with the same lowest count
#             lowest_exercises = [e for e in sorted_exercises if e.get_count() == min_count]

#             # If more than 3 tied at lowest count, pick 3 at random from them
#             if len(lowest_exercises) >= 3:
#                 selected_exercises = random.sample(lowest_exercises, 3)
#             else:
#                 # Fill from lowest ones first, then the next lowest, and so on
#                 selected_exercises = lowest_exercises
#                 next_index = len(lowest_exercises)
#                 while len(selected_exercises) < 3 and next_index < len(sorted_exercises):
#                     selected_exercises.append(sorted_exercises[next_index])
#                     next_index += 1

#             # Store the selected exercises
#             today_selected_exercises[group] = selected_exercises
            
#             # Print the selected exercises
#             for exercise in selected_exercises:
#                 weight = exercise.weight
#                 unit_display = 'lb'
#                 if unit_of_measure_selected == 'kilograms':
#                     weight = pounds_to_kilograms_conversion(weight)
#                     unit_display = 'kg'

#                 print(f"{group.capitalize():<20} {exercise.name:<35} {str(weight) + ' ' + unit_display:<10}")
#             print()





# def mark_workout_as_complete():
#     global user_schedule, today_selected_exercises
#     today_muscle_groups = user_schedule[0]
    
#     while True:
#         print("Mark workout as complete?")
#         print("1. Yes")
#         print("2. No")

#         try:
#             selection = int(input("Insert here: "))
#             if selection == 1:
#                 for group in today_muscle_groups:
#                     if group in today_selected_exercises:
#                         for exercise in today_selected_exercises[group]:
#                             exercise.increment_count()
                
#                 user_schedule.rotate(-1)
#                 print("Workout marked as complete.")
#                 print()
#                 break
                
#             elif selection == 2:
#                 continue_with_another_action()
#                 break
                
#             else:
#                 print("Invalid selection. Please select 1 (Yes) or 2 (No).")
                
#         except ValueError:
#             print("Invalid selection. Please select 1 (Yes) or 2 (No).")
#         print()






# # Reading the API key
# #with open('open_ai_key.csv', 'r') as api_file:
# #    openai.api_key = api_file.read().strip()

# # def get_AI_workout_of_the_day():
# #     global user_schedule
    
# #     # Format the user_schedule as a string before passing it to the OpenAI API
# #     schedule_str = json.dumps(list(user_schedule)[0]) # This converts the first element of user_schedule (which is the current day for workout of the day) dictionary to a string

# #     # Making exercises dictionary readable by the prompt
# #     simplified_exercises = {
# #         muscle_group: [exercise.name for exercise in exercises]
# #         for muscle_group, exercises in exercises_dictionary.items()
# #     }
# #     exercises_json = json.dumps(simplified_exercises)
    
# #     response = openai.chat.completions.create(
# #         model="gpt-4",
# #         messages=[
# #             {"role": "system", "content": "You are a fitness coach."},
# #             {"role": "user", "content": f"Propose a workout based on the user's current routine, which is stored in the following dictionary: {schedule_str}. I want the workout routine to consist of 3 exercises for each muscle group indicated in the user routine. In your suggestion, exclude the exercises listed in {exercises_json} so that the user always gets new exercises. Also, do not end the suggestion asking questions to the user."}
# #         ]
# #     )

# #     # Access the response content correctly
# #     print("AI WORKOUT SUGGESTION 🦾")
# #     print(response.choices[0].message.content)
# #     print()






# def main():
#     print("Welcome to your personal Fitness Tracker.")
#     login_menu()
#     print()
#     main_menu()





# if __name__ == '__main__':
#     main()
    
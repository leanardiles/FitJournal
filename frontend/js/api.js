// ========================================
// FitJournal API JavaScript
// Handles all frontend-backend communication
// ========================================

// API base URL - change this when you deploy
const API_URL = 'http://127.0.0.1:8000';

// ========================================
// REGISTRATION
// ========================================

const registrationForm = document.getElementById('registration-form');

if (registrationForm) {
    registrationForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent page reload
        
        // Get form values
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        // Validate passwords match
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        
        // Validate password length
        if (password.length < 6) {
            alert('Password must be at least 6 characters long');
            return;
        }
        
        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address');
            return;
        }
        
        try {
            // Show loading state (optional)
            const submitButton = registrationForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Creating Account...';
            submitButton.disabled = true;
            
            // Send registration request to backend
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_email: email,
                    user_password: password
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Success!
                alert('Account created successfully! Redirecting to login...');
                window.location.href = 'login.html';
            } else {
                // Error from backend
                alert(`Error: ${data.detail || 'Registration failed. Please try again.'}`);
                
                // Reset button
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        } catch (error) {
            console.error('Registration error:', error);
            alert('Network error. Please check if the backend is running and try again.');
            
            // Reset button
            const submitButton = registrationForm.querySelector('button[type="submit"]');
            submitButton.textContent = 'Create Account';
            submitButton.disabled = false;
        }
    });
}

// ========================================
// LOGIN
// ========================================

const loginForm = document.getElementById('login-form');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent page reload
        
        // Get form values
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        
        // Basic validation
        if (!email || !password) {
            alert('Please enter both email and password');
            return;
        }
        
        try {
            // Show loading state
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Signing In...';
            submitButton.disabled = true;
            
            // Send login request to backend
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_email: email,
                    user_password: password
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Success! Store user info
                localStorage.setItem('user_id', data.user_id);
                localStorage.setItem('user_email', data.user_email);
                
                alert('Login successful! Welcome to FitJournal!');
                window.location.href = 'dashboard.html'; // Redirect to dashboard
            } else {
                // Error from backend
                alert(`Error: ${data.detail || 'Login failed. Please check your credentials.'}`);
                
                // Reset button
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Network error. Please check if the backend is running and try again.');
            
            // Reset button
            const submitButton = loginForm.querySelector('button[type="submit"]');
            submitButton.textContent = 'Sign In';
            submitButton.disabled = false;
        }
    });
}

// ========================================
// HELPER FUNCTIONS
// ========================================

// Check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('user_id') !== null;
}

// Get current user ID
function getCurrentUserId() {
    return localStorage.getItem('user_id');
}

// Get current user email
function getCurrentUserEmail() {
    return localStorage.getItem('user_email');
}

// Logout function
function logout() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    window.location.href = 'index.html';
}

// Protect pages that require login
function requireLogin() {
    if (!isLoggedIn()) {
        alert('Please log in to access this page');
        window.location.href = 'login.html';
    }
}

// ========================================
// EXERCISES (to be used in exercises.html)
// ========================================

// Get all exercises for current user
async function getUserExercises() {
    const userId = getCurrentUserId();
    
    if (!userId) {
        alert('Please log in first');
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/exercises?user_id=${userId}`);
        
        if (response.ok) {
            const exercises = await response.json();
            return exercises;
        } else {
            console.error('Failed to fetch exercises');
            return [];
        }
    } catch (error) {
        console.error('Error fetching exercises:', error);
        return [];
    }
}

// Create new exercise
async function createExercise(exerciseData) {
    const userId = getCurrentUserId();
    
    if (!userId) {
        alert('Please log in first');
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/exercises?user_id=${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(exerciseData)
        });
        
        if (response.ok) {
            const newExercise = await response.json();
            return newExercise;
        } else {
            const error = await response.json();
            alert(`Error creating exercise: ${error.detail}`);
            return null;
        }
    } catch (error) {
        console.error('Error creating exercise:', error);
        alert('Network error. Please try again.');
        return null;
    }
}

// Delete exercise
async function deleteExercise(exerciseId) {
    const userId = getCurrentUserId();
    
    if (!userId) {
        alert('Please log in first');
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/exercises/${exerciseId}?user_id=${userId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            return true;
        } else {
            const error = await response.json();
            alert(`Error deleting exercise: ${error.detail}`);
            return false;
        }
    } catch (error) {
        console.error('Error deleting exercise:', error);
        alert('Network error. Please try again.');
        return false;
    }
}

// ========================================
// PROFILE
// ========================================

// Get user profile
async function getUserProfile() {
    const userId = getCurrentUserId();
    
    if (!userId) {
        alert('Please log in first');
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/profile/${userId}`);
        
        if (response.ok) {
            const profile = await response.json();
            return profile;
        } else {
            console.error('Failed to fetch profile');
            return null;
        }
    } catch (error) {
        console.error('Error fetching profile:', error);
        return null;
    }
}

// Update user profile
async function updateUserProfile(profileData) {
    const userId = getCurrentUserId();
    
    if (!userId) {
        alert('Please log in first');
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/profile/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(profileData)
        });
        
        if (response.ok) {
            const updatedProfile = await response.json();
            return updatedProfile;
        } else {
            const error = await response.json();
            alert(`Error updating profile: ${error.detail}`);
            return null;
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        alert('Network error. Please try again.');
        return null;
    }
}

// ========================================
// CONSOLE LOG (for debugging)
// ========================================

console.log('FitJournal API loaded successfully');
console.log('API URL:', API_URL);
if (isLoggedIn()) {
    console.log('User logged in:', getCurrentUserEmail());
} else {
    console.log('No user logged in');
}
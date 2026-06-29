// ==============================
// CONFIGURATION
// ==============================
const API_BASE_URL = 'http://localhost:5000/api';
const STUDENT_TOKEN_KEY = 'student_token';
const ADMIN_TOKEN_KEY = 'admin_token';

// ==============================
// UTILITY FUNCTIONS
// ==============================

/**
 * Get stored token based on type
 */
function getToken(type = 'student') {
    return localStorage.getItem(type === 'admin' ? ADMIN_TOKEN_KEY : STUDENT_TOKEN_KEY);
}

/**
 * Set token in localStorage
 */
function setToken(token, type = 'student') {
    localStorage.setItem(type === 'admin' ? ADMIN_TOKEN_KEY : STUDENT_TOKEN_KEY, token);
}

/**
 * Remove token from localStorage
 */
function removeToken(type = 'student') {
    localStorage.removeItem(type === 'admin' ? ADMIN_TOKEN_KEY : STUDENT_TOKEN_KEY);
}

/**
 * Check if user is authenticated
 */
function isAuthenticated(type = 'student') {
    return !!getToken(type);
}

/**
 * Make API request with proper headers
 */
async function apiRequest(endpoint, method = 'GET', body = null, type = 'student') {
    const token = getToken(type);
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        method,
        headers
    };
    
    if (body && method !== 'GET') {
        config.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Format date string to locale
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-KE', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return `KES ${parseFloat(amount).toLocaleString('en-KE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}`;
}

/**
 * Show message to user
 */
function showMessage(message, type = 'info', containerId = 'message-container') {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-error' : 
                      type === 'warning' ? 'alert-warning' : 'alert-info';
    
    container.innerHTML = `<div class="alert ${alertClass}">${message}</div>`;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

/**
 * Toggle mobile menu
 */
function toggleMenu() {
    const menu = document.getElementById('navMenu');
    if (menu) {
        menu.classList.toggle('active');
    }
}

/**
 * Logout function
 */
function logout(type = 'student') {
    removeToken(type);
    window.location.href = type === 'admin' ? 
        '/pages/admin/login.html' : 
        '/pages/login.html';
}

/**
 * Check authentication and redirect if needed
 */
function requireAuth(type = 'student') {
    if (!isAuthenticated(type)) {
        window.location.href = type === 'admin' ? 
            '/pages/admin/login.html' : 
            '/pages/login.html';
        return false;
    }
    return true;
}

// ==============================
// INITIALIZATION
// ==============================
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication status for UI updates
    const studentToken = getToken('student');
    const adminToken = getToken('admin');
    
    // Update navigation based on auth status
    const authButtons = document.getElementById('authButtons');
    const userMenu = document.getElementById('userMenu');
    
    if (authButtons && userMenu) {
        if (studentToken) {
            authButtons.style.display = 'none';
            userMenu.style.display = 'flex';
            
            // Fetch user info to display name
            apiRequest('/student/dashboard', 'GET', null, 'student')
                .then(data => {
                    const userNameEl = document.getElementById('userName');
                    if (userNameEl && data.user) {
                        userNameEl.textContent = data.user.full_name;
                    }
                })
                .catch(() => {
                    // Token might be expired
                    removeToken('student');
                    authButtons.style.display = 'flex';
                    userMenu.style.display = 'none';
                });
        }
    }
});

// ==============================
// EXPORT FOR USE IN PAGES
// ==============================
window.EPRA = {
    apiRequest,
    getToken,
    setToken,
    removeToken,
    isAuthenticated,
    requireAuth,
    formatDate,
    formatCurrency,
    showMessage,
    logout,
    toggleMenu,
    API_BASE_URL
};
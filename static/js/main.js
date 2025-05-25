/**
 * RecommRead main JavaScript file
 * Contains shared functionality used across the frontend
 */

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  updateNavigation();
  setupLogoutHandler();
});

// Update navigation based on authentication status
function updateNavigation() {
  const currentUser = getCurrentUser();
  
  const loggedOutElements = document.querySelectorAll('.user-logged-out');
  const loggedInElements = document.querySelectorAll('.user-logged-in');
  const authRequiredElements = document.querySelectorAll('.user-auth-required');
  
  if (currentUser) {
    // User is logged in
    loggedOutElements.forEach(el => el.style.display = 'none');
    loggedInElements.forEach(el => el.style.display = 'block');
    authRequiredElements.forEach(el => el.style.display = 'block');
    
    // Set username in the navigation
    const usernameDisplay = document.getElementById('username-display');
    if (usernameDisplay) {
      usernameDisplay.textContent = currentUser.username;
    }
  } else {
    // User is logged out
    loggedOutElements.forEach(el => el.style.display = 'block');
    loggedInElements.forEach(el => el.style.display = 'none');
    authRequiredElements.forEach(el => el.style.display = 'none');
  }
}

// Get current user from localStorage
function getCurrentUser() {
  const userJson = localStorage.getItem('user');
  if (!userJson) {
    return null;
  }
  
  try {
    return JSON.parse(userJson);
  } catch (e) {
    console.error('Error parsing user data from localStorage:', e);
    localStorage.removeItem('user');
    return null;
  }
}

// Set up logout handler
function setupLogoutHandler() {
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
      fetch('/api/logout', {
        method: 'POST',
        credentials: 'same-origin'
      })
      .then(() => {
        localStorage.removeItem('user');
        showAlert('Logged out successfully', 'success');
        
        setTimeout(() => {
          window.location.href = '/';
        }, 1000);
      })
      .catch(error => {
        console.error('Logout error:', error);
        showAlert('Failed to logout', 'danger');
      });
    });
  }
}

// Show alert message
function showAlert(message, type = 'info') {
  const alertContainer = document.querySelector('.alert-container');
  if (!alertContainer) return;
  
  const alertEl = document.createElement('div');
  alertEl.className = `alert alert-${type} alert-dismissible fade show`;
  alertEl.role = 'alert';
  
  alertEl.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  
  alertContainer.appendChild(alertEl);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (alertEl.parentNode) {
      const bsAlert = new bootstrap.Alert(alertEl);
      bsAlert.close();
    }
  }, 5000);
}
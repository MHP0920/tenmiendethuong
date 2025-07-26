// Authentication utility functions
async function checkAuthentication() {
    try {
        const response = await fetch(`${window.location.origin}/user/profile`, {
            credentials: 'include'
        });
        
        if (response.status === 401) {
            window.location.href = '/login';
            return false;
        }
        
        return response.ok;
    } catch (error) {
        console.error('Authentication check failed:', error);
        window.location.href = '/login';
        return false;
    }
}

async function makeAuthenticatedRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            credentials: 'include'
        });
        
        if (response.status === 401) {
            window.location.href = '/login';
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}

// Initialize authentication check on page load
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuthentication();
});

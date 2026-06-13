// Main JavaScript for CareerPath AI

// API Base URL
const API_BASE_URL = '/api';

// Utility function to make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Search jobs
async function searchJobs(query) {
    try {
        const result = await apiCall(`/jobs/?q=${encodeURIComponent(query)}`);
        console.log('Search results:', result);
        return result;
    } catch (error) {
        console.error('Search error:', error);
    }
}

// Get job details
async function getJobDetails(jobId) {
    try {
        const result = await apiCall(`/jobs/${jobId}/full_details/`);
        console.log('Job details:', result);
        return result;
    } catch (error) {
        console.error('Error fetching job details:', error);
    }
}

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('CareerPath AI loaded');
});

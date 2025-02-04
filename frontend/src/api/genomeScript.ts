import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

interface GenomicQuery {
    query_id: string;
    script: string;
    parameters?: Record<string, any>;
}

export const executeQuery = async (query: GenomicQuery) => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
        `${API_BASE_URL}/analyze`,
        query,
        {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        }
    );
    return response.data;
};

export const login = async (username: string, password: string) => {
    const response = await axios.post(
        `${API_BASE_URL}/token`,
        new URLSearchParams({
            'username': username,
            'password': password
        }),
        {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }
    );
    
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    return access_token;
};

export const executeScript = async (script: string) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/execute`, { script });
        return response.data;
    } catch (error) {
        console.error('Error executing script:', error);
        throw error;
    }
}; 
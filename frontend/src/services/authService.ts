import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

interface AuthResponse {
  is_admin: boolean;
  message: string;
}

export const checkAuth = async (): Promise<AuthResponse> => {
  try {
    const response = await axios.post<AuthResponse>(`${API_BASE_URL}/auth/check`);
    return response.data;
  } catch (error) {
    console.error('Auth check failed:', error);
    throw error;
  }
}; 
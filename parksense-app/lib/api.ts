// Centralized API configuration
// In production, NEXT_PUBLIC_API_URL is set to the Render backend URL
// In development, it defaults to localhost

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

import axios from "axios";
import { auth } from "../config/firebase";

const BASE_URL = "http://localhost:8000";

// Create axios instance with interceptor for Firebase tokens
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 5000, // Reduced from 10s to 5s for better performance
});

// Add request interceptor to include Firebase token
apiClient.interceptors.request.use(async (config) => {
  const user = auth.currentUser;
  if (user) {
    try {
      const token = await user.getIdToken();
      config.headers.Authorization = `Bearer ${token}`;
    } catch (error) {
      console.error('Error getting Firebase token:', error);
    }
  }
  return config;
});

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.log('Request timed out');
    } else if (!error.response) {
      console.log('Backend server not available');
    }
    return Promise.reject(error);
  }
);

// API Functions
export const predictImage = (formData) =>
  apiClient.post("/api/predict-image", formData);

export const predictText = (data) =>
  apiClient.post("/api/predict-text", data);

export const getRecommendation = (data) =>
  apiClient.post("/api/recommend", data);

export const calculateGHG = (data) =>
  apiClient.post("/api/ghg-savings", data);

export const getCarbonCredit = (data) =>
  apiClient.post("/api/carbon-credit", data);

export const downloadCertificate = (params) =>
  apiClient.get("/api/generate-certificate", { params, responseType: "blob" });

// Save analysis result to user dashboard
export const saveAnalysisResult = (data) =>
  apiClient.post("/api/dashboard/save-analysis", data);

// Get dashboard summary
export const getDashboardSummary = () =>
  apiClient.get("/api/dashboard/summary");

// Get dashboard stats only
export const getDashboardStats = () =>
  apiClient.get("/api/dashboard/stats");

// Get user activity only  
export const getUserActivity = (limit = 10) =>
  apiClient.get(`/api/dashboard/activity?limit=${limit}`);

// Firebase Authentication API functions
export const getAuthStatus = () =>
  apiClient.get("/api/auth/status");

export const getUserProfile = () =>
  apiClient.get("/api/dashboard/stats");

export const verifyToken = () =>
  apiClient.post("/api/auth/verify-token");

export const logout = () =>
  apiClient.delete("/api/auth/logout");

// Certificate generation
export const generateCertificate = (data) =>
  apiClient.post("/api/generate-certificate", data, { responseType: "blob" });

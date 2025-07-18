import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';
import * as api from '../services/api';

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState({
    totalAnalyses: 0,
    co2Saved: 0,
    carbonCredits: 0,
    estimatedEarnings: 0,
    recentActivities: [],
    loading: true,
    error: null
  });
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { user, isAuthenticated, loading: authLoading, logout } = useAuth();

  useEffect(() => {
    console.log('🎯 Dashboard useEffect:', { authLoading, isAuthenticated, user: user?.email });
    
    // Only redirect if definitely not authenticated and not loading
    if (!authLoading && !isAuthenticated) {
      console.log('🚨 Dashboard: User not authenticated, redirecting to login');
      navigate('/login');
      return;
    }
    
    if (user) {
      console.log('✅ Dashboard: User authenticated:', user.email);
      setLoading(false);
      // Load dashboard data when user is authenticated
      loadDashboardData();
    }
  }, [isAuthenticated, authLoading, user, navigate]);

  // Load dashboard data from API with optimistic loading
  const loadDashboardData = async () => {
    // First, show placeholder data immediately to improve perceived performance
    setDashboardData({
      totalAnalyses: 0,
      co2Saved: 0,
      carbonCredits: 0,
      estimatedEarnings: 0,
      recentActivities: [],
      loading: false, // Show UI immediately
      error: null
    });
    
    try {
      // Set a shorter timeout for API call (1.5 seconds max for dashboard)
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('API timeout')), 1500)
      );
      
      const apiPromise = api.getDashboardSummary();
      
      // Race between API call and timeout
      const response = await Promise.race([apiPromise, timeoutPromise]);
      
      // Update with real data if API responds
      setDashboardData({
        totalAnalyses: response.data.data.stats.totalAnalyses || 0,
        co2Saved: response.data.data.stats.co2Saved || 0,
        carbonCredits: response.data.data.stats.carbonCredits || 0,
        estimatedEarnings: response.data.data.stats.estimatedEarnings || 0,
        recentActivities: response.data.data.recentActivity || [],
        loading: false,
        error: null
      });
      
    } catch (error) {
      console.log('API not available, keeping placeholder data:', error.message);
      // Keep the placeholder data that was already set
      // No need to update state again
    }
  };

  const handleLogout = async () => {
    // Use Firebase logout from AuthContext
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Logout error:', error);
      navigate('/');
    }
  };

  if (loading || authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50 flex items-center justify-center">
        <div className="text-center">
          <svg className="animate-spin -ml-1 mr-3 h-8 w-8 text-emerald-600 mx-auto mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-emerald-600 font-medium text-sm">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800">{t('dashboard.title')}</h1>
                <p className="text-gray-600 text-sm">Welcome back, {user?.name || user?.email || 'User'}!</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              {t('dashboard.logout')}
            </button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-8 border border-gray-100">
          <div className="text-center">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent mb-4">
              {t('dashboard.welcomeMessage')}
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              {t('dashboard.welcomeDescription')}
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => navigate('/input')}
                className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-semibold py-3 px-6 rounded-xl shadow-lg transform hover:scale-105 transition-all duration-200"
              >
                {t('dashboard.startNewAnalysis')}
              </button>
              <button
                onClick={() => navigate('/history')}
                className="bg-white border-2 border-emerald-600 text-emerald-600 hover:bg-emerald-50 font-semibold py-3 px-6 rounded-xl transition-all duration-200"
              >
                {t('dashboard.viewPreviousAnalyses')}
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards - Dynamic Data */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Analyses */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <p className="text-gray-600 text-sm">{t('dashboard.stats.totalAnalyses')}</p>
                <p className="text-2xl font-bold text-gray-800">
                  {dashboardData.totalAnalyses}
                </p>
              </div>
            </div>
          </div>

          {/* CO2 Saved */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p className="text-gray-600 text-sm">{t('dashboard.stats.co2Saved')}</p>
                <p className="text-2xl font-bold text-gray-800">
                  {dashboardData.co2Saved} {dashboardData.co2Saved !== '—' && t('dashboard.tons')}
                </p>
              </div>
            </div>
          </div>

          {/* Carbon Credits */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-indigo-500 rounded-xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
              <div>
                <p className="text-gray-600 text-sm">{t('dashboard.stats.carbonCredits')}</p>
                <p className="text-2xl font-bold text-gray-800">
                  {dashboardData.carbonCredits}
                </p>
              </div>
            </div>
          </div>

          {/* Estimated Earnings */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
              <div>
                <p className="text-gray-600 text-sm">{t('dashboard.estimatedEarnings')}</p>
                <p className="text-2xl font-bold text-gray-800">
                  {dashboardData.estimatedEarnings !== '—' && t('dashboard.rupees')}{dashboardData.estimatedEarnings}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-gray-100">
            <h3 className="text-xl font-bold text-gray-800 mb-6">{t('dashboard.recentActivity')}</h3>
            <div className="space-y-4">
              {dashboardData.recentActivities && dashboardData.recentActivities.length > 0 ? (
                dashboardData.recentActivities.map((activity, index) => (
                  <div key={index} className="flex items-center p-4 bg-emerald-50 rounded-xl">
                    <div className="w-10 h-10 bg-emerald-500 rounded-full flex items-center justify-center mr-4">
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div>
                      <p className="font-medium text-gray-800">{activity.title}</p>
                      <p className="text-sm text-gray-600">{activity.time}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <svg className="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                  </svg>
                  <p className="text-gray-500">{t('dashboard.noRecentActivity')}</p>
                </div>
              )}
            </div>
          </div>

          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-gray-100">
            <h3 className="text-xl font-bold text-gray-800 mb-6">{t('dashboard.suggestions')}</h3>
            <div className="space-y-4">
              <div className="p-4 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl border border-emerald-200">
                <h4 className="font-semibold text-emerald-800 mb-2">{t('dashboard.biogasProduction.title')}</h4>
                <p className="text-emerald-700 text-sm">
                  {t('dashboard.biogasProduction.description')}
                </p>
              </div>
              
              <div className="p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl border border-blue-200">
                <h4 className="font-semibold text-blue-800 mb-2">{t('dashboard.compostFertilizer.title')}</h4>
                <p className="text-blue-700 text-sm">
                  {t('dashboard.compostFertilizer.description')}
                </p>
              </div>
              
              <div className="p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl border border-purple-200">
                <h4 className="font-semibold text-purple-800 mb-2">{t('dashboard.carbonCredits.title')}</h4>
                <p className="text-purple-700 text-sm">
                  {t('dashboard.carbonCredits.description')}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading, firebaseUser, user } = useAuth();
  const location = useLocation();

  console.log('🛡️ ProtectedRoute check:', { isAuthenticated, loading, hasFirebaseUser: !!firebaseUser, hasUser: !!user });

  // Only show loading if we're truly waiting for auth (no user data at all)
  if (loading && !firebaseUser && !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Authenticating...</p>
        </div>
      </div>
    );
  }

  // If we have Firebase user or cached user, consider authenticated
  if (!isAuthenticated && !firebaseUser && !user) {
    console.log('🚨 Not authenticated, redirecting to login');
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  console.log('✅ Authenticated, rendering protected content');
  return children;
};

export default ProtectedRoute;

import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const AuthDebug = () => {
  const { user, firebaseUser, isAuthenticated, loading } = useAuth();

  if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    return (
      <div className="fixed bottom-4 right-4 bg-black bg-opacity-75 text-white p-4 rounded-lg text-xs max-w-sm z-50">
        <h4 className="font-bold mb-2">🔥 Auth Debug</h4>
        <div className="space-y-1">
          <div>Loading: {loading ? '✅' : '❌'}</div>
          <div>Firebase User: {firebaseUser ? '✅' : '❌'}</div>
          <div>User Object: {user ? '✅' : '❌'}</div>
          <div>Is Authenticated: {isAuthenticated ? '✅' : '❌'}</div>
          {user && (
            <div className="mt-2 pt-2 border-t border-gray-600">
              <div>Email: {user.email}</div>
              <div>UID: {user.id?.substring(0, 8)}...</div>
            </div>
          )}
        </div>
      </div>
    );
  }
  
  return null;
};

export default AuthDebug;

import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getAuthStatus } from '../services/api';

const AuthTest = () => {
  const { user, firebaseUser, isAuthenticated, loading, getToken } = useAuth();
  const [backendStatus, setBackendStatus] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const testBackend = async () => {
      try {
        const status = await getAuthStatus();
        setBackendStatus(status.data);
      } catch (error) {
        console.error('Backend test failed:', error);
        setBackendStatus({ error: error.message });
      }
    };

    const getTokenTest = async () => {
      if (firebaseUser) {
        try {
          const userToken = await getToken();
          setToken(userToken ? userToken.substring(0, 50) + '...' : null);
        } catch (error) {
          console.error('Token test failed:', error);
        }
      }
    };

    testBackend();
    getTokenTest();
  }, [firebaseUser, getToken]);

  if (loading) {
    return <div>Loading authentication...</div>;
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">🔥 Firebase Authentication Test</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Firebase Status */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-3">Firebase Status</h2>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>Loading:</span>
              <span className={loading ? 'text-yellow-600' : 'text-green-600'}>
                {loading ? '⏳ Yes' : '✅ No'}
              </span>
            </div>
            <div className="flex justify-between">
              <span>Firebase User:</span>
              <span className={firebaseUser ? 'text-green-600' : 'text-red-600'}>
                {firebaseUser ? '✅ Yes' : '❌ No'}
              </span>
            </div>
            <div className="flex justify-between">
              <span>User Object:</span>
              <span className={user ? 'text-green-600' : 'text-red-600'}>
                {user ? '✅ Yes' : '❌ No'}
              </span>
            </div>
            <div className="flex justify-between">
              <span>Is Authenticated:</span>
              <span className={isAuthenticated ? 'text-green-600' : 'text-red-600'}>
                {isAuthenticated ? '✅ Yes' : '❌ No'}
              </span>
            </div>
          </div>
          
          {user && (
            <div className="mt-4 pt-4 border-t">
              <h3 className="font-semibold mb-2">User Details:</h3>
              <div className="text-sm space-y-1">
                <div>Email: {user.email}</div>
                <div>UID: {user.id}</div>
                <div>Name: {user.name}</div>
                <div>Email Verified: {user.emailVerified ? '✅' : '❌'}</div>
              </div>
            </div>
          )}
        </div>

        {/* Backend Status */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-3">Backend Status</h2>
          {backendStatus ? (
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Backend Connected:</span>
                <span className="text-green-600">✅ Yes</span>
              </div>
              <div className="flex justify-between">
                <span>Backend Auth:</span>
                <span className={backendStatus.authenticated ? 'text-green-600' : 'text-orange-600'}>
                  {backendStatus.authenticated ? '✅ Authenticated' : '⚠️ Anonymous'}
                </span>
              </div>
              <div className="text-sm text-gray-600">
                Message: {backendStatus.message}
              </div>
            </div>
          ) : (
            <div className="text-gray-500">Loading backend status...</div>
          )}
          
          {token && (
            <div className="mt-4 pt-4 border-t">
              <h3 className="font-semibold mb-2">Firebase Token:</h3>
              <div className="text-xs bg-gray-100 p-2 rounded">
                {token}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-6 flex gap-4">
        <button
          onClick={() => window.location.href = '/login'}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Go to Login
        </button>
        <button
          onClick={() => window.location.href = '/dashboard'}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Go to Dashboard
        </button>
      </div>
    </div>
  );
};

export default AuthTest;

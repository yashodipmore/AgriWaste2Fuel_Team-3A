import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const RouteTest = () => {
  const { isAuthenticated, user, loading } = useAuth();
  const navigate = useNavigate();

  const testRoutes = [
    { path: '/', label: 'Home' },
    { path: '/about', label: 'About' },
    { path: '/login', label: 'Login' },
    { path: '/register', label: 'Register' },
    { path: '/input', label: 'Analysis (Protected)' },
    { path: '/dashboard', label: 'Dashboard (Protected)' },
    { path: '/result', label: 'Result (Protected)' }
  ];

  const navigateToRoute = (path) => {
    navigate(path);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">🧭 Route Testing Dashboard</h1>
      
      {/* Auth Status */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-3">Authentication Status</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="font-medium">Loading:</span>
            <span className={`ml-2 ${loading ? 'text-yellow-600' : 'text-green-600'}`}>
              {loading ? '⏳ Yes' : '✅ No'}
            </span>
          </div>
          <div>
            <span className="font-medium">Authenticated:</span>
            <span className={`ml-2 ${isAuthenticated ? 'text-green-600' : 'text-red-600'}`}>
              {isAuthenticated ? '✅ Yes' : '❌ No'}
            </span>
          </div>
          {user && (
            <div className="col-span-2">
              <span className="font-medium">User:</span>
              <span className="ml-2 text-blue-600">{user.email}</span>
            </div>
          )}
        </div>
      </div>

      {/* Route Testing */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-3">Route Navigation Test</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {testRoutes.map((route) => (
            <button
              key={route.path}
              onClick={() => navigateToRoute(route.path)}
              className={`p-3 rounded-lg border text-left transition-all ${
                route.path.includes('(Protected)') && !isAuthenticated
                  ? 'border-red-300 bg-red-50 text-red-700 cursor-not-allowed'
                  : 'border-gray-300 bg-gray-50 hover:bg-blue-50 hover:border-blue-300'
              }`}
              disabled={route.path.includes('(Protected)') && !isAuthenticated}
            >
              <div className="font-medium">{route.label}</div>
              <div className="text-sm text-gray-500">{route.path}</div>
            </button>
          ))}
        </div>
        
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h3 className="font-medium text-yellow-800 mb-1">Expected Behavior:</h3>
          <ul className="text-sm text-yellow-700 space-y-1">
            <li>• If NOT logged in: Protected routes → Redirect to /login</li>
            <li>• If logged in: /login or /register → Redirect to /input</li>
            <li>• Login success → Redirect to /input (Analysis page)</li>
            <li>• Register success → Redirect to /input (Analysis page)</li>
          </ul>
        </div>
      </div>

      {/* Debug Info */}
      <div className="mt-6 bg-gray-100 p-4 rounded-lg">
        <h2 className="text-lg font-semibold mb-3">🔍 Debug Information</h2>
        <div className="text-sm space-y-1">
          <div>Current URL: <code>{window.location.pathname}</code></div>
          <div>Expected Default: <code>/input</code> (Analysis page)</div>
          <div>Auth Status: <code>{isAuthenticated ? 'AUTHENTICATED' : 'NOT_AUTHENTICATED'}</code></div>
          <div>Loading State: <code>{loading ? 'LOADING' : 'READY'}</code></div>
        </div>
      </div>
    </div>
  );
};

export default RouteTest;

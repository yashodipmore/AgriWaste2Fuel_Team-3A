import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const SimpleTest = () => {
  const { user, isAuthenticated, loading } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-2xl font-bold mb-4">🧪 Simple Dashboard Test</h1>
        
        <div className="space-y-3">
          <div className="p-3 bg-gray-50 rounded">
            <strong>Loading:</strong> {loading ? 'Yes' : 'No'}
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <strong>Authenticated:</strong> {isAuthenticated ? 'Yes' : 'No'}
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <strong>User:</strong> {user ? user.email : 'None'}
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <strong>Current Path:</strong> {window.location.pathname}
          </div>
        </div>

        <div className="mt-6 space-x-4">
          <Link to="/dashboard" className="bg-blue-500 text-white px-4 py-2 rounded">
            Go to Real Dashboard
          </Link>
          <Link to="/input" className="bg-green-500 text-white px-4 py-2 rounded">
            Go to Analysis
          </Link>
          <Link to="/" className="bg-gray-500 text-white px-4 py-2 rounded">
            Go to Home
          </Link>
        </div>

        {!isAuthenticated && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded">
            <p className="text-red-700">Not authenticated! You should be redirected to login.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SimpleTest;

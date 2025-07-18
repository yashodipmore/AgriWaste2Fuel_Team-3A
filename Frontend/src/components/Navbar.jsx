import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';
import LanguageSelector from './LanguageSelector';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const { t } = useTranslation();
  const { user, logout } = useAuth();

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    logout();
    setIsOpen(false);
  };

  return (
    <nav className="bg-white/90 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 flex items-center justify-center">
              <img 
                src="/AgriLogo.png" 
                alt="AgriWaste2Fuel Logo" 
                className="w-10 h-10 object-contain"
              />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              {t('navbar.logo')}
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              to="/" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive('/') 
                  ? 'bg-emerald-100 text-emerald-700' 
                  : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
              }`}
            >
              {t('navbar.home')}
            </Link>
            <Link 
              to="/input" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive('/input') 
                  ? 'bg-emerald-100 text-emerald-700' 
                  : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
              }`}
            >
              {t('navbar.analysis')}
            </Link>
            <Link 
              to="/about" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive('/about') 
                  ? 'bg-emerald-100 text-emerald-700' 
                  : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
              }`}
            >
              {t('navbar.about')}
            </Link>
            <LanguageSelector />
            
            {user ? (
              // Authenticated user navigation
              <>
                <Link 
                  to="/dashboard" 
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    isActive('/dashboard') 
                      ? 'bg-emerald-100 text-emerald-700' 
                      : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
                  }`}
                >
                  Dashboard
                </Link>
                <div className="flex items-center space-x-3">
                  <span className="text-sm text-gray-600">Welcome, {user.name}</span>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 rounded-lg font-medium border border-red-500 text-red-600 hover:bg-red-50 hover:border-red-600 transition-all duration-200"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              // Guest navigation
              <>
                <Link 
                  to="/login" 
                  className={`px-4 py-2 rounded-lg font-medium border border-emerald-600 transition-all duration-200 ${
                    isActive('/login') 
                      ? 'bg-emerald-100 text-emerald-700 border-emerald-700' 
                      : 'text-emerald-600 hover:bg-emerald-50 hover:border-emerald-700'
                  }`}
                >
                  {t('navbar.login')}
                </Link>
                <Link 
                  to="/register" 
                  className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 rounded-lg text-gray-600 hover:text-emerald-600 hover:bg-emerald-50 transition-colors duration-200"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-2">
            <Link 
              to="/" 
              onClick={() => setIsOpen(false)}
              className={`block px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                isActive('/') 
                  ? 'bg-emerald-100 text-emerald-700' 
                  : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
              }`}
            >
              {t('navbar.home')}
            </Link>
            <Link 
              to="/input" 
              onClick={() => setIsOpen(false)}
              className={`block px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                isActive('/input') 
                  ? 'bg-emerald-100 text-emerald-700' 
                  : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
              }`}
            >
              {t('navbar.analysis')}
            </Link>
            <Link 
              to="/about" 
              onClick={() => setIsOpen(false)}
              className={`block px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                isActive('/about') 
                  ? 'bg-emerald-100 text-emerald-700' 
                  : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
              }`}
            >
              {t('navbar.about')}
            </Link>
            <div className="px-4 py-2">
              <LanguageSelector />
            </div>
            
            {user ? (
              // Authenticated user mobile navigation
              <>
                <Link 
                  to="/dashboard" 
                  onClick={() => setIsOpen(false)}
                  className={`block px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                    isActive('/dashboard') 
                      ? 'bg-emerald-100 text-emerald-700' 
                      : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
                  }`}
                >
                  Dashboard
                </Link>
                <div className="px-4 py-3 text-sm text-gray-600">
                  Welcome, {user.name}
                </div>
                <button
                  onClick={handleLogout}
                  className="block w-full px-4 py-3 rounded-lg font-medium border border-red-500 text-red-600 hover:bg-red-50 hover:border-red-600 text-center transition-all duration-200"
                >
                  Logout
                </button>
              </>
            ) : (
              // Guest mobile navigation
              <>
                <Link 
                  to="/login" 
                  onClick={() => setIsOpen(false)}
                  className={`block px-4 py-3 rounded-lg font-medium border border-emerald-600 text-center transition-all duration-200 ${
                    isActive('/login') 
                      ? 'bg-emerald-100 text-emerald-700 border-emerald-700' 
                      : 'text-emerald-600 hover:bg-emerald-50 hover:border-emerald-700'
                  }`}
                >
                  {t('navbar.login')}
                </Link>
                <Link 
                  to="/register" 
                  onClick={() => setIsOpen(false)}
                  className="block bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-3 rounded-lg font-semibold text-center mt-4"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;

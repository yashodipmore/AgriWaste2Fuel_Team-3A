import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Register = () => {
  const { register, error } = useAuth();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    phoneNumber: '',
    location: '',
    farmSize: '',
    cropTypes: '',
    agreeTerms: false
  });
  const [isLoading, setIsLoading] = useState(false);
  const [localErrors, setLocalErrors] = useState({});
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    // Clear error when user starts typing
    if (localErrors[name]) {
      setLocalErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.fullName.trim()) {
      newErrors.fullName = 'Full name is required';
    }
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    if (!formData.phoneNumber) {
      newErrors.phoneNumber = 'Phone number is required';
    }
    
    if (!formData.location.trim()) {
      newErrors.location = 'Location is required';
    }
    
    if (!formData.agreeTerms) {
      newErrors.agreeTerms = 'You must agree to the terms and conditions';
    }
    
    setLocalErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    setLocalErrors({});
    
    try {
      const result = await register({
        name: formData.fullName,
        email: formData.email,
        password: formData.password,
        phoneNumber: formData.phoneNumber,
        location: formData.location,
        farmSize: formData.farmSize,
        cropTypes: formData.cropTypes
      });
      
      if (result.success) {
        // Registration successful, navigate to analysis page
        navigate('/input');
      } else {
        // Handle registration error
        setLocalErrors({ submit: result.error });
      }
    } catch (err) {
      console.error('Registration failed:', err);
      setLocalErrors({ submit: 'Registration failed. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-100/20 to-cyan-100/20"></div>
      <div className="absolute top-10 right-10 w-72 h-72 bg-emerald-200/30 rounded-full blur-3xl"></div>
      <div className="absolute bottom-10 left-10 w-96 h-96 bg-cyan-200/30 rounded-full blur-3xl"></div>
      
      <div className="relative z-10 flex items-center justify-center min-h-screen py-12 px-4">
        <div className="max-w-2xl w-full">
          {/* Register Card */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8 border border-gray-100">
            {/* Header */}
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center mb-4 mx-auto">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
              </div>
              <h2 className="text-3xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent mb-2">
                किसान रजिस्ट्रेशन
              </h2>
              <p className="text-gray-600">अपना नया खाता बनाएं और शुरू करें</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Display auth error if any */}
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                  {error}
                </div>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Full Name */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    पूरा नाम *
                  </label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    placeholder="आपका पूरा नाम"
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200 ${
                      localErrors.fullName ? 'border-red-400' : 'border-gray-200'
                    }`}
                  />
                  {localErrors.fullName && <p className="text-red-500 text-sm mt-1">{localErrors.fullName}</p>}
                </div>

                {/* Email */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ईमेल पता *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="your@email.com"
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200 ${
                      localErrors.email ? 'border-red-400' : 'border-gray-200'
                    }`}
                  />
                  {localErrors.email && <p className="text-red-500 text-sm mt-1">{localErrors.email}</p>}
                </div>

                {/* Phone Number */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    फोन नंबर *
                  </label>
                  <input
                    type="tel"
                    name="phoneNumber"
                    value={formData.phoneNumber}
                    onChange={handleInputChange}
                    placeholder="+91 9876543210"
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200 ${
                      localErrors.phoneNumber ? 'border-red-400' : 'border-gray-200'
                    }`}
                  />
                  {localErrors.phoneNumber && <p className="text-red-500 text-sm mt-1">{localErrors.phoneNumber}</p>}
                </div>

                {/* Location */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    स्थान *
                  </label>
                  <input
                    type="text"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    placeholder="गांव, जिला, राज्य"
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200 ${
                      localErrors.location ? 'border-red-400' : 'border-gray-200'
                    }`}
                  />
                  {localErrors.location && <p className="text-red-500 text-sm mt-1">{localErrors.location}</p>}
                </div>

                {/* Farm Size */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    खेत का आकार (एकड़ में)
                  </label>
                  <select
                    name="farmSize"
                    value={formData.farmSize}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200"
                  >
                    <option value="">चुनें</option>
                    <option value="0-1">0-1 एकड़</option>
                    <option value="1-5">1-5 एकड़</option>
                    <option value="5-10">5-10 एकड़</option>
                    <option value="10-50">10-50 एकड़</option>
                    <option value="50+">50+ एकड़</option>
                  </select>
                </div>

                {/* Crop Types */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    मुख्य फसलें
                  </label>
                  <input
                    type="text"
                    name="cropTypes"
                    value={formData.cropTypes}
                    onChange={handleInputChange}
                    placeholder="जैसे: गेहूं, धान, मक्का"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200"
                  />
                </div>
              </div>

              {/* Password Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    पासवर्ड *
                  </label>
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="कम से कम 6 अक्षर"
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200 ${
                      localErrors.password ? 'border-red-400' : 'border-gray-200'
                    }`}
                  />
                  {localErrors.password && <p className="text-red-500 text-sm mt-1">{localErrors.password}</p>}
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    पासवर्ड दोबारा दर्ज करें *
                  </label>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    placeholder="पासवर्ड दोबारा दर्ज करें"
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all duration-200 ${
                      localErrors.confirmPassword ? 'border-red-400' : 'border-gray-200'
                    }`}
                  />
                  {localErrors.confirmPassword && <p className="text-red-500 text-sm mt-1">{localErrors.confirmPassword}</p>}
                </div>
              </div>

              {/* Terms and Conditions */}
              <div>
                <label className="flex items-start">
                  <input
                    type="checkbox"
                    name="agreeTerms"
                    checked={formData.agreeTerms}
                    onChange={handleInputChange}
                    className="w-4 h-4 text-emerald-600 bg-gray-100 border-gray-300 rounded focus:ring-emerald-500 focus:ring-2 mt-1"
                  />
                  <span className="ml-3 text-sm text-gray-600">
                    मैं{' '}
                    <Link to="/terms" className="text-emerald-600 hover:text-emerald-700 font-medium">
                      नियम और शर्तों
                    </Link>{' '}
                    और{' '}
                    <Link to="/privacy" className="text-emerald-600 hover:text-emerald-700 font-medium">
                      गोपनीयता नीति
                    </Link>{' '}
                    से सहमत हूं।
                  </span>
                </label>
                {localErrors.agreeTerms && <p className="text-red-500 text-sm mt-1">{localErrors.agreeTerms}</p>}
              </div>

              {/* Error Display */}
              {localErrors.submit && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-700 text-sm">{localErrors.submit}</p>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className={`w-full py-3 px-6 rounded-xl font-semibold transition-all duration-300 flex items-center justify-center ${
                  isLoading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 transform hover:scale-105 shadow-lg hover:shadow-xl'
                } text-white`}
              >
                {isLoading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    रजिस्टर हो रहा है...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    रजिस्टर करें
                  </>
                )}
              </button>
            </form>

            {/* Login Link */}
            <div className="text-center mt-6">
              <p className="text-gray-600">
                क्या आपका पहले से खाता है?{' '}
                <Link to="/login" className="text-emerald-600 hover:text-emerald-700 font-semibold transition-colors duration-200">
                  यहाँ लॉगिन करें
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;

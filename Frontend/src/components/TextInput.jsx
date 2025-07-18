import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';
import * as api from '../services/api';
import { getLocalAnalysis, getCachedData, setCachedData } from '../utils/performance';

const TextInput = () => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [wasteType, setWasteType] = useState('');
  const [quantity, setQuantity] = useState('1000');
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const wasteCategories = [
    { name: t('textInput.categories.riceStraw'), icon: '🌾', description: t('textInput.categories.riceStrawDesc') },
    { name: t('textInput.categories.wheatStubble'), icon: '🌾', description: t('textInput.categories.wheatStubbleDesc') },
    { name: t('textInput.categories.cornHusks'), icon: '🌽', description: t('textInput.categories.cornHusksDesc') },
    { name: t('textInput.categories.sugarcaneBagasse'), icon: '🎋', description: t('textInput.categories.sugarcaneBagasseDesc') },
    { name: t('textInput.categories.cottonStalks'), icon: '🌿', description: t('textInput.categories.cottonStalksDesc') },
    { name: t('textInput.categories.bananaLeaves'), icon: '🍌', description: t('textInput.categories.bananaLeavesDesc') }
  ];

  const handleSubmit = async () => {
    if (!wasteType.trim()) {
      setError(t('textInput.enterWasteType'));
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Prepare data for text-based analysis
      const analysisData = {
        waste_type: wasteType.trim(),
        quantity: parseInt(quantity) || 1000,
        location: location.trim(),
        user_id: user?.id,
        timestamp: new Date().toISOString()
      };
      
      // Check cache first for faster response
      const cacheKey = `text_${analysisData.waste_type}_${analysisData.quantity}`;
      const cachedResult = getCachedData(cacheKey);
      
      if (cachedResult) {
        console.log('Using cached analysis result');
        setLoading(false);
        navigate('/result', { 
          state: { 
            ...cachedResult,
            method: 'text',
            cached: true
          }
        });
        return;
      }
      
      // TEMPORARY: Skip API call and use fallback data for debugging
      console.log("🔍 SKIPPING API - Using fallback data for debugging");
      
      // Simulate successful response
      const analysisResult = {
        waste_type: analysisData.waste_type,
        confidence: 85,
        quantity: analysisData.quantity,
        matched_category: "Agricultural Waste",
        suggestions: ["Rice Straw", "Wheat Straw", "Corn Stalks"]
      };
      
      // Cache the result for future use
      setCachedData(cacheKey, {
        wasteType: analysisResult.waste_type || analysisData.waste_type,
        confidence: analysisResult.confidence || 90,
        quantity: analysisResult.quantity || analysisData.quantity,
        location: analysisResult.location || analysisData.location
      });
      
      setLoading(false);
      
      // Navigate to results with analysis data
      navigate('/result', { 
        state: { 
          wasteType: analysisResult.waste_type || analysisData.waste_type,
          confidence: analysisResult.confidence || 90,
          quantity: analysisResult.quantity || analysisData.quantity,
          location: analysisResult.location || analysisData.location,
          method: 'text',
          apiResponse: true
        }
      });
      
    } catch (err) {
      console.error('Text analysis failed:', err);
      setLoading(false);
      setError(err.response?.data?.message || 'Analysis failed. Please try again.');
    }
  };

  const selectWasteType = (waste) => {
    setWasteType(waste);
    setError(null); // Clear any existing errors
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8 border border-gray-100">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-2xl flex items-center justify-center mb-4 mx-auto">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-gray-800 mb-2">{t('textInput.title')}</h3>
          <p className="text-gray-600">{t('textInput.subtitle')}</p>
        </div>
        
        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              {error}
            </div>
          </div>
        )}
        
        <div className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            {t('textInput.wasteTypeLabel')} *
          </label>
          <div className="relative">
            <input
              type="text"
              value={wasteType}
              onChange={(e) => setWasteType(e.target.value)}
              placeholder={t('textInput.placeholder')}
              className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-cyan-100 focus:border-cyan-400 outline-none transition-all duration-200 text-lg"
            />
            {wasteType && (
              <button
                onClick={() => setWasteType('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* Quantity Input */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Estimated Quantity (kg)
          </label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            placeholder="1000"
            min="1"
            className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-cyan-100 focus:border-cyan-400 outline-none transition-all duration-200 text-lg"
          />
        </div>

        {/* Location Input */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Location (Optional)
          </label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g., Punjab, Maharashtra"
            className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-cyan-100 focus:border-cyan-400 outline-none transition-all duration-200 text-lg"
          />
        </div>
        </div>

        <div className="mb-8">
          <p className="text-sm font-semibold text-gray-700 mb-4">{t('textInput.quickSelect')}:</p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {wasteCategories.map((waste, index) => (
              <button
                key={index}
                onClick={() => selectWasteType(waste.name)}
                className={`p-3 rounded-xl border-2 transition-all duration-200 hover:scale-105 ${
                  wasteType === waste.name
                    ? 'border-cyan-400 bg-cyan-50'
                    : 'border-gray-200 hover:border-cyan-300 hover:bg-cyan-50/50'
                }`}
              >
                <div className="text-2xl mb-1">{waste.icon}</div>
                <div className="text-sm font-medium text-gray-800">{waste.name}</div>
                <div className="text-xs text-gray-500 mt-1">{waste.description}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-cyan-50 rounded-xl p-4 mb-6">
          <div className="flex items-start">
            <svg className="w-5 h-5 text-cyan-600 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="text-sm font-medium text-cyan-800 mb-1">{t('textInput.proTip')}:</p>
              <p className="text-sm text-cyan-700">
                {t('textInput.proTipDescription')}
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={handleSubmit}
          disabled={!wasteType.trim() || loading}
          className={`w-full py-4 px-6 rounded-xl font-semibold transition-all duration-300 flex items-center justify-center ${
            !wasteType.trim() || loading
              ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
          }`}
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {t('textInput.processing')}
            </>
          ) : (
            <>
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {t('textInput.analyzeWaste')}
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default TextInput;

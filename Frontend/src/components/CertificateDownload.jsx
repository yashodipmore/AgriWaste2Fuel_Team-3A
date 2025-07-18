import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import * as api from '../services/api';

const CertificateDownload = ({ wasteType, co2Saved, carbonCredits, value, analysisId, userId }) => {
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  const handleDownload = async () => {
    if (!user) {
      setError('Please login to download certificate');
      return;
    }

    setDownloading(true);
    setError(null);
    
    try {
      // Prepare certificate data
      const certificateData = {
        analysis_id: analysisId,
        user_name: user?.name || user?.displayName || 'User',
        waste_type: wasteType,
        co2_saved: parseFloat(String(co2Saved).replace(/[^\d.-]/g, '')) || 0, // Extract number from string
        carbon_credits: parseFloat(String(carbonCredits).replace(/[^\d.-]/g, '')) || 0, // Extract number from string
        processing_method: 'Anaerobic Digestion' // Default processing method
      };
      
      // Backend API call for certificate generation
      const response = await api.generateCertificate(certificateData);
      
      // Create PDF blob from response
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `AgriWaste2Fuel_Certificate_${analysisId || Date.now()}.pdf`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (err) {
      console.error('Certificate download failed:', err);
      setError(err.response?.data?.message || err.message || 'Certificate generation requires backend implementation');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="text-center">
      {/* Error Display */}
      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <div className="flex items-center justify-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            {error}
          </div>
        </div>
      )}
      
      <button
        onClick={handleDownload}
        disabled={downloading || !user}
        className={`font-semibold py-3 px-6 rounded-lg shadow-lg transform transition-all duration-200 inline-flex items-center ${
          downloading
            ? 'bg-gray-400 cursor-not-allowed text-white'
            : !user 
            ? 'bg-gray-300 cursor-not-allowed text-gray-500'
            : 'bg-blue-600 hover:bg-blue-700 text-white hover:scale-105'
        }`}
      >
        {downloading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating Certificate...
          </>
        ) : (
          <>
            <svg 
              className="w-5 h-5 mr-2" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
              />
            </svg>
            Download Certificate
          </>
        )}
      </button>
      
      <p className="text-sm text-gray-600 mt-2">
        {user 
          ? 'Get your sustainability certificate in PDF format'
          : 'Please login to download your certificate'
        }
      </p>
      
      {user && (
        <div className="mt-4 text-xs text-gray-500">
          Certificate will be generated for: {user.name}
        </div>
      )}
    </div>
  );
};

export default CertificateDownload;

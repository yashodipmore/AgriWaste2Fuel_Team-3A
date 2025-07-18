import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import * as api from '../services/api';
import { optimizeImage, getLocalAnalysis } from '../utils/performance';

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    processFile(file);
  };

  const processFile = async (file) => {
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file');
        return;
      }
      
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('Image size should be less than 10MB');
        return;
      }
      
      setError(null);
      
      // Optimize image for faster processing
      try {
        const optimizedFile = await optimizeImage(file);
        setSelectedFile(optimizedFile);
        const reader = new FileReader();
        reader.onload = (e) => setPreview(e.target.result);
        reader.readAsDataURL(optimizedFile);
      } catch (error) {
        // Fallback to original file if optimization fails
        setSelectedFile(file);
        const reader = new FileReader();
        reader.onload = (e) => setPreview(e.target.result);
        reader.readAsDataURL(file);
      }
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Create FormData for image upload
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      // Add user info if available
      if (user) {
        formData.append('userId', user.id);
      }
      
      // Backend API call for image prediction with shorter timeout
      try {
        // Reduce timeout to 3 seconds for image processing (was 7 seconds)
        const timeoutPromise = new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Image analysis timeout')), 3000)
        );
        
        const apiPromise = api.predictImage(formData);
        
        // Race between API call and timeout
        const response = await Promise.race([apiPromise, timeoutPromise]);
        const analysisResult = response.data;
        
        setLoading(false);
        
        // Navigate to results with analysis data
        navigate('/result', { 
          state: { 
            wasteType: analysisResult.waste_type || 'Agricultural Waste',
            confidence: analysisResult.confidence || 80,
            quantity: analysisResult.quantity || 1000,
            method: 'image',
            filename: selectedFile.name,
            imageData: selectedFile,
            timestamp: new Date().toISOString(),
            userId: user?.id,
            apiResponse: true
          }
        });
        
      } catch (apiError) {
        console.log('Image API not available, using basic analysis:', apiError.message);
        
        // Quick fallback: basic image analysis based on filename
        const basicAnalysis = analyzeImageFilename(selectedFile.name);
        
        setLoading(false);
        navigate('/result', { 
          state: { 
            wasteType: basicAnalysis.wasteType,
            confidence: basicAnalysis.confidence,
            quantity: 1000,
            method: 'image',
            filename: selectedFile.name,
            imageData: selectedFile,
            timestamp: new Date().toISOString(),
            userId: user?.id,
            fallback: true // Flag to show this was fallback analysis
          }
        });
      }
      
    } catch (err) {
      console.error('Image analysis failed:', err);
      setLoading(false);
      setError(err.response?.data?.message || 'Image analysis failed. Please try again.');
    }
  };

  // Basic image analysis based on filename (fallback)
  const analyzeImageFilename = (filename) => {
    const name = filename.toLowerCase();
    
    if (name.includes('rice') || name.includes('straw')) {
      return { wasteType: 'Rice Straw', confidence: 75 };
    } else if (name.includes('wheat')) {
      return { wasteType: 'Wheat Straw', confidence: 75 };
    } else if (name.includes('corn') || name.includes('maize')) {
      return { wasteType: 'Corn Stalks', confidence: 70 };
    } else if (name.includes('cotton')) {
      return { wasteType: 'Cotton Waste', confidence: 70 };
    } else {
      return { wasteType: 'Agricultural Waste', confidence: 60 };
    }
  };

  const resetUpload = () => {
    setSelectedFile(null);
    setPreview(null);
    setError(null);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl p-10 border border-gray-100">
        <div className="text-center mb-10">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-3xl flex items-center justify-center mb-6 mx-auto shadow-lg">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-3xl font-bold text-gray-800 mb-3">Upload Agricultural Waste Image</h3>
          <p className="text-gray-600 text-lg">Upload a clear, high-quality image of your agricultural waste for accurate AI analysis</p>
        </div>
        
        {/* Error Display */}
        {error && (
          <div className="mb-8 bg-red-50 border-l-4 border-red-400 text-red-700 px-6 py-4 rounded-r-xl shadow-md">
            <div className="flex items-center">
              <svg className="w-6 h-6 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <span className="font-medium">{error}</span>
            </div>
          </div>
        )}
        
        {!preview ? (
          <div
            className={`relative border-2 border-dashed rounded-3xl p-16 text-center transition-all duration-300 ${
              dragActive 
                ? 'border-blue-400 bg-blue-50/70 scale-[1.02]' 
                : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50/50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              id="file-upload"
            />
            
            <div className="space-y-6">
              <div className="w-24 h-24 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full flex items-center justify-center mx-auto shadow-lg">
                <svg className="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              
              <div>
                <p className="text-2xl font-bold text-gray-700 mb-3">
                  Drop your image here, or <span className="text-blue-600 hover:text-blue-700 cursor-pointer">browse</span>
                </p>
                <p className="text-gray-500 text-lg">
                  Supports JPG, PNG, GIF up to 10MB
                </p>
                <p className="text-gray-400 text-sm mt-2">
                  For best results, ensure good lighting and clear visibility of waste materials
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            <div className="relative group">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-80 object-cover rounded-2xl shadow-xl border border-gray-200"
              />
              <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl flex items-center justify-center">
                <button
                  onClick={resetUpload}
                  className="bg-red-500 hover:bg-red-600 text-white p-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-110"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <button
                onClick={resetUpload}
                className="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg transition-colors duration-200 md:opacity-0 md:group-hover:opacity-100"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="bg-green-50 border-l-4 border-green-400 rounded-r-2xl p-6 shadow-md">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h4 className="text-lg font-semibold text-green-800">Image uploaded successfully!</h4>
                  <p className="text-green-700 mt-1">
                    <span className="font-medium">File:</span> {selectedFile?.name}
                  </p>
                  <p className="text-green-700">
                    <span className="font-medium">Size:</span> {(selectedFile?.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <p className="text-green-600 text-sm mt-2">
                    Ready for AI analysis. Click "Analyze Waste" to continue.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="mt-10">
          <button
            onClick={handleSubmit}
            disabled={!selectedFile || loading}
            className={`w-full py-5 px-8 rounded-2xl font-bold text-lg transition-all duration-300 flex items-center justify-center shadow-lg ${
              !selectedFile || loading
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white shadow-xl hover:shadow-2xl transform hover:scale-[1.02]'
            }`}
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Analyzing Image...</span>
              </>
            ) : (
              <>
                <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span>Analyze Agricultural Waste</span>
              </>
            )}
          </button>
          
          {!selectedFile && (
            <p className="text-center text-gray-500 mt-4 text-sm">
              Please upload an image to enable analysis
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;

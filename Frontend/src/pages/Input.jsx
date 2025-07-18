import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import ImageUpload from '../components/ImageUpload';
import TextInput from '../components/TextInput';

const Input = () => {
  const [activeTab, setActiveTab] = useState('image');
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 font-['Poppins',sans-serif] py-8">
      {/* Subtle background decoration */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-50/50 to-blue-50/30"></div>
      <div className="absolute top-20 left-20 w-72 h-72 bg-blue-100/20 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-emerald-100/20 rounded-full blur-3xl"></div>
      
      <div className="relative z-10 container mx-auto px-4">
        {/* Header Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center bg-white/90 backdrop-blur-sm rounded-full px-8 py-3 mb-8 shadow-lg border border-gray-100">
            <div className="w-3 h-3 bg-gradient-to-r from-emerald-400 to-blue-500 rounded-full mr-3 animate-pulse"></div>
            <span className="text-gray-700 font-semibold tracking-wide">{t('input.badge')}</span>
          </div>
          
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-gray-800 mb-6 tracking-tight px-4 sm:px-0">
            {t('input.title')} <span className="bg-gradient-to-r from-emerald-600 to-emerald-500 bg-clip-text text-transparent">{t('input.titleHighlight')}</span> {t('input.titleSuffix')}
          </h1>
          <p className="text-lg sm:text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed font-light px-4 sm:px-0">
            {t('input.description')}
          </p>
        </div>
        
        <div className="max-w-5xl mx-auto">
          {/* Tab Navigation */}
          <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl border border-gray-100 mb-12 p-2">
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setActiveTab('image')}
                className={`py-6 px-8 text-center font-semibold rounded-2xl transition-all duration-500 flex items-center justify-center group ${
                  activeTab === 'image'
                    ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-xl transform scale-[1.02]'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50 hover:scale-[1.01]'
                }`}
              >
                <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mr-4 transition-all duration-300 ${
                  activeTab === 'image' 
                    ? 'bg-white/20' 
                    : 'bg-blue-100 group-hover:bg-blue-200'
                }`}>
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div className="text-left">
                  <div className="text-xl font-bold">{t('input.tabs.image.title')}</div>
                  <div className={`text-sm font-normal ${
                    activeTab === 'image' ? 'text-white/90' : 'text-gray-500'
                  }`}>
                    {t('input.tabs.image.subtitle')}
                  </div>
                </div>
              </button>
              
              <button
                onClick={() => setActiveTab('text')}
                className={`py-6 px-8 text-center font-semibold rounded-2xl transition-all duration-500 flex items-center justify-center group ${
                  activeTab === 'text'
                    ? 'bg-gradient-to-r from-emerald-600 to-emerald-500 text-white shadow-xl transform scale-[1.02]'
                    : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50 hover:scale-[1.01]'
                }`}
              >
                <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mr-4 transition-all duration-300 ${
                  activeTab === 'text' 
                    ? 'bg-white/20' 
                    : 'bg-emerald-100 group-hover:bg-emerald-200'
                }`}>
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <div className="text-left">
                  <div className="text-xl font-bold">{t('input.tabs.text.title')}</div>
                  <div className={`text-sm font-normal ${
                    activeTab === 'text' ? 'text-white/90' : 'text-gray-500'
                  }`}>
                    {t('input.tabs.text.subtitle')}
                  </div>
                </div>
              </button>
            </div>
          </div>

          {/* Tab Content */}
          <div className="mb-16">
            {activeTab === 'image' ? <ImageUpload /> : <TextInput />}
          </div>

          {/* Process Information Cards */}
          <div className="grid lg:grid-cols-2 gap-8 mb-16">
            {/* How It Works */}
            <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl border border-gray-100 overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-blue-500 p-8">
                <h3 className="text-3xl font-bold text-white text-center">How It Works</h3>
              </div>
              <div className="p-8">
                <div className="space-y-8">
                  <div className="flex items-start group">
                    <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl mr-6 flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300">
                      1
                    </div>
                    <div className="pt-2">
                      <h4 className="text-xl font-bold text-gray-800 mb-2">Upload or Describe</h4>
                      <p className="text-gray-600 leading-relaxed">
                        Choose between uploading a clear image of your agricultural waste or providing a detailed text description of the waste type and quantity.
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start group">
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl mr-6 flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300">
                      2
                    </div>
                    <div className="pt-2">
                      <h4 className="text-xl font-bold text-gray-800 mb-2">AI Analysis</h4>
                      <p className="text-gray-600 leading-relaxed">
                        Our advanced AI algorithms analyze your input using computer vision and natural language processing to identify waste type and optimal processing methods.
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start group">
                    <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl mr-6 flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300">
                      3
                    </div>
                    <div className="pt-2">
                      <h4 className="text-xl font-bold text-gray-800 mb-2">Get Results</h4>
                      <p className="text-gray-600 leading-relaxed">
                        Receive comprehensive analysis including processing recommendations, environmental impact calculations, and carbon credit estimations.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* What You Get */}
            <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl border border-gray-100 overflow-hidden">
              <div className="bg-gradient-to-r from-emerald-600 to-emerald-500 p-8">
                <h3 className="text-3xl font-bold text-white text-center">What You Get</h3>
              </div>
              <div className="p-8">
                <div className="space-y-6">
                  <div className="flex items-center group hover:bg-gray-50 p-3 rounded-xl transition-all duration-300">
                    <div className="w-12 h-12 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                      <svg className="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div>
                      <span className="text-lg font-semibold text-gray-800">Waste Type Identification</span>
                      <p className="text-gray-600 text-sm">Accurate classification with confidence scores</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center group hover:bg-gray-50 p-3 rounded-xl transition-all duration-300">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <div>
                      <span className="text-lg font-semibold text-gray-800">Processing Recommendations</span>
                      <p className="text-gray-600 text-sm">Optimal methods for maximum value extraction</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center group hover:bg-gray-50 p-3 rounded-xl transition-all duration-300">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-purple-200 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                      <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div>
                      <span className="text-lg font-semibold text-gray-800">CO₂ Impact Analysis</span>
                      <p className="text-gray-600 text-sm">Environmental savings and carbon footprint</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center group hover:bg-gray-50 p-3 rounded-xl transition-all duration-300">
                    <div className="w-12 h-12 bg-gradient-to-br from-orange-100 to-orange-200 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                      <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                      </svg>
                    </div>
                    <div>
                      <span className="text-lg font-semibold text-gray-800">Carbon Credits & Value</span>
                      <p className="text-gray-600 text-sm">Monetary estimates and earning potential</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center group hover:bg-gray-50 p-3 rounded-xl transition-all duration-300">
                    <div className="w-12 h-12 bg-gradient-to-br from-teal-100 to-teal-200 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                      <svg className="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div>
                      <span className="text-lg font-semibold text-gray-800">Sustainability Certificate</span>
                      <p className="text-gray-600 text-sm">Verifiable environmental impact documentation</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Call to Action */}
          <div className="text-center">
            <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl border border-gray-100 p-12">
              <div className="max-w-3xl mx-auto">
                <h2 className="text-4xl font-bold text-gray-800 mb-6">Ready to Get Started?</h2>
                <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                  Join thousands of farmers who are already transforming their agricultural waste into sustainable energy and earning carbon credits through our AI-powered platform.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <button 
                    onClick={() => setActiveTab('image')}
                    className="bg-gradient-to-r from-blue-600 to-blue-500 text-white px-8 py-4 rounded-2xl font-semibold text-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 flex items-center justify-center"
                  >
                    <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Upload Image
                  </button>
                  <button 
                    onClick={() => setActiveTab('text')}
                    className="bg-white text-emerald-600 border-2 border-emerald-500 px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-emerald-50 hover:border-emerald-600 transform hover:scale-105 transition-all duration-300 flex items-center justify-center"
                  >
                    <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Describe Waste
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Input;

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const Home = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative pt-16 pb-20 px-4 bg-gradient-to-br from-gray-50 via-white to-emerald-50/30">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_24%,rgba(34,197,94,0.05)_25%,rgba(34,197,94,0.05)_26%,transparent_27%,transparent_74%,rgba(34,197,94,0.05)_75%,rgba(34,197,94,0.05)_76%,transparent_77%)] bg-[length:20px_20px]"></div>
        <div className="max-w-7xl mx-auto relative">
          <div className="text-center mb-20">
            <div className="inline-flex items-center bg-gradient-to-r from-emerald-50 to-green-50 border border-emerald-200 text-emerald-700 px-8 py-3 rounded-full text-sm font-bold mb-8 shadow-md hover:shadow-lg transition-all duration-300 backdrop-blur-sm">
              <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full mr-3 animate-pulse"></div>
              {t('home.hackathonBadge')}
            </div>
            
            {/* Logo with subtle animation */}
            <div className="flex justify-center mb-4">
              <div className="relative group">
                <div className="absolute -inset-4 bg-gradient-to-r from-emerald-400 to-green-400 rounded-full opacity-20 group-hover:opacity-30 transition-opacity duration-300 blur-xl"></div>
                <img 
                  src="/AgriLogo.png" 
                  alt="AgriWaste2Fuel Logo" 
                  className="h-32 md:h-36 lg:h-40 w-auto object-contain relative z-10 transition-transform duration-300 group-hover:scale-105"
                />
              </div>
            </div>
            
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight tracking-tight">
              <span className="relative inline-block">
                {t('home.title')}
                <div className="absolute -bottom-2 left-0 w-full h-1 bg-gradient-to-r from-emerald-600 to-green-600 rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
              </span>
              <span className="block bg-gradient-to-r from-emerald-600 via-green-600 to-teal-600 bg-clip-text text-transparent mt-2">
                {t('home.subtitle')}
              </span>
            </h1>
            
            <p className="text-lg sm:text-xl md:text-2xl text-gray-600 mb-8 sm:mb-12 max-w-4xl mx-auto leading-relaxed font-medium px-4 sm:px-0">
              {t('home.description')}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center px-4 sm:px-0">
              <button
                onClick={() => navigate('/input')}
                className="group relative bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-700 hover:to-green-700 text-white px-8 sm:px-12 py-3 sm:py-4 rounded-xl font-bold text-base sm:text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center justify-center overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <svg className="w-5 h-5 mr-3 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="relative z-10">{t('home.startAnalysis')}</span>
              </button>
              
              <button
                onClick={() => navigate('/about')}
                className="group relative border-2 border-emerald-300 text-emerald-700 hover:border-emerald-500 hover:bg-emerald-50 px-8 sm:px-12 py-3 sm:py-4 rounded-xl font-bold text-base sm:text-lg transition-all duration-300 flex items-center justify-center backdrop-blur-sm"
              >
                <svg className="w-5 h-5 mr-3 transition-transform group-hover:rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {t('home.documentation')}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 mb-4 sm:mb-6 px-4">{t('home.modules.title')}</h2>
            <p className="text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto px-4">
              {t('home.modules.subtitle')}
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 px-4 sm:px-0">
            <div className="group bg-white border border-gray-200 hover:border-emerald-200 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t('home.modules.wasteDetection.title')}</h3>
              <p className="text-gray-600 leading-relaxed">{t('home.modules.wasteDetection.description')}</p>
              <div className="mt-6 flex items-center text-emerald-600 font-semibold">
                <span>{t('home.modules.wasteDetection.moduleLabel')}</span>
                <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>

            <div className="group bg-white border border-gray-200 hover:border-blue-200 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t('home.modules.biogasRecommendation.title')}</h3>
              <p className="text-gray-600 leading-relaxed">{t('home.modules.biogasRecommendation.description')}</p>
              <div className="mt-6 flex items-center text-blue-600 font-semibold">
                <span>{t('home.modules.biogasRecommendation.moduleLabel')}</span>
                <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>

            <div className="group bg-white border border-gray-200 hover:border-green-200 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">{t('home.modules.carbonCredits.title')}</h3>
              <p className="text-gray-600 leading-relaxed">{t('home.modules.carbonCredits.description')}</p>
              <div className="mt-6 flex items-center text-green-600 font-semibold">
                <span>{t('home.modules.carbonCredits.moduleLabel')}</span>
                <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">{t('home.projectStatus.title')}</h2>
            <p className="text-xl text-gray-600">{t('home.projectStatus.subtitle')}</p>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 sm:gap-8 px-4 sm:px-0">
            <div className="text-center bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
              <div className="text-5xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent mb-3">{t('home.projectStatus.version.label')}</div>
              <div className="text-gray-600 font-semibold">{t('home.projectStatus.version.title')}</div>
              <div className="text-sm text-gray-500 mt-2">{t('home.projectStatus.version.status')}</div>
            </div>
            <div className="text-center bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
              <div className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-3">{t('home.projectStatus.coreModules.label')}</div>
              <div className="text-gray-600 font-semibold">{t('home.projectStatus.coreModules.title')}</div>
              <div className="text-sm text-gray-500 mt-2">{t('home.projectStatus.coreModules.status')}</div>
            </div>
            <div className="text-center bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
              <div className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">{t('home.projectStatus.testingPhase.label')}</div>
              <div className="text-gray-600 font-semibold">{t('home.projectStatus.testingPhase.title')}</div>
              <div className="text-sm text-gray-500 mt-2">{t('home.projectStatus.testingPhase.status')}</div>
            </div>
            <div className="text-center bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
              <div className="text-5xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-3">{t('home.projectStatus.openSource.label')}</div>
              <div className="text-gray-600 font-semibold">{t('home.projectStatus.openSource.title')}</div>
              <div className="text-sm text-gray-500 mt-2">{t('home.projectStatus.openSource.status')}</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gray-900 text-white relative">
        <div className="max-w-5xl mx-auto text-center px-4 relative">
          <div className="inline-flex items-center bg-emerald-500/20 border border-emerald-400/30 text-emerald-300 px-6 py-3 rounded-full text-sm font-semibold mb-8">
            <svg className="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {t('home.cta.badge')}
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            {t('home.cta.title')}
            <span className="block text-gray-300">
              {t('home.cta.titleSecond')}
            </span>
          </h2>
          
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
            {t('home.cta.description')}
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <button
              onClick={() => navigate('/input')}
              className="group bg-white hover:bg-gray-100 text-gray-900 px-12 py-5 rounded-2xl font-bold text-lg transition-all duration-300 shadow-xl transform hover:-translate-y-1"
            >
              {t('home.cta.tryDemo')}
              <svg className="w-5 h-5 ml-3 inline group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </button>
            
            <button
              onClick={() => navigate('/about')}
              className="group border-2 border-gray-600 text-gray-300 hover:border-white hover:text-white hover:bg-white/10 px-12 py-5 rounded-2xl font-bold text-lg transition-all duration-300"
            >
              {t('home.cta.aboutProject')}
              <svg className="w-5 h-5 ml-3 inline group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
          </div>
          
          <div className="mt-16 grid md:grid-cols-3 gap-8 text-center">
            <div className="border border-gray-700 bg-gray-800/50 p-6 rounded-xl">
              <div className="text-emerald-400 font-bold text-lg mb-2">{t('home.cta.features.openSource.title')}</div>
              <div className="text-gray-400 text-sm">{t('home.cta.features.openSource.description')}</div>
            </div>
            <div className="border border-gray-700 bg-gray-800/50 p-6 rounded-xl">
              <div className="text-emerald-400 font-bold text-lg mb-2">{t('home.cta.features.team.title')}</div>
              <div className="text-gray-400 text-sm">{t('home.cta.features.team.description')}</div>
            </div>
            <div className="border border-gray-700 bg-gray-800/50 p-6 rounded-xl">
              <div className="text-emerald-400 font-bold text-lg mb-2">{t('home.cta.features.forFarmers.title')}</div>
              <div className="text-gray-400 text-sm">{t('home.cta.features.forFarmers.description')}</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;

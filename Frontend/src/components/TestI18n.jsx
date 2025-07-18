import React from 'react';
import { useTranslation } from 'react-i18next';

const TestI18n = () => {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang);
  };

  return (
    <div className="p-4 bg-gray-100 rounded-lg m-4">
      <h2 className="text-xl font-bold mb-4">I18n Test Component</h2>
      <div className="mb-4">
        <button 
          onClick={() => changeLanguage('en')} 
          className="mr-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          English
        </button>
        <button 
          onClick={() => changeLanguage('hi')} 
          className="mr-2 px-4 py-2 bg-green-500 text-white rounded"
        >
          Hindi
        </button>
        <button 
          onClick={() => changeLanguage('mr')} 
          className="mr-2 px-4 py-2 bg-red-500 text-white rounded"
        >
          Marathi
        </button>
      </div>
      <div>
        <p><strong>Current Language:</strong> {i18n.language}</p>
        <p><strong>Home:</strong> {t('navbar.home')}</p>
        <p><strong>Analysis:</strong> {t('navbar.analysis')}</p>
        <p><strong>About:</strong> {t('navbar.about')}</p>
        <p><strong>Title:</strong> {t('home.title')}</p>
      </div>
    </div>
  );
};

export default TestI18n;

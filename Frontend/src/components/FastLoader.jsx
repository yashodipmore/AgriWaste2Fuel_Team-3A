import React from 'react';

const FastLoader = ({ message = "Loading...", size = "md" }) => {
  const sizeClasses = {
    sm: "h-4 w-4",
    md: "h-8 w-8", 
    lg: "h-12 w-12"
  };

  return (
    <div className="flex items-center justify-center">
      <div className="text-center">
        <svg 
          className={`animate-spin -ml-1 mr-3 text-emerald-600 mx-auto mb-3 ${sizeClasses[size]}`}
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          />
          <path 
            className="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
        <p className="text-emerald-600 font-medium text-sm">{message}</p>
      </div>
    </div>
  );
};

// Quick inline loader for buttons
export const ButtonLoader = () => (
  <svg 
    className="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" 
    xmlns="http://www.w3.org/2000/svg" 
    fill="none" 
    viewBox="0 0 24 24"
  >
    <circle 
      className="opacity-25" 
      cx="12" 
      cy="12" 
      r="10" 
      stroke="currentColor" 
      strokeWidth="4"
    />
    <path 
      className="opacity-75" 
      fill="currentColor" 
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
    />
  </svg>
);

// Progress indicator for file uploads
export const ProgressLoader = ({ progress = 0, message = "Processing..." }) => (
  <div className="w-full max-w-md mx-auto">
    <div className="flex items-center justify-between mb-2">
      <span className="text-sm text-emerald-600 font-medium">{message}</span>
      <span className="text-sm text-emerald-600">{Math.round(progress)}%</span>
    </div>
    <div className="w-full bg-emerald-100 rounded-full h-2">
      <div 
        className="bg-emerald-600 h-2 rounded-full transition-all duration-300 ease-out"
        style={{ width: `${progress}%` }}
      />
    </div>
  </div>
);

export default FastLoader;

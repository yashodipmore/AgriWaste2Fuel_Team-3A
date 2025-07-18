// Performance Optimization Utilities - Enhanced

// Debounce function for API calls
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Throttle function for performance
export const throttle = (func, limit) => {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// Enhanced cache for API responses
const apiCache = new Map();

export const getCachedData = (key) => {
  const cached = apiCache.get(key);
  if (cached && Date.now() - cached.timestamp < 300000) { // 5 minutes
    return cached.data;
  }
  return null;
};

export const setCachedData = (key, data) => {
  apiCache.set(key, {
    data,
    timestamp: Date.now()
  });
};

// Clear expired cache entries
export const clearExpiredCache = () => {
  const now = Date.now();
  for (const [key, value] of apiCache.entries()) {
    if (now - value.timestamp > 300000) { // 5 minutes
      apiCache.delete(key);
    }
  }
};

// Fast user session check - made even faster
export const fastSessionCheck = () => {
  try {
    const saved = localStorage.getItem('agriWasteUserSession');
    if (saved) {
      const session = JSON.parse(saved);
      // Extend session time and return immediately
      if (Date.now() - session.timestamp < 604800000) { // 7 days instead of 24 hours
        return session.user;
      }
    }
  } catch (error) {
    // Silent fail for performance
  }
  return null;
};

export const saveUserSession = (user) => {
  try {
    // Save asynchronously to avoid blocking
    setTimeout(() => {
      localStorage.setItem('agriWasteUserSession', JSON.stringify({
        user,
        timestamp: Date.now()
      }));
    }, 0);
  } catch (error) {
    // Silent fail
  }
};

export const clearUserSession = () => {
  try {
    // Clear asynchronously
    setTimeout(() => {
      localStorage.removeItem('agriWasteUserSession');
    }, 0);
  } catch (error) {
    // Silent fail
  }
};

// Fast local analysis for instant fallback
export const getLocalAnalysis = (wasteType, quantity = 1000) => {
  const analyses = {
    'Rice Straw': {
      co2Factor: 0.6,
      creditFactor: 0.4,
      valueFactor: 18,
      method: 'Anaerobic Digestion'
    },
    'Wheat Straw': {
      co2Factor: 0.55,
      creditFactor: 0.35,
      valueFactor: 16,
      method: 'Gasification'
    },
    'Corn Stalks': {
      co2Factor: 0.7,
      creditFactor: 0.45,
      valueFactor: 20,
      method: 'Pyrolysis'
    },
    'Cotton Waste': {
      co2Factor: 0.5,
      creditFactor: 0.3,
      valueFactor: 14,
      method: 'Composting'
    },
    'Sugarcane Bagasse': {
      co2Factor: 0.8,
      creditFactor: 0.5,
      valueFactor: 22,
      method: 'Direct Combustion'
    }
  };
  
  const analysis = analyses[wasteType] || analyses['Rice Straw'];
  
  return {
    wasteType,
    quantity,
    recommendedMethod: analysis.method,
    co2Saved: Math.round(quantity * analysis.co2Factor * 100) / 100,
    carbonCredits: Math.round(quantity * analysis.creditFactor * 100) / 100,
    value: Math.round(quantity * analysis.valueFactor * 100) / 100,
    confidence: 85,
    processingTime: Math.round((Math.log10(quantity / 1000 + 1) + 1) * 4 * 10) / 10,
    timestamp: new Date().toISOString()
  };
};

// Optimize image for faster upload
export const optimizeImage = (file, maxWidth = 800, quality = 0.8) => {
  return new Promise((resolve) => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      // Calculate new dimensions
      const ratio = Math.min(maxWidth / img.width, maxWidth / img.height);
      canvas.width = img.width * ratio;
      canvas.height = img.height * ratio;
      
      // Draw and compress
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      
      canvas.toBlob(resolve, 'image/jpeg', quality);
    };
    
    img.src = URL.createObjectURL(file);
  });
};

// Clean cache periodically for better performance
setInterval(clearExpiredCache, 5 * 60 * 1000); // Every 5 minutes

export default {
  debounce,
  throttle,
  getCachedData,
  setCachedData,
  clearExpiredCache,
  fastSessionCheck,
  saveUserSession,
  getLocalAnalysis,
  optimizeImage
};

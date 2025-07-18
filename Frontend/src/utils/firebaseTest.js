// Firebase Configuration Test
import { auth } from '../config/firebase';

export const testFirebaseConfig = () => {
  console.log('🔥 Firebase Configuration Test');
  console.log('Auth instance:', auth);
  console.log('Auth app:', auth.app);
  console.log('Project ID:', auth.app.options.projectId);
  console.log('API Key:', auth.app.options.apiKey?.substring(0, 20) + '...');
  console.log('Auth Domain:', auth.app.options.authDomain);
  
  // Test if we can access Firebase methods
  try {
    const user = auth.currentUser;
    console.log('Current user:', user);
    console.log('✅ Firebase initialized successfully!');
    return true;
  } catch (error) {
    console.error('❌ Firebase initialization failed:', error);
    return false;
  }
};

// Run test on import
testFirebaseConfig();

import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  updateProfile 
} from 'firebase/auth';
import { auth } from '../config/firebase';
import { getAuthStatus, getUserProfile } from '../services/api';
import { fastSessionCheck, saveUserSession, clearUserSession } from '../utils/performance';
import '../utils/firebaseTest'; // Run Firebase configuration test

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [firebaseUser, setFirebaseUser] = useState(null);

  // Quick initialization check - Make this super fast
  useEffect(() => {
    const quickCheck = () => {
      // Check Firebase current user immediately
      const currentUser = auth.currentUser;
      if (currentUser) {
        console.log('🚀 Firebase user found instantly:', currentUser.email);
        const userData = {
          id: currentUser.uid,
          email: currentUser.email,
          name: currentUser.displayName || currentUser.email,
          emailVerified: currentUser.emailVerified
        };
        setFirebaseUser(currentUser);
        setUser(userData);
        saveUserSession(userData);
        setLoading(false); // Stop loading immediately
        return;
      }
      
      // Try cached session as fallback
      const cachedUser = fastSessionCheck();
      if (cachedUser) {
        console.log('🚀 Cached user found:', cachedUser.email);
        setUser(cachedUser);
        setLoading(false); // Stop loading immediately
        return;
      }
      
      // If no user found, stop loading after short delay
      setTimeout(() => {
        setLoading(false);
      }, 100);
    };
    
    // Run immediately
    quickCheck();
  }, []);

  // Listen for Firebase auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      console.log('🔥 Auth state changed:', firebaseUser ? 'User logged in' : 'User logged out');
      
      setFirebaseUser(firebaseUser);
      
      if (firebaseUser) {
        try {
          // Set user immediately with Firebase data (fast)
          const basicUser = {
            id: firebaseUser.uid,
            email: firebaseUser.email,
            name: firebaseUser.displayName || firebaseUser.email,
            emailVerified: firebaseUser.emailVerified,
            photoURL: firebaseUser.photoURL
          };
          setUser(basicUser);
          saveUserSession(basicUser); // Cache user session
          setLoading(false); // Set loading to false immediately
          
          // Fetch backend profile in background (completely non-blocking)
          setTimeout(async () => {
            try {
              const profile = await getUserProfile();
              setUser(prev => ({ ...prev, ...profile.data }));
              console.log('✅ Backend profile loaded in background');
            } catch (error) {
              console.log('⚠️ Backend profile failed (non-critical):', error.message);
            }
          }, 50); // Very small delay to avoid blocking UI
        } catch (error) {
          console.error('Error setting user:', error);
          setUser({
            id: firebaseUser.uid,
            email: firebaseUser.email,
            name: firebaseUser.displayName || firebaseUser.email,
            emailVerified: firebaseUser.emailVerified
          });
          setLoading(false);
        }
      } else {
        setUser(null);
        clearUserSession(); // Clear cached session
        setLoading(false);
      }
    });

    return unsubscribe;
  }, []);

  // Login function with Firebase
  const login = async (email, password) => {
    try {
      setLoading(true);
      const result = await signInWithEmailAndPassword(auth, email, password);
      
      // User data will be set automatically by onAuthStateChanged
      console.log('✅ Login successful:', result.user.email);
      
      // Test backend authentication in background (non-blocking)
      setTimeout(async () => {
        try {
          const token = await result.user.getIdToken();
          console.log('🔥 Firebase token generated:', token.substring(0, 50) + '...');
          
          const authStatus = await getAuthStatus();
          console.log('✅ Backend auth status:', authStatus.data);
        } catch (backendError) {
          console.log('⚠️ Backend authentication test failed (non-critical):', backendError.message);
        }
      }, 100); // Run after 100ms
      
      return { success: true, user: result.user };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: getFirebaseErrorMessage(error.code) 
      };
    } finally {
      setLoading(false);
    }
  };

  // Register function with Firebase
  const register = async (userData) => {
    try {
      setLoading(true);
      const { email, password, name } = userData;
      
      const result = await createUserWithEmailAndPassword(auth, email, password);
      
      // Update display name if provided
      if (name) {
        await updateProfile(result.user, { displayName: name });
      }
      
      return { success: true, user: result.user };
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        error: getFirebaseErrorMessage(error.code) 
      };
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await signOut(auth);
      setUser(null);
      setFirebaseUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Get Firebase error message
  const getFirebaseErrorMessage = (errorCode) => {
    switch (errorCode) {
      case 'auth/user-not-found':
        return 'No user found with this email address.';
      case 'auth/wrong-password':
        return 'Incorrect password.';
      case 'auth/email-already-in-use':
        return 'An account with this email already exists.';
      case 'auth/weak-password':
        return 'Password should be at least 6 characters.';
      case 'auth/invalid-email':
        return 'Please enter a valid email address.';
      case 'auth/too-many-requests':
        return 'Too many failed login attempts. Please try again later.';
      default:
        return 'An error occurred. Please try again.';
    }
  };

  // Get current Firebase token
  const getToken = async () => {
    if (firebaseUser) {
      try {
        return await firebaseUser.getIdToken();
      } catch (error) {
        console.error('Error getting token:', error);
        return null;
      }
    }
    return null;
  };

  const value = {
    user,
    firebaseUser,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    getToken,
    loading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

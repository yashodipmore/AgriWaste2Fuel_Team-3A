// Firebase Configuration for Frontend
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyClNDyJaezeXmFS07GHGFcNyRcOg-SmWVQ",
  authDomain: "agriwaste2fuel-737b5.firebaseapp.com",
  projectId: "agriwaste2fuel-737b5",
  storageBucket: "agriwaste2fuel-737b5.firebasestorage.app",
  messagingSenderId: "608178897702",
  appId: "1:608178897702:web:a81874e926b9ea7299f7e7",
  measurementId: "G-HDKYJMTN3S"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);
export default app;

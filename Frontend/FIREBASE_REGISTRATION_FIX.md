# 🔥 Firebase Console Setup for User Registration

## ❌ **Current Issue**: User registration failing

## 🔧 **Solution**: Enable Email/Password Authentication

### **Step 1: Go to Firebase Console**
1. Open: https://console.firebase.google.com/
2. Select your project: `agriwaste2fuel-737b5`

### **Step 2: Enable Email/Password Authentication**
1. Click "Authentication" in left sidebar
2. Go to "Sign-in method" tab
3. Find "Email/Password" provider
4. Click the edit icon (pencil)
5. **Enable** the first toggle (Email/Password)
6. **Optional**: Enable "Email link (passwordless sign-in)"
7. Click "Save"

### **Step 3: Verify Settings**
- Email/Password should show "Enabled" status
- You should see it in the "Sign-in providers" list

### **Step 4: Test User Registration**
1. Go to your app: `http://localhost:3000/register`
2. Fill out the registration form
3. Click "Register"
4. Check Firebase Console > Authentication > Users

### **Step 5: Check Firebase Console Logs**
1. Go to Firebase Console > Project Overview
2. Click "Functions" (if available)
3. Look for any error logs

## 🔍 **Debugging Steps**

### **Check Browser Console**
Open Developer Tools (F12) and look for:
```javascript
🔥 Firebase Configuration Test
✅ Firebase initialized successfully!
```

### **Check Registration Errors**
Look for specific error messages:
- `auth/email-already-in-use` - User already exists
- `auth/weak-password` - Password too weak (< 6 chars)
- `auth/invalid-email` - Invalid email format
- `auth/operation-not-allowed` - Email/Password not enabled

### **Test with Simple Credentials**
Try registering with:
- Email: `test@example.com`
- Password: `password123`
- Name: `Test User`

## 🚨 **Common Issues**

### **1. Email/Password Not Enabled**
**Solution**: Enable in Firebase Console > Authentication > Sign-in method

### **2. Password Too Weak**
**Solution**: Use password with at least 6 characters

### **3. Email Already Exists**
**Solution**: Use different email or try login instead

### **4. Network Issues**
**Solution**: Check if backend is running on port 8000

## 📱 **Quick Test**
Run this in browser console on your app:
```javascript
// Test Firebase auth
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from './config/firebase';

createUserWithEmailAndPassword(auth, 'test@example.com', 'password123')
  .then(result => console.log('✅ Registration successful:', result))
  .catch(error => console.error('❌ Registration failed:', error));
```

## 🎯 **Expected Result**
After enabling Email/Password authentication:
1. Registration form should work
2. User should appear in Firebase Console
3. Auto-redirect to dashboard
4. Backend should receive Firebase token

---
**Enable Email/Password authentication in Firebase Console and try again!** 🚀

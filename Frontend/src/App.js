import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AuthDebug from './components/AuthDebug';
import Home from './pages/Home';
import Input from './pages/Input';
import Result from './pages/Result';
import About from './pages/About';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AuthTest from './pages/AuthTest';
import RouteTest from './pages/RouteTest';
import SimpleTest from './pages/SimpleTest';
import './App.css';
import './i18n';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/auth-test" element={<AuthTest />} />
              
              {/* Protected Routes */}
              <Route path="/input" element={
                <ProtectedRoute>
                  <Input />
                </ProtectedRoute>
              } />
              <Route path="/result" element={
                <ProtectedRoute>
                  <Result />
                </ProtectedRoute>
              } />
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="/simple-test" element={
                <ProtectedRoute>
                  <SimpleTest />
                </ProtectedRoute>
              } />
            </Routes>
          </main>
          <Footer />
          <AuthDebug />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

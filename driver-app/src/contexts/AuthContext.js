import React, { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [driver, setDriver] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkLoginStatus();
  }, []);

  const checkLoginStatus = async () => {
    try {
      const isLoggedIn = await authService.isLoggedIn();
      if (isLoggedIn) {
        const driverData = await authService.getStoredDriver();
        setDriver(driverData);
      }
    } catch (error) {
      console.error('Error checking login status:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (phone, password) => {
    try {
      const data = await authService.login(phone, password);
      setDriver(data.driver);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || 'فشل تسجيل الدخول',
      };
    }
  };

  const register = async (driverData) => {
    try {
      console.log('🔵 AuthContext: Starting registration with:', driverData);
      const data = await authService.register(driverData);
      console.log('🟢 AuthContext: Registration successful, data:', data);
      setDriver(data.driver);
      return { success: true };
    } catch (error) {
      console.error('🔴 AuthContext: Registration failed:', error);
      console.error('🔴 Error details:', error.response?.data);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'فشل التسجيل',
      };
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      setDriver(null);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  const value = {
    driver,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!driver,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};


import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// تكوين API
// ⚠️ مهم: عند التشغيل على الجوال، استبدل localhost بـ IP جهازك
// لمعرفة IP جهازك، شغّل: ./get-ip.sh
const API_URL = 'http://192.168.0.65:3000/api'; // استخدم IP جهازك هنا

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// إضافة التوكن تلقائياً لكل طلب
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('driverToken');
      if (token && token !== 'null' && token !== 'undefined') {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// خدمات المصادقة
export const authService = {
  // تسجيل دخول السائق
  login: async (phone, password) => {
    const response = await api.post('/drivers/login', { phone, password });
    if (response.data.tokens?.accessToken) {
      await AsyncStorage.setItem('driverToken', String(response.data.tokens.accessToken));
      await AsyncStorage.setItem('driverData', JSON.stringify(response.data.data));
    }
    return { driver: response.data.data };
  },

  // تسجيل سائق جديد
  register: async (driverData) => {
    try {
      console.log('📤 Sending registration data:', driverData);
      const response = await api.post('/drivers/register', driverData);
      console.log('📥 Registration response:', response.data);

      if (response.data.tokens?.accessToken) {
        await AsyncStorage.setItem('driverToken', String(response.data.tokens.accessToken));
        await AsyncStorage.setItem('driverData', JSON.stringify(response.data.data));
        console.log('✅ Token and data saved successfully');
      }
      return { driver: response.data.data };
    } catch (error) {
      console.error('❌ Registration error:', error);
      console.error('❌ Error response:', error.response?.data);
      throw error;
    }
  },

  // تسجيل الخروج
  logout: async () => {
    try {
      await AsyncStorage.removeItem('driverToken');
      await AsyncStorage.removeItem('driverData');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  },

  // الحصول على بيانات السائق المحفوظة
  getStoredDriver: async () => {
    try {
      const driverData = await AsyncStorage.getItem('driverData');
      if (!driverData || driverData === 'null' || driverData === 'undefined') {
        return null;
      }
      return JSON.parse(driverData);
    } catch (error) {
      console.error('Error getting stored driver:', error);
      return null;
    }
  },

  // التحقق من تسجيل الدخول
  isLoggedIn: async () => {
    try {
      const token = await AsyncStorage.getItem('driverToken');
      // تحويل صريح - تجنب مشكلة String to Boolean
      if (!token || token === 'null' || token === 'undefined' || token === '') {
        return false;
      }
      return true;
    } catch (error) {
      console.error('Error checking login status:', error);
      return false;
    }
  },
};

// خدمات الطلبات
export const orderService = {
  // الحصول على الطلبات المتاحة
  getAvailableOrders: async () => {
    const response = await api.get('/orders/available');
    return response.data;
  },

  // الحصول على طلبات السائق الحالية
  getMyOrders: async () => {
    const response = await api.get('/drivers/orders');
    return response.data;
  },

  // قبول طلب
  acceptOrder: async (orderId) => {
    const response = await api.post(`/orders/${orderId}/accept`);
    return response.data;
  },

  // رفض طلب
  rejectOrder: async (orderId, reason) => {
    const response = await api.post(`/orders/${orderId}/reject`, { reason });
    return response.data;
  },

  // تحديث حالة الطلب
  updateOrderStatus: async (orderId, status) => {
    const response = await api.put(`/orders/${orderId}/status`, { status });
    return response.data;
  },

  // الحصول على تفاصيل طلب
  getOrderDetails: async (orderId) => {
    const response = await api.get(`/orders/${orderId}`);
    return response.data;
  },
};

// خدمات الموقع
export const locationService = {
  // تحديث موقع السائق
  updateLocation: async (latitude, longitude) => {
    const response = await api.post('/drivers/location', {
      latitude,
      longitude,
    });
    return response.data;
  },
};

// خدمات الملف الشخصي
export const profileService = {
  // الحصول على بيانات السائق
  getProfile: async () => {
    const response = await api.get('/drivers/profile');
    return response.data;
  },

  // تحديث بيانات السائق
  updateProfile: async (profileData) => {
    const response = await api.put('/drivers/profile', profileData);
    return response.data;
  },

  // الحصول على إحصائيات السائق
  getStats: async () => {
    const response = await api.get('/drivers/stats');
    return response.data;
  },
};

export default api;


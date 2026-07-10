# 🚗 تطبيق السائقين - Wasl Driver App

> تطبيق React Native للسائقين في نظام وصل للتوصيل

---

## ✅ الحالة الحالية

**تم إنشاء التطبيق بنجاح!** 🎉

### ما تم إنجازه:

- ✅ إعداد المشروع بـ React Native + Expo
- ✅ تثبيت جميع المكتبات المطلوبة
- ✅ إنشاء هيكل المشروع
- ✅ نظام المصادقة (تسجيل دخول + تسجيل)
- ✅ الشاشة الرئيسية مع الإحصائيات
- ✅ شاشة الطلبات المتاحة
- ✅ خدمات API
- ✅ Context للمصادقة
- ✅ Navigation System

---

## 📱 الشاشات المتوفرة

### ✅ شاشات المصادقة
- **شاشة تسجيل الدخول** - `LoginScreen.js`
- **شاشة التسجيل** - `RegisterScreen.js`

### ✅ الشاشات الرئيسية
- **الشاشة الرئيسية** - `HomeScreen.js`
  - عرض الإحصائيات (الطلبات، الأرباح، التقييم)
  - الإجراءات السريعة
  - زر تسجيل الخروج

- **شاشة الطلبات المتاحة** - `AvailableOrdersScreen.js`
  - عرض جميع الطلبات المتاحة
  - تفاصيل كل طلب (العنوان، السعر، المسافة)
  - إمكانية التحديث

---

## 🚀 التشغيل

### 1. تثبيت المكتبات (تم بالفعل ✅)
```bash
npm install
```

### 2. تشغيل التطبيق
```bash
# تشغيل Expo
npm start

# أو للأندرويد مباشرة
npm run android

# أو للـ iOS مباشرة
npm run ios
```

### 3. فتح التطبيق
- امسح QR Code بتطبيق Expo Go على هاتفك
- أو اضغط `a` للأندرويد
- أو اضغط `i` للـ iOS

---

## 📦 المكتبات المثبتة

- ✅ `@react-navigation/native` - التنقل
- ✅ `@react-navigation/stack` - Stack Navigation
- ✅ `@react-navigation/bottom-tabs` - Bottom Tabs
- ✅ `react-native-screens` - تحسين الأداء
- ✅ `react-native-safe-area-context` - Safe Area
- ✅ `@react-native-async-storage/async-storage` - التخزين المحلي
- ✅ `axios` - طلبات HTTP
- ✅ `react-native-maps` - الخرائط
- ✅ `expo-location` - تتبع الموقع

---

## 📁 هيكل المشروع

```
driver-app/
├── App.js                          ← الملف الرئيسي
├── src/
│   ├── screens/                    ← الشاشات
│   │   ├── LoginScreen.js          ✅
│   │   ├── RegisterScreen.js       ✅
│   │   ├── HomeScreen.js           ✅
│   │   └── AvailableOrdersScreen.js ✅
│   ├── navigation/                 ← التنقل
│   │   └── AppNavigator.js         ✅
│   ├── contexts/                   ← Contexts
│   │   └── AuthContext.js          ✅
│   ├── services/                   ← خدمات API
│   │   └── api.js                  ✅
│   ├── components/                 ← المكونات
│   └── utils/                      ← الأدوات المساعدة
├── package.json
└── README.md
```

---

## 🔄 الشاشات المتبقية (قيد التطوير)

- [ ] شاشة تفاصيل الطلب
- [ ] شاشة طلباتي الحالية
- [ ] شاشة الخريطة والملاحة
- [ ] شاشة سجل الطلبات
- [ ] شاشة الأرباح
- [ ] شاشة الملف الشخصي
- [ ] شاشة الإعدادات

---

## 🔗 الاتصال بالـ Backend

التطبيق يتصل بـ Backend API على:
```
http://localhost:3000/api
```

لتغيير العنوان، عدّل ملف `src/services/api.js`:
```javascript
const API_URL = 'http://YOUR_IP:3000/api';
```

**ملاحظة:** استخدم IP الجهاز بدلاً من localhost عند التجربة على الهاتف!

---

## 🎨 المميزات

- ✅ واجهة عربية كاملة
- ✅ تصميم حديث وجذاب
- ✅ سهل الاستخدام
- ✅ نظام مصادقة آمن
- ✅ تحديث تلقائي للبيانات
- ✅ معالجة الأخطاء

---

## 📞 الدعم

للاستفسارات، يرجى التواصل مع فريق التطوير.

---

**صنع بـ ❤️ في اليمن 🇾🇪**


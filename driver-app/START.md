# 🚀 تشغيل سريع - Quick Start

## الخطوات البسيطة:

### 1️⃣ ثبّت Expo Go على جوالك
- **Android:** من Google Play Store
- **iOS:** من App Store

### 2️⃣ شغّل Backend
```bash
cd /Users/khalidawadh/wasl-delivery-system/backend
npm run dev
```

### 3️⃣ شغّل التطبيق
في Terminal جديد:
```bash
cd /Users/khalidawadh/wasl-delivery-system/driver-app
npm start
```

### 4️⃣ افتح على الجوال
- امسح QR Code بتطبيق Expo Go
- أو اضغط `a` للأندرويد
- أو اضغط `i` للـ iOS

---

## ⚠️ مهم جداً!

**الجوال والماك يجب أن يكونا على نفس الـ WiFi!**

---

## 🔧 إذا لم يعمل:

1. شغّل السكريبت لمعرفة IP:
```bash
./get-ip.sh
```

2. افتح `src/services/api.js` وحدّث السطر 7:
```javascript
const API_URL = 'http://YOUR_IP:3000/api';
```

---

## 📖 للتفاصيل الكاملة:
اقرأ ملف: `HOW-TO-RUN-ON-PHONE.md`

---

**بالتوفيق! 🎉**


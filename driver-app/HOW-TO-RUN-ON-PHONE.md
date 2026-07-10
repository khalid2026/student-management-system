# 📱 كيفية تشغيل التطبيق على الجوال

## الخطوة 1️⃣: تثبيت Expo Go

### على Android:
1. افتح **Google Play Store**
2. ابحث عن **"Expo Go"**
3. اضغط **تثبيت**

### على iOS:
1. افتح **App Store**
2. ابحث عن **"Expo Go"**
3. اضغط **تثبيت**

---

## الخطوة 2️⃣: معرفة IP جهاز الماك

افتح Terminal واكتب:

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

ستحصل على شيء مثل:
```
inet 192.168.1.5
```

**احفظ هذا الرقم!** 📝 (مثلاً: `192.168.1.5`)

---

## الخطوة 3️⃣: تحديث API URL

افتح ملف `src/services/api.js` وغيّر السطر 5:

**من:**
```javascript
const API_URL = 'http://localhost:3000/api';
```

**إلى:**
```javascript
const API_URL = 'http://192.168.1.5:3000/api';  // استخدم IP جهازك
```

⚠️ **مهم:** استبدل `192.168.1.5` بـ IP جهازك الفعلي!

---

## الخطوة 4️⃣: تشغيل Backend

في Terminal الأول:

```bash
cd /Users/khalidawadh/wasl-delivery-system/backend
npm run dev
```

يجب أن ترى:
```
✅ Server running on port 3000
✅ MongoDB connected
```

**اترك هذا Terminal مفتوحاً!**

---

## الخطوة 5️⃣: تشغيل تطبيق السائقين

في Terminal جديد (ثاني):

```bash
cd /Users/khalidawadh/wasl-delivery-system/driver-app
npm start
```

انتظر قليلاً... ستظهر لك:

```
› Metro waiting on exp://192.168.1.5:8081
› Scan the QR code above with Expo Go (Android) or the Camera app (iOS)
```

---

## الخطوة 6️⃣: فتح التطبيق على الجوال

### على Android:
1. افتح تطبيق **Expo Go**
2. اضغط على **"Scan QR Code"**
3. امسح الـ QR Code من Terminal

### على iOS:
1. افتح تطبيق **الكاميرا** العادي
2. وجّه الكاميرا على QR Code
3. اضغط على الإشعار الذي يظهر
4. سيفتح في Expo Go

---

## ✅ التطبيق يعمل!

الآن يجب أن ترى:
- شاشة تسجيل الدخول 🔐
- يمكنك التسجيل كسائق جديد
- أو تسجيل الدخول

---

## 🔧 حل المشاكل الشائعة

### المشكلة 1: "Network request failed"
**الحل:**
- تأكد أن الجوال والماك على نفس الـ WiFi
- تأكد من تحديث API_URL بـ IP الصحيح
- تأكد أن Backend يعمل

### المشكلة 2: QR Code لا يعمل
**الحل:**
- اضغط `a` في Terminal لفتح Android مباشرة
- أو اضغط `i` لفتح iOS Simulator

### المشكلة 3: التطبيق يتوقف
**الحل:**
- اضغط `r` في Terminal لإعادة التحميل
- أو هز الجوال واختر "Reload"

---

## 📝 ملاحظات مهمة

1. **الجوال والماك يجب أن يكونا على نفس الـ WiFi** ✅
2. **Backend يجب أن يعمل أولاً** ✅
3. **استخدم IP الجهاز وليس localhost** ✅
4. **لا تغلق Terminal** ✅

---

## 🎯 الأوامر السريعة

```bash
# Terminal 1: Backend
cd /Users/khalidawadh/wasl-delivery-system/backend
npm run dev

# Terminal 2: Driver App
cd /Users/khalidawadh/wasl-delivery-system/driver-app
npm start
```

---

## 📞 إذا واجهت مشكلة

تأكد من:
- [ ] Expo Go مثبت على الجوال
- [ ] الجوال والماك على نفس WiFi
- [ ] Backend يعمل (Terminal 1)
- [ ] Driver App يعمل (Terminal 2)
- [ ] API_URL محدث بـ IP الصحيح

---

**بالتوفيق! 🚀**

صنع بـ ❤️ في اليمن 🇾🇪


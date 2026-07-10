# 🔧 حل المشكلة - MongoDB غير مشغّل

## ❌ المشكلة:
التطبيق لا يعمل لأن **MongoDB غير مشغّل** على جهازك!

---

## ✅ الحل السريع - استخدام MongoDB Atlas (مجاني):

### الخطوة 1️⃣: إنشاء حساب MongoDB Atlas

1. اذهب إلى: https://www.mongodb.com/cloud/atlas/register
2. سجّل حساب مجاني
3. اختر **FREE** tier (M0)
4. اختر Region قريب منك (مثلاً: AWS / Frankfurt)

### الخطوة 2️⃣: إنشاء Cluster

1. بعد التسجيل، اضغط **"Build a Database"**
2. اختر **FREE** (M0)
3. اختر Region
4. اضغط **"Create Cluster"**

### الخطوة 3️⃣: إنشاء Database User

1. اضغط على **"Database Access"** من القائمة اليسرى
2. اضغط **"Add New Database User"**
3. اختر:
   - Username: `wasl_admin`
   - Password: `wasl123456` (أو أي كلمة مرور تريدها)
4. اضغط **"Add User"**

### الخطوة 4️⃣: السماح بالاتصال من أي مكان

1. اضغط على **"Network Access"** من القائمة اليسرى
2. اضغط **"Add IP Address"**
3. اضغط **"Allow Access from Anywhere"** (0.0.0.0/0)
4. اضغط **"Confirm"**

### الخطوة 5️⃣: الحصول على Connection String

1. ارجع إلى **"Database"**
2. اضغط **"Connect"** على الـ Cluster
3. اختر **"Connect your application"**
4. انسخ الـ **Connection String**
5. سيكون شكله:
   ```
   mongodb+srv://wasl_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### الخطوة 6️⃣: تحديث Backend

افتح ملف: `/Users/khalidawadh/wasl-delivery-system/backend/.env`

غيّر السطر:
```
MONGODB_URI=mongodb://localhost:27017/wasl-delivery
```

إلى:
```
MONGODB_URI=mongodb+srv://wasl_admin:wasl123456@cluster0.xxxxx.mongodb.net/wasl-delivery?retryWrites=true&w=majority
```

⚠️ **مهم:** استبدل `<password>` بكلمة المرور التي اخترتها!

### الخطوة 7️⃣: إعادة تشغيل Backend

```bash
# أوقف Backend الحالي (Ctrl+C في Terminal)
# ثم شغّله مرة أخرى:
cd /Users/khalidawadh/wasl-delivery-system/backend
npm run dev
```

---

## 🎯 الحل البديل - تثبيت MongoDB محلياً:

إذا كنت تفضل استخدام MongoDB محلياً:

### على macOS:

```bash
# تثبيت Homebrew (إذا لم يكن مثبتاً)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# تثبيت MongoDB
brew tap mongodb/brew
brew install mongodb-community

# تشغيل MongoDB
brew services start mongodb-community
```

---

## 📝 كيف تعرف أن المشكلة حُلّت؟

بعد تحديث `.env` وإعادة تشغيل Backend، يجب أن ترى:

```
✅ Server running on port 3000
✅ MongoDB connected successfully
```

---

## 🚀 بعد حل المشكلة:

1. شغّل Backend (يجب أن يتصل بـ MongoDB)
2. شغّل Driver App
3. امسح QR Code
4. التطبيق سيعمل! 🎉

---

**أخبرني أي حل تفضل وسأساعدك!** 💪


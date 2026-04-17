# 🎓 نظام إدارة الطلاب - Khalid Soft

نظام شامل لإدارة الطلاب والوكلاء والمؤسسات التعليمية بالرنجت الماليزي.

## ✨ المميزات

- 👥 إدارة الطلاب والوكلاء
- 🏫 إدارة المؤسسات التعليمية  
- 💰 نظام المدفوعات بالرنجت الماليزي (RM)
- 📊 تقارير شاملة ولوحة تحكم
- 🔐 نظام مستخدمين متعدد المستويات
- 📱 تصميم متجاوب

## 🚀 التثبيت والتشغيل

### الطريقة الأولى: Python مباشرة

```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل النظام
python student_management.py
```

### الطريقة الثانية: Docker

```bash
# تشغيل بـ Docker Compose
docker-compose up -d
```

## 🌐 الوصول للنظام

- **الرابط**: http://localhost:5001
- **المدير**: `admin` / `admin123`
- **الموظف**: `employee` / `emp123`

## 💰 العملة

النظام يعمل بالرنجت الماليزي (RM) فقط.

## 📁 هيكل المشروع

```
student-management-system/
├── student_management.py      # الملف الرئيسي
├── templates/                 # قوالب HTML
├── static/                   # ملفات CSS/JS
├── requirements.txt          # المتطلبات
├── Dockerfile               # إعدادات Docker
└── README.md               # هذا الملف
```

## 🛠️ المتطلبات

- Python 3.8+
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Werkzeug 2.3.7

## 📞 الدعم

تم تطوير النظام بواسطة **Khalid Soft**

---

© 2024 Khalid Soft - جميع الحقوق محفوظة

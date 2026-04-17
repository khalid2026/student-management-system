# استخدام Python 3.9 كصورة أساسية
FROM python:3.9-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات التطبيق
COPY . .

# إنشاء مجلد للبيانات
RUN mkdir -p instance

# تعيين المنفذ
EXPOSE 5001

# تشغيل التطبيق
CMD ["python", "student_management.py"]

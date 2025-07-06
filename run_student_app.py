#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل تطبيق إدارة الطلاب
Student Management System Runner
Khalid Soft
"""

from student_management import app, create_database, create_default_users, add_sample_data

if __name__ == '__main__':
    print("=" * 50)
    print("🎓 نظام إدارة الطلاب - Khalid Soft")
    print("=" * 50)
    print("📊 جاري إعداد قاعدة البيانات...")
    
    # إنشاء قاعدة البيانات
    create_database()

    # إنشاء المستخدمين الافتراضيين
    create_default_users()

    # إضافة البيانات التجريبية
    add_sample_data()
    
    print("✅ تم إعداد قاعدة البيانات بنجاح!")
    print("🌐 التطبيق يعمل على: http://localhost:5001")
    print("📱 يمكنك الوصول للتطبيق من أي جهاز على الشبكة المحلية")
    print("=" * 50)
    
    # تشغيل التطبيق
    app.run(debug=True, host='0.0.0.0', port=5001)

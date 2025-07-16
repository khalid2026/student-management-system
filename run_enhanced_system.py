#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل نظام إدارة الطلاب المحسن
Enhanced Student Management System Runner
"""

from student_enhanced import app, db, create_default_data

def initialize_system():
    """تهيئة النظام"""
    with app.app_context():
        print("🔧 إنشاء قاعدة البيانات...")
        db.create_all()
        
        print("📊 إنشاء البيانات الافتراضية...")
        create_default_data()
        
        print("✅ تم تهيئة النظام بنجاح!")

if __name__ == '__main__':
    print("=" * 80)
    print("🎓 نظام إدارة الطلاب المحسن مع الوكلاء ومدة الدراسة - خالد سوفت")
    print("   Enhanced Student Management System with Agents - Khalid Soft")
    print("=" * 80)
    
    # تهيئة النظام
    initialize_system()
    
    print("\n🌐 تشغيل الخادم على:")
    print("   http://localhost:5004")
    print("\n📋 بيانات الدخول:")
    print("   المدير: admin / admin123")
    print("   الموظف: employee / employee123")
    print("\n🎯 المميزات الجديدة:")
    print("   ✅ إدارة الوكلاء مع نسب العمولة")
    print("   ✅ مدة الدراسة (شهور/سنوات)")
    print("   ✅ حساب تلقائي للأرباح والعمولات")
    print("   ✅ إحصائيات متقدمة للوكلاء")
    print("   ✅ واجهة محسنة مع تصميم جديد")
    print("   ✅ بحث وفلترة متقدمة")
    print("\n⚠️  للإيقاف: اضغط Ctrl+C")
    print("=" * 80)
    
    # تشغيل التطبيق
    app.run(host='0.0.0.0', port=5004, debug=True)

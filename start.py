#!/usr/bin/env python3
"""
🎓 نظام إدارة الطلاب - Khalid Soft
Student Management System Launcher
"""

import os
import sys

def main():
    """تشغيل نظام إدارة الطلاب"""
    
    print("=" * 50)
    print("🎓 نظام إدارة الطلاب - Khalid Soft")
    print("🚀 Student Management System")
    print("=" * 50)
    
    # التحقق من وجود الملفات المطلوبة
    required_files = ['student_management.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {', '.join(missing_files)}")
        print("تأكد من وجود جميع الملفات المطلوبة")
        sys.exit(1)
    
    print("📋 التحقق من المتطلبات...")
    
    # محاولة استيراد المكتبات المطلوبة
    try:
        import flask
        import flask_sqlalchemy
        print("✅ تم العثور على جميع المكتبات المطلوبة")
    except ImportError as e:
        print(f"❌ مكتبة مفقودة: {e}")
        print("قم بتثبيت المتطلبات باستخدام:")
        print("pip install -r student_requirements.txt")
        sys.exit(1)
    
    print("📊 جاري إعداد قاعدة البيانات...")
    
    # تشغيل التطبيق
    try:
        from student_management import app
        
        print("✅ تم إعداد قاعدة البيانات بنجاح!")
        print("🌐 النظام يعمل على: http://localhost:5001")
        print("📱 يمكنك الوصول للنظام من أي جهاز على الشبكة المحلية")
        print("🔧 للإيقاف اضغط Ctrl+C")
        print("=" * 50)
        print("🔑 بيانات تسجيل الدخول الافتراضية:")
        print("المدير: admin / admin123")
        print("الموظف: employee / emp123")
        print("=" * 50)
        
        app.run(host='0.0.0.0', port=5001, debug=True)
        
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف النظام بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {e}")
        print("💡 جرب حذف مجلد instance وإعادة التشغيل")
        sys.exit(1)

if __name__ == "__main__":
    main()

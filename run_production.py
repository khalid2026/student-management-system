#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل النظام للإنتاج
Production runner for Khalid Soft Student Management System
"""

import os
from student_management import app, db, create_database

if __name__ == '__main__':
    # إنشاء قاعدة البيانات إذا لم تكن موجودة
    with app.app_context():
        create_database()
    
    # تشغيل التطبيق
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق إدارة الطلاب والحسابات
Student Management System
Khalid Soft - نظام إدارة الطلاب
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import json
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'khalid-soft-student-management-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# إنشاء مجلد الرفع إذا لم يكن موجوداً
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# قاموس الترجمات الكامل
TRANSLATIONS = {
    'ar': {
        # العناوين الرئيسية
        'app_title': 'نظام إدارة الطلاب - Khalid Soft',
        'dashboard': 'لوحة التحكم',
        'add_student': 'تسجيل طالب جديد',
        'manage_students': 'إدارة الطلاب',
        'institutions': 'المؤسسات التعليمية',
        'payments': 'المدفوعات',
        'reports': 'التقارير',
        'users': 'إدارة المستخدمين',
        'settings': 'الإعدادات',
        'search': 'البحث',
        'logout': 'تسجيل الخروج',
        'login': 'تسجيل الدخول',

        # بيانات المستخدم
        'username': 'اسم المستخدم',
        'password': 'كلمة المرور',
        'full_name': 'الاسم الكامل',
        'role': 'الصلاحية',
        'admin': 'مدير',
        'employee': 'موظف',
        'active': 'نشط',
        'inactive': 'غير نشط',
        'last_login': 'آخر تسجيل دخول',
        'created_at': 'تاريخ الإنشاء',

        # بيانات الطلاب
        'student_info': 'بيانات الطالب',
        'personal_info': 'البيانات الشخصية',
        'contact_info': 'بيانات الاتصال',
        'academic_info': 'البيانات الأكاديمية',
        'financial_info': 'البيانات المالية',
        'first_name_ar': 'الاسم الأول (عربي)',
        'last_name_ar': 'اسم العائلة (عربي)',
        'first_name_en': 'الاسم الأول (إنجليزي)',
        'last_name_en': 'اسم العائلة (إنجليزي)',
        'passport_number': 'رقم الجواز',
        'national_id': 'رقم الهوية الوطنية',
        'birth_date': 'تاريخ الميلاد',
        'nationality': 'الجنسية',
        'gender': 'الجنس',
        'male': 'ذكر',
        'female': 'أنثى',
        'phone': 'رقم الهاتف',
        'email': 'البريد الإلكتروني',
        'address': 'العنوان',
        'institution': 'المؤسسة التعليمية',
        'student_id_number': 'الرقم الجامعي',
        'major': 'التخصص',
        'level': 'المستوى الدراسي',
        'enrollment_date': 'تاريخ التسجيل',
        'graduation_date': 'تاريخ التخرج المتوقع',
        'status': 'الحالة',
        'tuition_fees': 'الرسوم الدراسية',
        'paid_amount': 'المبلغ المدفوع',
        'remaining_amount': 'المبلغ المتبقي',
        'notes': 'ملاحظات',

        # الإحصائيات
        'welcome': 'مرحباً بك في نظام إدارة الطلاب',
        'total_students': 'إجمالي الطلاب',
        'active_students': 'الطلاب النشطون',
        'graduated_students': 'الخريجون',
        'suspended_students': 'المتوقفون',
        'total_institutions': 'المؤسسات التعليمية',
        'universities': 'الجامعات',
        'institutes': 'المعاهد',
        'colleges': 'الكليات',
        'total_payments': 'إجمالي المدفوعات',
        'total_amount': 'إجمالي المبلغ',
        'total_users': 'إجمالي المستخدمين',

        # الأزرار والإجراءات
        'save': 'حفظ',
        'cancel': 'إلغاء',
        'edit': 'تعديل',
        'delete': 'حذف',
        'view': 'عرض',
        'add': 'إضافة',
        'update': 'تحديث',
        'submit': 'إرسال',
        'reset': 'إعادة تعيين',
        'back': 'العودة',
        'next': 'التالي',
        'previous': 'السابق',
        'close': 'إغلاق',
        'confirm': 'تأكيد',
        'yes': 'نعم',
        'no': 'لا',

        # الإعدادات
        'language': 'اللغة',
        'theme': 'المظهر',
        'color_scheme': 'نظام الألوان',
        'font_size': 'حجم الخط',
        'appearance_settings': 'إعدادات المظهر واللغة',
        'text_settings': 'إعدادات النص',
        'current_settings': 'الإعدادات الحالية',
        'theme_preview': 'معاينة المظهر',
        'default_theme': 'الافتراضي',
        'dark_theme': 'المظهر الداكن',
        'light_theme': 'المظهر الفاتح',
        'modern_theme': 'عصري',
        'small_font': 'صغير',
        'medium_font': 'متوسط',
        'large_font': 'كبير',
        'sidebar_collapsed': 'إخفاء القائمة الجانبية افتراضياً',

        # الرسائل
        'success_message': 'تم بنجاح!',
        'error_message': 'حدث خطأ!',
        'warning_message': 'تحذير!',
        'info_message': 'معلومات',
        'no_data': 'لا توجد بيانات',
        'loading': 'جاري التحميل...',
        'please_wait': 'يرجى الانتظار...',
        'required_field': 'حقل مطلوب',
        'invalid_data': 'بيانات غير صحيحة',
        'confirm_delete': 'هل أنت متأكد من الحذف؟',

        # التنقل والقوائم
        'home': 'الرئيسية',
        'quick_actions': 'الإجراءات السريعة',
        'recent_activities': 'آخر الأنشطة',
        'important_alerts': 'تنبيهات مهمة',
        'statistics': 'الإحصائيات',
        'all_rights_reserved': 'جميع الحقوق محفوظة',

        # البحث والفلترة
        'search_by_name': 'البحث بالاسم',
        'search_by_passport': 'البحث برقم الجواز',
        'search_by_student_id': 'البحث بالرقم الجامعي',
        'search_results': 'نتائج البحث',
        'no_results': 'لم يتم العثور على نتائج',
        'search_placeholder': 'أدخل كلمة البحث',

        # المدفوعات
        'payment_date': 'تاريخ الدفع',
        'payment_method': 'طريقة الدفع',
        'receipt_number': 'رقم الإيصال',
        'amount': 'المبلغ',
        'cash': 'نقدي',
        'bank_transfer': 'تحويل بنكي',
        'check': 'شيك',
        'credit_card': 'بطاقة ائتمان',
        'other': 'أخرى',

        # التقارير
        'student_statistics': 'إحصائيات الطلاب',
        'institution_statistics': 'إحصائيات المؤسسات',
        'payment_statistics': 'إحصائيات المدفوعات',
        'monthly_payments': 'المدفوعات الشهرية',
        'student_distribution': 'توزيع الطلاب حسب المؤسسة',
        'quick_reports': 'تقارير سريعة',
        'students_list': 'قائمة الطلاب',
        'payments_report': 'تقرير المدفوعات',
        'institutions_report': 'تقرير المؤسسات',
        'financial_report': 'التقرير المالي',
        'export_excel': 'تصدير Excel',
        'export_pdf': 'تصدير PDF',
        'profit_percentage': 'نسبة الربح (%)',
        'net_profit': 'الربح الصافي',
        'total_net_profit': 'إجمالي الأرباح الصافية',
        'upload_document': 'رفع مستند',
        'documents': 'المستندات',
        'document_type': 'نوع المستند',
        'file_size': 'حجم الملف',
        'uploaded_at': 'تاريخ الرفع',
        'download': 'تحميل',
        'passport': 'جواز السفر',
        'certificate': 'شهادة',
        'transcript': 'كشف درجات',
        'photo': 'صورة شخصية',
        'official_document': 'وثيقة رسمية'
    },
    'en': {
        # Main Titles
        'app_title': 'Student Management System - Khalid Soft',
        'dashboard': 'Dashboard',
        'add_student': 'Add New Student',
        'manage_students': 'Manage Students',
        'institutions': 'Educational Institutions',
        'payments': 'Payments',
        'reports': 'Reports',
        'users': 'User Management',
        'settings': 'Settings',
        'search': 'Search',
        'logout': 'Logout',
        'login': 'Login',

        # User Data
        'username': 'Username',
        'password': 'Password',
        'full_name': 'Full Name',
        'role': 'Role',
        'admin': 'Admin',
        'employee': 'Employee',
        'active': 'Active',
        'inactive': 'Inactive',
        'last_login': 'Last Login',
        'created_at': 'Created At',

        # Student Data
        'student_info': 'Student Information',
        'personal_info': 'Personal Information',
        'contact_info': 'Contact Information',
        'academic_info': 'Academic Information',
        'financial_info': 'Financial Information',
        'first_name_ar': 'First Name (Arabic)',
        'last_name_ar': 'Last Name (Arabic)',
        'first_name_en': 'First Name (English)',
        'last_name_en': 'Last Name (English)',
        'passport_number': 'Passport Number',
        'national_id': 'National ID',
        'birth_date': 'Birth Date',
        'nationality': 'Nationality',
        'gender': 'Gender',
        'male': 'Male',
        'female': 'Female',
        'phone': 'Phone Number',
        'email': 'Email Address',
        'address': 'Address',
        'institution': 'Educational Institution',
        'student_id_number': 'Student ID Number',
        'major': 'Major',
        'level': 'Academic Level',
        'enrollment_date': 'Enrollment Date',
        'graduation_date': 'Expected Graduation Date',
        'status': 'Status',
        'tuition_fees': 'Tuition Fees',
        'paid_amount': 'Paid Amount',
        'remaining_amount': 'Remaining Amount',
        'notes': 'Notes',

        # Statistics
        'welcome': 'Welcome to Student Management System',
        'total_students': 'Total Students',
        'active_students': 'Active Students',
        'graduated_students': 'Graduated Students',
        'suspended_students': 'Suspended Students',
        'total_institutions': 'Total Institutions',
        'universities': 'Universities',
        'institutes': 'Institutes',
        'colleges': 'Colleges',
        'total_payments': 'Total Payments',
        'total_amount': 'Total Amount',
        'total_users': 'Total Users',

        # Buttons and Actions
        'save': 'Save',
        'cancel': 'Cancel',
        'edit': 'Edit',
        'delete': 'Delete',
        'view': 'View',
        'add': 'Add',
        'update': 'Update',
        'submit': 'Submit',
        'reset': 'Reset',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'close': 'Close',
        'confirm': 'Confirm',
        'yes': 'Yes',
        'no': 'No',

        # Settings
        'language': 'Language',
        'theme': 'Theme',
        'color_scheme': 'Color Scheme',
        'font_size': 'Font Size',
        'appearance_settings': 'Appearance & Language Settings',
        'text_settings': 'Text Settings',
        'current_settings': 'Current Settings',
        'theme_preview': 'Theme Preview',
        'default_theme': 'Default',
        'dark_theme': 'Dark Mode',
        'light_theme': 'Light Mode',
        'modern_theme': 'Modern',
        'small_font': 'Small',
        'medium_font': 'Medium',
        'large_font': 'Large',
        'sidebar_collapsed': 'Collapse Sidebar by Default',

        # Messages
        'success_message': 'Success!',
        'error_message': 'Error!',
        'warning_message': 'Warning!',
        'info_message': 'Information',
        'no_data': 'No Data Available',
        'loading': 'Loading...',
        'please_wait': 'Please Wait...',
        'required_field': 'Required Field',
        'invalid_data': 'Invalid Data',
        'confirm_delete': 'Are you sure you want to delete?',

        # Navigation and Menus
        'home': 'Home',
        'quick_actions': 'Quick Actions',
        'recent_activities': 'Recent Activities',
        'important_alerts': 'Important Alerts',
        'statistics': 'Statistics',
        'all_rights_reserved': 'All Rights Reserved',

        # Search and Filter
        'search_by_name': 'Search by Name',
        'search_by_passport': 'Search by Passport',
        'search_by_student_id': 'Search by Student ID',
        'search_results': 'Search Results',
        'no_results': 'No Results Found',
        'search_placeholder': 'Enter search term',

        # Payments
        'payment_date': 'Payment Date',
        'payment_method': 'Payment Method',
        'receipt_number': 'Receipt Number',
        'amount': 'Amount',
        'cash': 'Cash',
        'bank_transfer': 'Bank Transfer',
        'check': 'Check',
        'credit_card': 'Credit Card',
        'other': 'Other',

        # Reports
        'student_statistics': 'Student Statistics',
        'institution_statistics': 'Institution Statistics',
        'payment_statistics': 'Payment Statistics',
        'monthly_payments': 'Monthly Payments',
        'student_distribution': 'Student Distribution by Institution',
        'quick_reports': 'Quick Reports',
        'students_list': 'Students List',
        'payments_report': 'Payments Report',
        'institutions_report': 'Institutions Report',
        'financial_report': 'Financial Report',
        'export_excel': 'Export Excel',
        'export_pdf': 'Export PDF',
        'profit_percentage': 'Profit Percentage (%)',
        'net_profit': 'Net Profit',
        'total_net_profit': 'Total Net Profits',
        'upload_document': 'Upload Document',
        'documents': 'Documents',
        'document_type': 'Document Type',
        'file_size': 'File Size',
        'uploaded_at': 'Uploaded At',
        'download': 'Download',
        'passport': 'Passport',
        'certificate': 'Certificate',
        'transcript': 'Transcript',
        'photo': 'Personal Photo',
        'official_document': 'Official Document'
    }
}

# وظائف الترجمة
def get_user_language():
    """الحصول على لغة المستخدم"""
    if 'user_id' in session:
        user_settings = UserSettings.query.filter_by(user_id=session['user_id']).first()
        if user_settings:
            return user_settings.language
    return session.get('language', 'ar')

def translate(key, lang=None):
    """ترجمة النص"""
    if lang is None:
        lang = get_user_language()
    return TRANSLATIONS.get(lang, {}).get(key, key)

# إضافة الترجمة للقوالب
@app.context_processor
def inject_translations():
    return {
        'translate': translate,
        'current_language': get_user_language(),
        'user_settings': get_user_settings() if 'user_id' in session else None
    }

def get_user_settings():
    """الحصول على إعدادات المستخدم"""
    if 'user_id' in session:
        settings = UserSettings.query.filter_by(user_id=session['user_id']).first()
        if not settings:
            # إنشاء إعدادات افتراضية
            settings = UserSettings(user_id=session['user_id'])
            db.session.add(settings)
            db.session.commit()
        return settings
    return None

# وظائف حساب الأرباح
def calculate_net_profit(student):
    """حساب الربح الصافي للطالب"""
    if student.paid_amount and student.profit_percentage:
        return (student.paid_amount * student.profit_percentage) / 100
    return 0.0

def update_student_profit(student):
    """تحديث الربح الصافي للطالب"""
    student.net_profit = calculate_net_profit(student)
    return student.net_profit

# وظائف إدارة الأنشطة
def log_activity(action, description, student_id=None, institution_id=None):
    """تسجيل نشاط جديد"""
    try:
        activity = Activity(
            action=action,
            description=description,
            user_id=session.get('user_id'),
            related_student_id=student_id,
            related_institution_id=institution_id,
            ip_address=request.remote_addr if request else None
        )
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging activity: {e}")

# وظائف إدارة التنبيهات
def create_alert(title, message, alert_type, priority='medium', student_id=None):
    """إنشاء تنبيه جديد"""
    try:
        alert = Alert(
            title=title,
            message=message,
            alert_type=alert_type,
            priority=priority,
            related_student_id=student_id
        )
        db.session.add(alert)
        db.session.commit()
        return alert
    except Exception as e:
        print(f"Error creating alert: {e}")
        return None

def check_payment_alerts():
    """فحص التنبيهات المتعلقة بالمدفوعات"""
    alerts = []

    # البحث عن الطلاب الذين لديهم مبالغ متبقية كبيرة
    students_with_debt = Student.query.filter(Student.remaining_amount > 1000).all()

    for student in students_with_debt:
        # التحقق من عدم وجود تنبيه مشابه حديث
        existing_alert = Alert.query.filter_by(
            alert_type='payment',
            related_student_id=student.id,
            is_read=False
        ).first()

        if not existing_alert:
            alert = create_alert(
                title=f"مبلغ متبقي كبير - {student.full_name_ar}",
                message=f"الطالب {student.full_name_ar} لديه مبلغ متبقي قدره {student.remaining_amount:.2f} دولار",
                alert_type='payment',
                priority='high',
                student_id=student.id
            )
            if alert:
                alerts.append(alert)

    return alerts

def get_recent_activities(limit=10):
    """الحصول على آخر الأنشطة"""
    return Activity.query.order_by(Activity.created_at.desc()).limit(limit).all()

def get_unread_alerts(limit=5):
    """الحصول على التنبيهات غير المقروءة"""
    return Alert.query.filter_by(is_read=False).order_by(Alert.created_at.desc()).limit(limit).all()

# وظائف رفع المستندات
def allowed_file(filename):
    """التحقق من أن نوع الملف مسموح"""
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, student_id, document_type):
    """حفظ الملف المرفوع"""
    if file and allowed_file(file.filename):
        # إنشاء اسم ملف فريد
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"

        # إنشاء مجلد للطالب
        student_folder = os.path.join(app.config['UPLOAD_FOLDER'], f'student_{student_id}')
        if not os.path.exists(student_folder):
            os.makedirs(student_folder)

        # حفظ الملف
        file_path = os.path.join(student_folder, unique_filename)
        file.save(file_path)

        # حفظ معلومات المستند في قاعدة البيانات
        document = StudentDocument(
            student_id=student_id,
            document_type=document_type,
            document_name=filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            uploaded_by=session.get('user_id')
        )

        db.session.add(document)
        db.session.commit()

        return document
    return None

# نماذج قاعدة البيانات
class User(db.Model):
    """نموذج المستخدمين"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # admin, employee
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """تشفير كلمة المرور"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class UserSettings(db.Model):
    """نموذج إعدادات المستخدم"""
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language = db.Column(db.String(10), default='ar')  # ar, en
    theme = db.Column(db.String(20), default='default')  # default, dark, blue, green, etc.
    color_scheme = db.Column(db.String(20), default='blue')  # blue, purple, green, red, etc.
    font_size = db.Column(db.String(10), default='medium')  # small, medium, large
    sidebar_collapsed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقة مع المستخدم
    user = db.relationship('User', backref='settings', lazy=True)

    def __repr__(self):
        return f'<UserSettings for User {self.user_id}>'

class Institution(db.Model):
    """نموذج المؤسسات التعليمية (الجامعات والمعاهد)"""
    __tablename__ = 'institutions'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)  # الاسم بالعربية
    name_en = db.Column(db.String(200), nullable=True)   # الاسم بالإنجليزية
    type = db.Column(db.String(50), nullable=False)      # نوع المؤسسة (جامعة، معهد، كلية)
    city = db.Column(db.String(100), nullable=True)      # المدينة
    country = db.Column(db.String(100), nullable=True)   # البلد
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع الطلاب
    students = db.relationship('Student', backref='institution', lazy=True)
    
    def __repr__(self):
        return f'<Institution {self.name_ar}>'

class Student(db.Model):
    """نموذج الطلاب"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # البيانات الشخصية
    first_name_ar = db.Column(db.String(100), nullable=False)    # الاسم الأول بالعربية
    last_name_ar = db.Column(db.String(100), nullable=False)     # اسم العائلة بالعربية
    first_name_en = db.Column(db.String(100), nullable=True)     # الاسم الأول بالإنجليزية
    last_name_en = db.Column(db.String(100), nullable=True)      # اسم العائلة بالإنجليزية
    
    # بيانات الهوية
    passport_number = db.Column(db.String(50), unique=True, nullable=False)  # رقم الجواز
    national_id = db.Column(db.String(50), nullable=True)        # رقم الهوية الوطنية
    birth_date = db.Column(db.Date, nullable=True)               # تاريخ الميلاد
    nationality = db.Column(db.String(100), nullable=True)       # الجنسية
    gender = db.Column(db.String(10), nullable=True)             # الجنس
    
    # بيانات الاتصال
    phone = db.Column(db.String(20), nullable=True)              # رقم الهاتف
    email = db.Column(db.String(120), nullable=True)             # البريد الإلكتروني
    address = db.Column(db.Text, nullable=True)                  # العنوان
    
    # البيانات الأكاديمية
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    student_id_number = db.Column(db.String(50), nullable=True)  # الرقم الجامعي
    major = db.Column(db.String(200), nullable=True)             # التخصص
    level = db.Column(db.String(50), nullable=True)              # المستوى الدراسي
    enrollment_date = db.Column(db.Date, nullable=True)          # تاريخ التسجيل
    graduation_date = db.Column(db.Date, nullable=True)          # تاريخ التخرج المتوقع
    status = db.Column(db.String(50), default='نشط')            # حالة الطالب
    
    # البيانات المالية
    tuition_fees = db.Column(db.Float, default=0.0)             # الرسوم الدراسية
    paid_amount = db.Column(db.Float, default=0.0)              # المبلغ المدفوع
    remaining_amount = db.Column(db.Float, default=0.0)         # المبلغ المتبقي
    profit_percentage = db.Column(db.Float, default=20.0)       # نسبة الربح %
    net_profit = db.Column(db.Float, default=0.0)               # الربح الصافي
    
    # بيانات النظام
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)                   # ملاحظات
    
    def __repr__(self):
        return f'<Student {self.first_name_ar} {self.last_name_ar}>'
    
    @property
    def full_name_ar(self):
        """الاسم الكامل بالعربية"""
        return f"{self.first_name_ar} {self.last_name_ar}"
    
    @property
    def full_name_en(self):
        """الاسم الكامل بالإنجليزية"""
        if self.first_name_en and self.last_name_en:
            return f"{self.first_name_en} {self.last_name_en}"
        return None

class Payment(db.Model):
    """نموذج المدفوعات"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)                 # المبلغ
    payment_date = db.Column(db.Date, nullable=False)            # تاريخ الدفع
    payment_method = db.Column(db.String(50), nullable=True)     # طريقة الدفع
    receipt_number = db.Column(db.String(100), nullable=True)    # رقم الإيصال
    notes = db.Column(db.Text, nullable=True)                    # ملاحظات
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع الطالب
    student = db.relationship('Student', backref='payments', lazy=True)
    
    def __repr__(self):
        return f'<Payment {self.amount} for Student {self.student_id}>'

class StudentDocument(db.Model):
    """نموذج مستندات الطالب"""
    __tablename__ = 'student_documents'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # نوع المستند (جواز، شهادة، إلخ)
    document_name = db.Column(db.String(200), nullable=False)  # اسم المستند
    file_path = db.Column(db.String(500), nullable=False)     # مسار الملف
    file_size = db.Column(db.Integer, nullable=True)          # حجم الملف
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # العلاقات
    student = db.relationship('Student', backref='documents', lazy=True)
    uploader = db.relationship('User', backref='uploaded_documents', lazy=True)

    def __repr__(self):
        return f'<Document {self.document_name} for Student {self.student_id}>'

class Alert(db.Model):
    """نموذج التنبيهات"""
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)         # عنوان التنبيه
    message = db.Column(db.Text, nullable=False)              # رسالة التنبيه
    alert_type = db.Column(db.String(50), nullable=False)     # نوع التنبيه (payment, student, system)
    priority = db.Column(db.String(20), default='medium')     # الأولوية (low, medium, high)
    is_read = db.Column(db.Boolean, default=False)            # هل تم قراءة التنبيه
    related_student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)

    # العلاقات
    student = db.relationship('Student', backref='alerts', lazy=True)

    def __repr__(self):
        return f'<Alert {self.title}>'

class Activity(db.Model):
    """نموذج الأنشطة"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)        # نوع النشاط
    description = db.Column(db.Text, nullable=False)          # وصف النشاط
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    related_student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    related_institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)      # عنوان IP
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    user = db.relationship('User', backref='activities', lazy=True)
    student = db.relationship('Student', backref='activities', lazy=True)
    institution = db.relationship('Institution', backref='activities', lazy=True)

    def __repr__(self):
        return f'<Activity {self.action} by User {self.user_id}>'

# وظائف المصادقة والصلاحيات
def login_required(f):
    """التحقق من تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """التحقق من صلاحيات المدير"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """الحصول على المستخدم الحالي"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# إنشاء قاعدة البيانات
def create_database():
    """إنشاء جداول قاعدة البيانات"""
    with app.app_context():
        db.create_all()
        print("تم إنشاء قاعدة البيانات بنجاح!")

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    """تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            session['role'] = user.role

            # تحديث آخر تسجيل دخول
            user.last_login = datetime.utcnow()
            db.session.commit()

            flash(f'مرحباً {user.full_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')

    return render_template('login.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('login'))

# الصفحة الرئيسية
@app.route('/')
@login_required
def index():
    """الصفحة الرئيسية"""
    total_students = Student.query.count()
    total_institutions = Institution.query.count()
    active_students = Student.query.filter_by(status='نشط').count()

    # حساب إجمالي الأرباح الصافية
    total_net_profit = db.session.query(db.func.sum(Student.net_profit)).scalar() or 0.0

    # فحص التنبيهات
    check_payment_alerts()

    # الحصول على التنبيهات والأنشطة الحديثة
    recent_alerts = get_unread_alerts(5)
    recent_activities = get_recent_activities(10)

    current_user = get_current_user()

    return render_template('student_index.html',
                         total_students=total_students,
                         total_institutions=total_institutions,
                         active_students=active_students,
                         total_net_profit=total_net_profit,
                         recent_alerts=recent_alerts,
                         recent_activities=recent_activities,
                         current_user=current_user)

# صفحة تسجيل طالب جديد
@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    """تسجيل طالب جديد"""
    if request.method == 'POST':
        try:
            # معالجة التواريخ
            birth_date = None
            enrollment_date = None
            graduation_date = None

            if request.form.get('birth_date'):
                birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
            if request.form.get('enrollment_date'):
                enrollment_date = datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()
            if request.form.get('graduation_date'):
                graduation_date = datetime.strptime(request.form['graduation_date'], '%Y-%m-%d').date()

            # استلام البيانات من النموذج
            student = Student(
                first_name_ar=request.form['first_name_ar'],
                last_name_ar=request.form['last_name_ar'],
                first_name_en=request.form.get('first_name_en'),
                last_name_en=request.form.get('last_name_en'),
                passport_number=request.form['passport_number'],
                national_id=request.form.get('national_id'),
                birth_date=birth_date,
                nationality=request.form.get('nationality'),
                gender=request.form.get('gender'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                address=request.form.get('address'),
                institution_id=request.form['institution_id'],
                student_id_number=request.form.get('student_id_number'),
                major=request.form.get('major'),
                level=request.form.get('level'),
                enrollment_date=enrollment_date,
                graduation_date=graduation_date,
                tuition_fees=float(request.form.get('tuition_fees', 0)),
                profit_percentage=float(request.form.get('profit_percentage', 20.0)),
                status=request.form.get('status', 'نشط'),
                notes=request.form.get('notes')
            )

            # تحديث المبلغ المتبقي والربح الصافي
            student.paid_amount = student.paid_amount or 0.0
            student.remaining_amount = student.tuition_fees - student.paid_amount
            student.net_profit = calculate_net_profit(student)

            db.session.add(student)
            db.session.commit()

            # تسجيل النشاط
            log_activity(
                action='add_student',
                description=f'تم تسجيل طالب جديد: {student.full_name_ar}',
                student_id=student.id
            )

            # إنشاء تنبيه للطالب الجديد
            create_alert(
                title='طالب جديد',
                message=f'تم تسجيل طالب جديد: {student.full_name_ar}',
                alert_type='student',
                priority='medium',
                student_id=student.id
            )

            flash('تم تسجيل الطالب بنجاح!', 'success')
            return redirect(url_for('view_students'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء تسجيل الطالب: {str(e)}', 'error')

    # جلب المؤسسات التعليمية
    institutions = Institution.query.all()
    return render_template('students/add_student.html', institutions=institutions)

# صفحة البحث عن الطلاب
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_students():
    """البحث عن الطلاب"""
    students = []
    search_query = ''

    if request.method == 'POST':
        search_type = request.form.get('search_type')
        search_query = request.form.get('search_query', '').strip()

        if search_query:
            if search_type == 'name':
                students = Student.query.filter(
                    db.or_(
                        Student.first_name_ar.contains(search_query),
                        Student.last_name_ar.contains(search_query),
                        Student.first_name_en.contains(search_query),
                        Student.last_name_en.contains(search_query)
                    )
                ).all()
            elif search_type == 'passport':
                students = Student.query.filter(
                    Student.passport_number.contains(search_query)
                ).all()
            elif search_type == 'student_id':
                students = Student.query.filter(
                    Student.student_id_number.contains(search_query)
                ).all()

    return render_template('students/search.html',
                         students=students,
                         search_query=search_query)

# API للبحث السريع
@app.route('/api/search')
def api_search():
    """API للبحث السريع"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'name')

    if not query:
        return jsonify([])

    students = []

    if search_type == 'name':
        results = Student.query.filter(
            db.or_(
                Student.first_name_ar.contains(query),
                Student.last_name_ar.contains(query),
                Student.first_name_en.contains(query),
                Student.last_name_en.contains(query)
            )
        ).limit(10).all()
    elif search_type == 'passport':
        results = Student.query.filter(
            Student.passport_number.contains(query)
        ).limit(10).all()
    else:
        results = []

    for student in results:
        students.append({
            'id': student.id,
            'name_ar': student.full_name_ar,
            'name_en': student.full_name_en,
            'passport_number': student.passport_number,
            'institution': student.institution.name_ar if student.institution else '',
            'status': student.status
        })

    return jsonify(students)

# API لتحميل قائمة الطلاب للمدفوعات
@app.route('/api/students')
@admin_required
def api_students():
    """API لتحميل قائمة الطلاب"""
    students = Student.query.all()
    students_list = []

    for student in students:
        students_list.append({
            'id': student.id,
            'name': student.full_name_ar,
            'passport': student.passport_number,
            'remaining': student.remaining_amount or 0
        })

    return jsonify(students_list)

# صفحة عرض جميع الطلاب
@app.route('/students')
@login_required
def view_students():
    """عرض جميع الطلاب"""
    page = request.args.get('page', 1, type=int)
    per_page = 20  # عدد الطلاب في كل صفحة

    students = Student.query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('students/list.html', students=students)

# صفحة تفاصيل الطالب
@app.route('/student/<int:student_id>')
@login_required
def student_details(student_id):
    """عرض تفاصيل الطالب"""
    student = Student.query.get_or_404(student_id)
    return render_template('students/details.html', student=student)

# صفحة إدارة المؤسسات التعليمية
@app.route('/institutions')
def institutions():
    """إدارة المؤسسات التعليمية"""
    institutions = Institution.query.all()
    return render_template('students/institutions.html', institutions=institutions)

# صفحة المدفوعات
@app.route('/payments')
@admin_required
def payments():
    """عرض جميع المدفوعات"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    payments = Payment.query.order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # إحصائيات المدفوعات
    total_payments = Payment.query.count()
    total_amount = db.session.query(db.func.sum(Payment.amount)).scalar() or 0

    return render_template('students/payments.html',
                         payments=payments,
                         total_payments=total_payments,
                         total_amount=total_amount)

# إضافة دفعة جديدة
@app.route('/add_payment', methods=['POST'])
@admin_required
def add_payment():
    """إضافة دفعة جديدة"""
    try:
        student_id = request.form['student_id']
        amount = float(request.form['amount'])
        payment_date = datetime.strptime(request.form['payment_date'], '%Y-%m-%d').date()
        payment_method = request.form.get('payment_method')
        receipt_number = request.form.get('receipt_number')
        notes = request.form.get('notes')

        # إنشاء الدفعة
        payment = Payment(
            student_id=student_id,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            receipt_number=receipt_number,
            notes=notes
        )

        db.session.add(payment)

        # تحديث المبلغ المدفوع للطالب
        student = Student.query.get(student_id)
        if student:
            student.paid_amount += amount
            student.remaining_amount = student.tuition_fees - student.paid_amount
            # تحديث الربح الصافي
            student.net_profit = calculate_net_profit(student)

        db.session.commit()

        # تسجيل النشاط
        if student:
            log_activity(
                action='add_payment',
                description=f'تم إضافة دفعة بمبلغ {amount} دولار للطالب {student.full_name_ar}',
                student_id=student.id
            )

        flash('تم إضافة الدفعة بنجاح!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء إضافة الدفعة: {str(e)}', 'error')

    return redirect(url_for('payments'))

# صفحة التقارير
@app.route('/reports')
@admin_required
def reports():
    """عرض التقارير والإحصائيات"""
    # إحصائيات الطلاب
    total_students = Student.query.count()
    active_students = Student.query.filter_by(status='نشط').count()
    graduated_students = Student.query.filter_by(status='متخرج').count()
    suspended_students = Student.query.filter_by(status='متوقف').count()

    # إحصائيات المؤسسات
    total_institutions = Institution.query.count()
    universities = Institution.query.filter_by(type='جامعة').count()
    institutes = Institution.query.filter_by(type='معهد').count()

    # إحصائيات المدفوعات
    total_payments = Payment.query.count()
    total_amount = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    total_fees = db.session.query(db.func.sum(Student.tuition_fees)).scalar() or 0
    total_paid = db.session.query(db.func.sum(Student.paid_amount)).scalar() or 0
    total_remaining = db.session.query(db.func.sum(Student.remaining_amount)).scalar() or 0

    # الطلاب حسب المؤسسة
    students_by_institution = db.session.query(
        Institution.name_ar,
        db.func.count(Student.id).label('count')
    ).join(Student).group_by(Institution.id).all()

    # المدفوعات الشهرية (آخر 6 أشهر)
    monthly_payments = db.session.query(
        db.func.strftime('%Y-%m', Payment.payment_date).label('month'),
        db.func.sum(Payment.amount).label('total')
    ).filter(
        Payment.payment_date >= datetime.now().date().replace(month=datetime.now().month-5 if datetime.now().month > 5 else 1)
    ).group_by(db.func.strftime('%Y-%m', Payment.payment_date)).all()

    return render_template('students/reports.html',
                         total_students=total_students,
                         active_students=active_students,
                         graduated_students=graduated_students,
                         suspended_students=suspended_students,
                         total_institutions=total_institutions,
                         universities=universities,
                         institutes=institutes,
                         total_payments=total_payments,
                         total_amount=total_amount,
                         total_fees=total_fees,
                         total_paid=total_paid,
                         total_remaining=total_remaining,
                         students_by_institution=students_by_institution,
                         monthly_payments=monthly_payments)

# إضافة مؤسسة تعليمية جديدة
@app.route('/add_institution', methods=['POST'])
@login_required
def add_institution():
    """إضافة مؤسسة تعليمية جديدة"""
    try:
        institution = Institution(
            name_ar=request.form['name_ar'],
            name_en=request.form.get('name_en'),
            type=request.form['type'],
            city=request.form.get('city'),
            country=request.form.get('country')
        )

        db.session.add(institution)
        db.session.commit()

        flash('تم إضافة المؤسسة التعليمية بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء إضافة المؤسسة: {str(e)}', 'error')

    return redirect(url_for('institutions'))

# عرض تفاصيل المؤسسة
@app.route('/institution/<int:institution_id>')
@login_required
def institution_details(institution_id):
    """عرض تفاصيل المؤسسة التعليمية"""
    institution = Institution.query.get_or_404(institution_id)

    # جلب الطلاب المنتسبين للمؤسسة
    students = Student.query.filter_by(institution_id=institution_id).all()

    # إحصائيات المؤسسة
    total_students = len(students)
    active_students = len([s for s in students if s.status == 'نشط'])
    graduated_students = len([s for s in students if s.status == 'متخرج'])

    return render_template('students/institution_details.html',
                         institution=institution,
                         students=students,
                         total_students=total_students,
                         active_students=active_students,
                         graduated_students=graduated_students)

# تعديل المؤسسة
@app.route('/edit_institution/<int:institution_id>', methods=['GET', 'POST'])
@login_required
def edit_institution(institution_id):
    """تعديل بيانات المؤسسة التعليمية"""
    institution = Institution.query.get_or_404(institution_id)

    if request.method == 'POST':
        try:
            institution.name_ar = request.form['name_ar']
            institution.name_en = request.form.get('name_en')
            institution.type = request.form['type']
            institution.city = request.form.get('city')
            institution.country = request.form.get('country')

            db.session.commit()
            flash('تم تحديث بيانات المؤسسة بنجاح!', 'success')
            return redirect(url_for('institution_details', institution_id=institution.id))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء تحديث المؤسسة: {str(e)}', 'error')

    return render_template('students/edit_institution.html', institution=institution)

# تعديل الطالب
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    """تعديل بيانات الطالب"""
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        try:
            # معالجة التواريخ
            birth_date = None
            enrollment_date = None
            graduation_date = None

            if request.form.get('birth_date'):
                birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
            if request.form.get('enrollment_date'):
                enrollment_date = datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()
            if request.form.get('graduation_date'):
                graduation_date = datetime.strptime(request.form['graduation_date'], '%Y-%m-%d').date()

            # تحديث البيانات
            student.first_name_ar = request.form['first_name_ar']
            student.last_name_ar = request.form['last_name_ar']
            student.first_name_en = request.form.get('first_name_en')
            student.last_name_en = request.form.get('last_name_en')
            student.passport_number = request.form['passport_number']
            student.national_id = request.form.get('national_id')
            student.birth_date = birth_date
            student.nationality = request.form.get('nationality')
            student.gender = request.form.get('gender')
            student.phone = request.form.get('phone')
            student.email = request.form.get('email')
            student.address = request.form.get('address')
            student.institution_id = request.form['institution_id']
            student.student_id_number = request.form.get('student_id_number')
            student.major = request.form.get('major')
            student.level = request.form.get('level')
            student.enrollment_date = enrollment_date
            student.graduation_date = graduation_date
            student.tuition_fees = float(request.form.get('tuition_fees', 0))
            student.profit_percentage = float(request.form.get('profit_percentage', 20.0))
            student.status = request.form.get('status', 'نشط')
            student.notes = request.form.get('notes')

            # تحديث المبلغ المتبقي والربح الصافي
            student.paid_amount = student.paid_amount or 0.0
            student.remaining_amount = student.tuition_fees - student.paid_amount
            student.net_profit = calculate_net_profit(student)

            db.session.commit()
            flash('تم تحديث بيانات الطالب بنجاح!', 'success')
            return redirect(url_for('student_details', student_id=student.id))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء تحديث الطالب: {str(e)}', 'error')

    # جلب المؤسسات التعليمية
    institutions = Institution.query.all()
    return render_template('students/edit_student.html', student=student, institutions=institutions)

# صفحة إدارة المستخدمين
@app.route('/users')
@admin_required
def manage_users():
    """إدارة المستخدمين"""
    users = User.query.all()
    return render_template('students/users.html', users=users)

# إضافة مستخدم جديد
@app.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    """إضافة مستخدم جديد"""
    try:
        username = request.form['username']
        full_name = request.form['full_name']
        password = request.form['password']
        role = request.form['role']

        # التحقق من عدم وجود المستخدم
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('اسم المستخدم موجود بالفعل!', 'error')
            return redirect(url_for('manage_users'))

        # إنشاء المستخدم الجديد
        user = User(
            username=username,
            full_name=full_name,
            role=role
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('تم إضافة المستخدم بنجاح!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء إضافة المستخدم: {str(e)}', 'error')

    return redirect(url_for('manage_users'))

# تغيير كلمة مرور المستخدم
@app.route('/change_password', methods=['POST'])
@admin_required
def change_password():
    """تغيير كلمة مرور المستخدم"""
    try:
        user_id = request.form['user_id']
        new_password = request.form['new_password']

        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            flash(f'تم تغيير كلمة مرور {user.full_name} بنجاح!', 'success')
        else:
            flash('المستخدم غير موجود!', 'error')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تغيير كلمة المرور: {str(e)}', 'error')

    return redirect(url_for('manage_users'))

# تغيير حالة المستخدم (تفعيل/إلغاء تفعيل)
@app.route('/toggle_user/<int:user_id>')
@admin_required
def toggle_user(user_id):
    """تفعيل أو إلغاء تفعيل المستخدم"""
    try:
        user = User.query.get(user_id)
        if user:
            user.is_active = not user.is_active
            db.session.commit()
            status = 'تم تفعيل' if user.is_active else 'تم إلغاء تفعيل'
            flash(f'{status} المستخدم {user.full_name}', 'success')
        else:
            flash('المستخدم غير موجود!', 'error')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'error')

    return redirect(url_for('manage_users'))

# حذف المستخدم
@app.route('/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    """حذف المستخدم"""
    try:
        user = User.query.get(user_id)
        if user:
            # منع حذف المدير الرئيسي
            if user.username == 'admin':
                flash('لا يمكن حذف المدير الرئيسي!', 'error')
                return redirect(url_for('manage_users'))

            db.session.delete(user)
            db.session.commit()
            flash(f'تم حذف المستخدم {user.full_name} بنجاح!', 'success')
        else:
            flash('المستخدم غير موجود!', 'error')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف المستخدم: {str(e)}', 'error')

    return redirect(url_for('manage_users'))

# صفحة الإعدادات
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """إعدادات المستخدم"""
    user_settings = get_user_settings()

    if request.method == 'POST':
        try:
            # تحديث الإعدادات
            user_settings.language = request.form.get('language', 'ar')
            user_settings.theme = request.form.get('theme', 'default')
            user_settings.color_scheme = request.form.get('color_scheme', 'blue')
            user_settings.font_size = request.form.get('font_size', 'medium')
            user_settings.sidebar_collapsed = 'sidebar_collapsed' in request.form

            db.session.commit()

            # تحديث الجلسة
            session['language'] = user_settings.language
            session['theme'] = user_settings.theme
            session['color_scheme'] = user_settings.color_scheme

            flash('تم حفظ الإعدادات بنجاح!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء حفظ الإعدادات: {str(e)}', 'error')

    return render_template('students/settings.html', settings=user_settings)

# تغيير اللغة
@app.route('/change_language/<language>')
@login_required
def change_language(language):
    """تغيير لغة الواجهة"""
    if language in ['ar', 'en']:
        session['language'] = language

        # تحديث إعدادات المستخدم
        user_settings = get_user_settings()
        if user_settings:
            user_settings.language = language
            db.session.commit()

    return redirect(request.referrer or url_for('index'))

# رفع مستندات الطالب
@app.route('/upload_document/<int:student_id>', methods=['POST'])
@login_required
def upload_document(student_id):
    """رفع مستند للطالب"""
    student = Student.query.get_or_404(student_id)

    if 'document' not in request.files:
        flash('لم يتم اختيار ملف!', 'error')
        return redirect(url_for('student_details', student_id=student_id))

    file = request.files['document']
    document_type = request.form.get('document_type', 'أخرى')

    if file.filename == '':
        flash('لم يتم اختيار ملف!', 'error')
        return redirect(url_for('student_details', student_id=student_id))

    document = save_uploaded_file(file, student_id, document_type)

    if document:
        # تسجيل النشاط
        log_activity(
            action='upload_document',
            description=f'تم رفع مستند ({document_type}) للطالب {student.full_name_ar}',
            student_id=student_id
        )

        flash('تم رفع المستند بنجاح!', 'success')
    else:
        flash('فشل في رفع المستند. تأكد من نوع الملف.', 'error')

    return redirect(url_for('student_details', student_id=student_id))

# عرض المستند
@app.route('/view_document/<int:document_id>')
@login_required
def view_document(document_id):
    """عرض المستند"""
    from flask import send_file
    document = StudentDocument.query.get_or_404(document_id)

    try:
        return send_file(document.file_path, as_attachment=False)
    except FileNotFoundError:
        flash('الملف غير موجود!', 'error')
        return redirect(url_for('student_details', student_id=document.student_id))

# تحميل المستند
@app.route('/download_document/<int:document_id>')
@login_required
def download_document(document_id):
    """تحميل المستند"""
    from flask import send_file
    document = StudentDocument.query.get_or_404(document_id)

    try:
        return send_file(document.file_path, as_attachment=True,
                        download_name=document.document_name)
    except FileNotFoundError:
        flash('الملف غير موجود!', 'error')
        return redirect(url_for('student_details', student_id=document.student_id))

# حذف المستند
@app.route('/delete_document/<int:document_id>', methods=['POST'])
@login_required
def delete_document(document_id):
    """حذف المستند"""
    document = StudentDocument.query.get_or_404(document_id)
    student_id = document.student_id

    try:
        # حذف الملف من النظام
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # حذف السجل من قاعدة البيانات
        db.session.delete(document)
        db.session.commit()

        # تسجيل النشاط
        log_activity(
            action='delete_document',
            description=f'تم حذف مستند ({document.document_type}) للطالب',
            student_id=student_id
        )

        flash('تم حذف المستند بنجاح!', 'success')
    except Exception as e:
        flash(f'فشل في حذف المستند: {str(e)}', 'error')

    return redirect(url_for('student_details', student_id=student_id))

# إضافة المستخدمين الافتراضيين
def create_default_users():
    """إنشاء المستخدمين الافتراضيين"""
    with app.app_context():
        # التحقق من وجود مستخدمين
        if User.query.count() > 0:
            return

        # إنشاء المدير
        admin = User(
            username='admin',
            full_name='المدير العام',
            role='admin'
        )
        admin.set_password('admin123')

        # إنشاء الموظف
        employee = User(
            username='employee',
            full_name='الموظف',
            role='employee'
        )
        employee.set_password('emp123')

        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

        print("تم إنشاء المستخدمين الافتراضيين:")
        print("المدير: admin / admin123")
        print("الموظف: employee / emp123")

# إضافة بيانات تجريبية
def add_sample_data():
    """إضافة بيانات تجريبية للاختبار"""
    with app.app_context():
        # التحقق من وجود بيانات
        if Institution.query.count() > 0:
            return

        # إضافة مؤسسات تعليمية
        institutions = [
            # الجامعات العراقية
            Institution(name_ar='جامعة بغداد', name_en='University of Baghdad',
                       type='جامعة', city='بغداد', country='العراق'),
            Institution(name_ar='الجامعة المستنصرية', name_en='Al-Mustansiriyah University',
                       type='جامعة', city='بغداد', country='العراق'),
            Institution(name_ar='جامعة البصرة', name_en='University of Basrah',
                       type='جامعة', city='البصرة', country='العراق'),
            Institution(name_ar='معهد الإدارة التقني', name_en='Technical Management Institute',
                       type='معهد', city='بغداد', country='العراق'),

            # الجامعات الماليزية الحكومية
            Institution(name_ar='جامعة مالايا', name_en='University of Malaya (UM)',
                       type='جامعة', city='كوالالمبور', country='ماليزيا'),
            Institution(name_ar='جامعة كيبانجسان ماليزيا', name_en='Universiti Kebangsaan Malaysia (UKM)',
                       type='جامعة', city='بانجي', country='ماليزيا'),
            Institution(name_ar='جامعة بوترا ماليزيا', name_en='Universiti Putra Malaysia (UPM)',
                       type='جامعة', city='سردانج', country='ماليزيا'),
            Institution(name_ar='جامعة ساينس ماليزيا', name_en='Universiti Sains Malaysia (USM)',
                       type='جامعة', city='بينانج', country='ماليزيا'),
            Institution(name_ar='جامعة تكنولوجي ماليزيا', name_en='Universiti Teknologi Malaysia (UTM)',
                       type='جامعة', city='جوهور بارو', country='ماليزيا'),
            Institution(name_ar='الجامعة الإسلامية العالمية بماليزيا', name_en='International Islamic University Malaysia (IIUM)',
                       type='جامعة', city='جومباك', country='ماليزيا'),
            Institution(name_ar='جامعة تكنولوجي مارا', name_en='Universiti Teknologi MARA (UiTM)',
                       type='جامعة', city='شاه علم', country='ماليزيا'),
            Institution(name_ar='جامعة أوتارا ماليزيا', name_en='Universiti Utara Malaysia (UUM)',
                       type='جامعة', city='سينتوك', country='ماليزيا'),
            Institution(name_ar='جامعة ماليزيا صباح', name_en='Universiti Malaysia Sabah (UMS)',
                       type='جامعة', city='كوتا كينابالو', country='ماليزيا'),
            Institution(name_ar='جامعة ماليزيا ساراواك', name_en='Universiti Malaysia Sarawak (UNIMAS)',
                       type='جامعة', city='كوتشينغ', country='ماليزيا'),

            # الجامعات الماليزية الخاصة المشهورة
            Institution(name_ar='جامعة تايلور', name_en="Taylor's University",
                       type='جامعة', city='سوبانج جايا', country='ماليزيا'),
            Institution(name_ar='جامعة صنواي', name_en='Sunway University',
                       type='جامعة', city='صنواي', country='ماليزيا'),
            Institution(name_ar='جامعة مونتكيارا', name_en='Monash University Malaysia',
                       type='جامعة', city='صنواي', country='ماليزيا'),
            Institution(name_ar='جامعة نوتنغهام ماليزيا', name_en='University of Nottingham Malaysia',
                       type='جامعة', city='سيمنيه', country='ماليزيا'),
            Institution(name_ar='جامعة كيرتن ماليزيا', name_en='Curtin University Malaysia',
                       type='جامعة', city='ميري', country='ماليزيا'),
            Institution(name_ar='جامعة سوينبرن للتكنولوجيا', name_en='Swinburne University of Technology Sarawak',
                       type='جامعة', city='كوتشينغ', country='ماليزيا'),
            Institution(name_ar='جامعة آسيا باسيفيك للتكنولوجيا والابتكار', name_en='Asia Pacific University (APU)',
                       type='جامعة', city='كوالالمبور', country='ماليزيا'),
            Institution(name_ar='جامعة إنتي الدولية', name_en='INTI International University',
                       type='جامعة', city='نيلاي', country='ماليزيا'),
            Institution(name_ar='جامعة ليمكوكوينغ', name_en='Limkokwing University',
                       type='جامعة', city='سايبرجايا', country='ماليزيا'),
            Institution(name_ar='جامعة هيلب', name_en='HELP University',
                       type='جامعة', city='كوالالمبور', country='ماليزيا'),

            # الكليات والمعاهد الماليزية
            Institution(name_ar='كلية تايلور', name_en="Taylor's College",
                       type='كلية', city='سوبانج جايا', country='ماليزيا'),
            Institution(name_ar='كلية صنواي', name_en='Sunway College',
                       type='كلية', city='صنواي', country='ماليزيا'),
            Institution(name_ar='كلية إنتي', name_en='INTI College',
                       type='كلية', city='سوبانج جايا', country='ماليزيا'),
            Institution(name_ar='كلية سيدايا', name_en='Sedaya College',
                       type='كلية', city='كوالالمبور', country='ماليزيا'),
            Institution(name_ar='معهد جنتنغ للتعليم العالي', name_en='Genting Highlands Institute',
                       type='معهد', city='جنتنغ هايلاندز', country='ماليزيا'),
            Institution(name_ar='معهد كوالالمبور للهندسة', name_en='Kuala Lumpur Engineering Institute',
                       type='معهد', city='كوالالمبور', country='ماليزيا')
        ]

        for inst in institutions:
            db.session.add(inst)

        db.session.commit()
        print("تم إضافة البيانات التجريبية بنجاح!")

if __name__ == '__main__':
    create_database()
    create_default_users()
    add_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5001)

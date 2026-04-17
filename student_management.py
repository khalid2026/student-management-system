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
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()
import os
import json
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# إعدادات قاعدة البيانات للإنتاج والتطوير
if os.environ.get('DATABASE_URL'):
    # للإنتاج (Render.com)
    database_url = os.environ.get('DATABASE_URL')
    # إصلاح URL إذا كان يبدأ بـ postgres:// بدلاً من postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # للتطوير المحلي
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'khalid-soft-student-management-2024')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# إنشاء مجلد الرفع إذا لم يكن موجوداً
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# العملة الوحيدة المدعومة - الرنجت الماليزي
CURRENCY_SYMBOLS = {
    'MYR': 'RM'
}

# العملة الافتراضية
DEFAULT_CURRENCY = 'MYR'

def format_amount_with_currency(amount, currency_code=None):
    """تنسيق المبلغ مع رمز الرنجت الماليزي"""
    return f"RM {amount:,.2f}"

# قاموس الترجمات الكامل
TRANSLATIONS = {
    'ar': {
        # العناوين الرئيسية
        'app_title': 'نظام رايت للاستشارات الطلابية - Right Student Consultancy',
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
        'agent_name': 'اسم الوكيل',
        'agent_commission': 'عمولة الوكيل (%)',
        'agent_commission_amount': 'مبلغ العمولة',
        'study_duration_months': 'مدة الدراسة (بالأشهر)',
        'study_duration_years': 'مدة الدراسة (بالسنوات)',
        'agents': 'الوكلاء',
        'agent': 'وكيل',
        'add_agent': 'إضافة وكيل',
        'edit_agent': 'تعديل وكيل',
        'agent_list': 'قائمة الوكلاء',
        'agent_details': 'تفاصيل الوكيل',
        'commission_percentage': 'نسبة العمولة (%)',
        'total_students': 'إجمالي الطلاب',
        'total_commission': 'إجمالي العمولة',

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
        'app_title': 'Right Student Consultancy System - نظام رايت للاستشارات الطلابية',
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
        'agent_name': 'Agent Name',
        'agent_commission': 'Agent Commission (%)',
        'agent_commission_amount': 'Commission Amount',
        'study_duration_months': 'Study Duration (Months)',
        'study_duration_years': 'Study Duration (Years)',
        'agents': 'Agents',
        'agent': 'Agent',
        'add_agent': 'Add Agent',
        'edit_agent': 'Edit Agent',
        'agent_list': 'Agents List',
        'agent_details': 'Agent Details',
        'commission_percentage': 'Commission Percentage (%)',
        'total_students': 'Total Students',
        'total_commission': 'Total Commission',

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

# إضافة الترجمة والعملات للقوالب
@app.context_processor
def inject_translations():
    return {
        'translate': translate,
        'current_language': get_user_language(),
        'user_settings': get_user_settings() if 'user_id' in session else None,
        'currency_symbols': CURRENCY_SYMBOLS,
        'format_amount_with_currency': format_amount_with_currency
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

def calculate_agent_commission(student):
    """حساب عمولة الوكيل"""
    if student.paid_amount and student.agent_commission:
        return (student.paid_amount * student.agent_commission) / 100
    return 0.0

def update_student_profit(student):
    """تحديث الربح الصافي للطالب وعمولة الوكيل"""
    student.net_profit = calculate_net_profit(student)
    student.agent_commission_amount = calculate_agent_commission(student)
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
                title=f"مبلغ متبقي كبير - {student.full_name_en}",
                message=f"الطالب {student.full_name_en} لديه مبلغ متبقي قدره {student.remaining_amount:.2f} دولار",
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
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

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

# نموذج الوكيل
class Agent(db.Model):
    """نموذج الوكلاء"""
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)              # اسم الوكيل
    phone = db.Column(db.String(20), nullable=True)               # رقم الهاتف
    email = db.Column(db.String(100), nullable=True)              # البريد الإلكتروني
    commission_type = db.Column(db.String(20), default='percentage')  # نوع العمولة (percentage, fixed)
    commission_percentage = db.Column(db.Float, default=5.0)      # نسبة العمولة الافتراضية
    commission_fixed = db.Column(db.Float, default=0.0)           # العمولة الثابتة
    address = db.Column(db.Text, nullable=True)                   # العنوان
    notes = db.Column(db.Text, nullable=True)                     # ملاحظات
    status = db.Column(db.String(20), default='نشط')             # الحالة (نشط، غير نشط)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # تاريخ الإنشاء

    def __repr__(self):
        return f'<Agent {self.name}>'

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
    full_name_en = db.Column(db.String(200), nullable=False)     # الاسم الكامل بالإنجليزية

    # بيانات الهوية
    passport_number = db.Column(db.String(50), unique=True, nullable=False)  # رقم الجواز
    nationality = db.Column(db.String(100), nullable=True)       # الجنسية
    gender = db.Column(db.String(10), nullable=True)             # الجنس
    
    # البيانات الأكاديمية
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    major = db.Column(db.String(200), nullable=True)             # التخصص
    level = db.Column(db.String(50), nullable=True)              # المستوى الدراسي
    enrollment_date = db.Column(db.Date, nullable=True)          # تاريخ التسجيل
    graduation_date = db.Column(db.Date, nullable=True)          # تاريخ التخرج المتوقع
    status = db.Column(db.String(50), default='نشط')            # حالة الطالب
    
    # البيانات المالية
    tuition_fees = db.Column(db.Float, default=0.0)             # الرسوم الدراسية
    currency_symbol = db.Column(db.String(10), default='MYR')   # رمز العملة - رنجت ماليزي
    paid_amount = db.Column(db.Float, default=0.0)              # المبلغ المدفوع
    remaining_amount = db.Column(db.Float, default=0.0)         # المبلغ المتبقي
    profit_percentage = db.Column(db.Float, default=20.0)       # نسبة الربح %
    net_profit = db.Column(db.Float, default=0.0)               # الربح الصافي

    # بيانات الوكيل ومدة الدراسة
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)  # معرف الوكيل
    agent_name = db.Column(db.String(200), nullable=True)       # اسم الوكيل الذي جلب الطالب (للبيانات القديمة)
    agent_commission = db.Column(db.Float, default=0.0)         # نسبة عمولة الوكيل %
    agent_commission_amount = db.Column(db.Float, default=0.0)  # مبلغ عمولة الوكيل المحسوب
    study_duration_months = db.Column(db.Integer, nullable=True) # مدة الدراسة بالأشهر
    
    # بيانات النظام
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)                   # ملاحظات
    
    def __repr__(self):
        return f'<Student {self.full_name_en}>'

class Payment(db.Model):
    """نموذج المدفوعات"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)                 # المبلغ
    currency = db.Column(db.String(10), default='MYR')           # العملة - رنجت ماليزي
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

        user = db.session.get(User, session['user_id'])
        if not user or user.role != 'admin':
            flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """الحصول على المستخدم الحالي"""
    if 'user_id' in session:
        return db.session.get(User, session['user_id'])
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
    # جلب قائمة الوكلاء النشطين
    agents = Agent.query.filter_by(status='نشط').order_by(Agent.name).all()

    if request.method == 'POST':
        try:
            # معالجة التواريخ
            enrollment_date = None
            graduation_date = None

            if request.form.get('enrollment_date'):
                enrollment_date = datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()
            if request.form.get('graduation_date'):
                graduation_date = datetime.strptime(request.form['graduation_date'], '%Y-%m-%d').date()

            # استلام البيانات من النموذج
            student = Student(
                full_name_en=request.form['full_name_en'],
                passport_number=request.form['passport_number'],
                nationality=request.form.get('nationality'),
                gender=request.form.get('gender'),
                institution_id=request.form['institution_id'],
                major=request.form.get('major'),
                level=request.form.get('level'),
                enrollment_date=enrollment_date,
                graduation_date=graduation_date,
                tuition_fees=float(request.form.get('tuition_fees', 0)),
                currency_symbol=request.form.get('currency_symbol', 'MYR'),
                profit_percentage=float(request.form.get('profit_percentage', 20.0)),
                status=request.form.get('status', 'نشط'),
                notes=request.form.get('notes'),
                agent_id=int(request.form.get('agent_id')) if request.form.get('agent_id') else None,
                agent_name=request.form.get('agent_name'),  # للبيانات القديمة
                agent_commission=float(request.form.get('agent_commission', 0.0)),
                study_duration_months=int(request.form.get('study_duration_months', 0)) if request.form.get('study_duration_months') else None
            )

            # تحديث المبلغ المتبقي والربح الصافي وعمولة الوكيل
            student.paid_amount = student.paid_amount or 0.0
            student.remaining_amount = student.tuition_fees - student.paid_amount
            student.net_profit = calculate_net_profit(student)
            student.agent_commission_amount = calculate_agent_commission(student)

            db.session.add(student)
            db.session.commit()

            # تسجيل النشاط
            log_activity(
                action='add_student',
                description=f'تم تسجيل طالب جديد: {student.full_name_en}',
                student_id=student.id
            )

            # إنشاء تنبيه للطالب الجديد
            create_alert(
                title='طالب جديد',
                message=f'تم تسجيل طالب جديد: {student.full_name_en}',
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
    return render_template('students/add_student.html', institutions=institutions, agents=agents)

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
                    Student.full_name_en.contains(search_query)
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
            Student.full_name_en.contains(query)
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
            'name_ar': student.full_name_en,
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
            'name': student.full_name_en,
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

# حذف الطالب
@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id):
    """حذف الطالب"""
    try:
        student = Student.query.get_or_404(student_id)
        student_name = student.full_name_en

        # حذف المدفوعات المرتبطة أولاً
        Payment.query.filter_by(student_id=student_id).delete()

        # حذف الطالب
        db.session.delete(student)
        db.session.commit()

        flash(f'تم حذف الطالب {student_name} بنجاح!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف الطالب: {str(e)}', 'error')

    return redirect(url_for('view_students'))

# عرض مدفوعات الطالب
@app.route('/student/<int:student_id>/payments')
@login_required
def student_payments(student_id):
    """عرض مدفوعات الطالب"""
    student = Student.query.get_or_404(student_id)
    payments = Payment.query.filter_by(student_id=student_id).order_by(Payment.payment_date.desc()).all()
    return render_template('students/student_payments.html', student=student, payments=payments)

# صفحة إدارة المؤسسات التعليمية
@app.route('/institutions')
def institutions():
    """إدارة المؤسسات التعليمية"""
    institutions = Institution.query.all()
    return render_template('students/institutions.html', institutions=institutions)

# حذف المؤسسة
@app.route('/delete_institution/<int:institution_id>', methods=['POST'])
@login_required
@admin_required
def delete_institution(institution_id):
    """حذف المؤسسة التعليمية"""
    try:
        institution = Institution.query.get_or_404(institution_id)

        # التحقق من وجود طلاب مرتبطين بالمؤسسة
        students_count = Student.query.filter_by(institution_id=institution_id).count()
        if students_count > 0:
            flash(f'لا يمكن حذف المؤسسة {institution.name_ar} لأنها مرتبطة بـ {students_count} طالب', 'error')
            return redirect(url_for('institutions'))

        institution_name = institution.name_ar
        db.session.delete(institution)
        db.session.commit()

        flash(f'تم حذف المؤسسة {institution_name} بنجاح!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف المؤسسة: {str(e)}', 'error')

    return redirect(url_for('institutions'))

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
            currency='MYR',  # رنجت ماليزي
            payment_date=payment_date,
            payment_method=payment_method,
            receipt_number=receipt_number,
            notes=notes
        )

        db.session.add(payment)

        # تحديث المبلغ المدفوع للطالب
        student = db.session.get(Student, student_id)
        if student:
            student.paid_amount += amount
            student.remaining_amount = student.tuition_fees - student.paid_amount
            # تحديث الربح الصافي وعمولة الوكيل
            student.net_profit = calculate_net_profit(student)
            student.agent_commission_amount = calculate_agent_commission(student)

        db.session.commit()

        # تسجيل النشاط
        if student:
            log_activity(
                action='add_payment',
                description=f'تم إضافة دفعة بمبلغ {amount} دولار للطالب {student.full_name_en}',
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

    # إحصائيات الوكلاء
    agents_stats = db.session.query(
        Student.agent_name,
        db.func.count(Student.id).label('students_count'),
        db.func.sum(Student.agent_commission_amount).label('total_commission')
    ).filter(
        Student.agent_name.isnot(None),
        Student.agent_name != ''
    ).group_by(Student.agent_name).all()

    # إجمالي عمولات الوكلاء
    total_agent_commissions = db.session.query(db.func.sum(Student.agent_commission_amount)).scalar() or 0

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
                         monthly_payments=monthly_payments,
                         agents_stats=agents_stats,
                         total_agent_commissions=total_agent_commissions)

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
            # طباعة البيانات المستلمة للتشخيص
            print("البيانات المستلمة:", dict(request.form))

            # معالجة التواريخ
            birth_date = None
            enrollment_date = None
            graduation_date = None

            if request.form.get('birth_date'):
                try:
                    birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
                except ValueError:
                    flash('تاريخ الميلاد غير صحيح', 'error')

            if request.form.get('enrollment_date'):
                try:
                    enrollment_date = datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()
                except ValueError:
                    flash('تاريخ التسجيل غير صحيح', 'error')

            if request.form.get('graduation_date'):
                try:
                    graduation_date = datetime.strptime(request.form['graduation_date'], '%Y-%m-%d').date()
                except ValueError:
                    flash('تاريخ التخرج غير صحيح', 'error')

            # التحقق من الحقول المطلوبة
            if not request.form.get('full_name_en'):
                flash('الاسم الكامل مطلوب', 'error')
                raise ValueError('الاسم الكامل مطلوب')

            if not request.form.get('passport_number'):
                flash('رقم الجواز مطلوب', 'error')
                raise ValueError('رقم الجواز مطلوب')

            # تحديث البيانات
            student.full_name_en = request.form['full_name_en'].strip()
            student.passport_number = request.form['passport_number'].strip()
            student.nationality = request.form.get('nationality', '').strip() or None
            student.gender = request.form.get('gender', '').strip() or None

            # التحقق من المؤسسة
            institution_id = request.form.get('institution_id')
            if institution_id:
                student.institution_id = int(institution_id)
            else:
                flash('المؤسسة التعليمية مطلوبة', 'error')
                raise ValueError('المؤسسة التعليمية مطلوبة')


            student.major = request.form.get('major', '').strip() or None
            student.level = request.form.get('level', '').strip() or None
            student.enrollment_date = enrollment_date
            student.graduation_date = graduation_date

            # معالجة الرسوم ونسبة الربح والعملة
            try:
                student.tuition_fees = float(request.form.get('tuition_fees', 0))
            except ValueError:
                student.tuition_fees = 0.0

            # تحديث رمز العملة
            student.currency_symbol = request.form.get('currency_symbol', 'MYR')

            try:
                student.profit_percentage = float(request.form.get('profit_percentage', 20.0))
            except ValueError:
                student.profit_percentage = 20.0

            student.status = request.form.get('status', 'نشط')
            student.notes = request.form.get('notes', '').strip() or None

            # تحديث بيانات الوكيل ومدة الدراسة
            student.agent_name = request.form.get('agent_name', '').strip() or None
            try:
                student.agent_commission = float(request.form.get('agent_commission', 0.0))
            except ValueError:
                student.agent_commission = 0.0

            try:
                study_duration = request.form.get('study_duration_months')
                student.study_duration_months = int(study_duration) if study_duration else None
            except ValueError:
                student.study_duration_months = None

            # تحديث المبلغ المتبقي والربح الصافي وعمولة الوكيل
            student.paid_amount = student.paid_amount or 0.0
            student.remaining_amount = student.tuition_fees - student.paid_amount
            student.net_profit = calculate_net_profit(student)
            student.agent_commission_amount = calculate_agent_commission(student)

            # تحديث تاريخ التعديل
            student.updated_at = datetime.utcnow()

            # حفظ التغييرات
            db.session.commit()

            # تسجيل النشاط
            log_activity(
                action='edit_student',
                description=f'تم تعديل بيانات الطالب {student.full_name_en}',
                student_id=student.id
            )

            flash('تم تحديث بيانات الطالب بنجاح!', 'success')
            return redirect(url_for('student_details', student_id=student.id))

        except Exception as e:
            db.session.rollback()
            print(f"خطأ في تحديث الطالب: {str(e)}")
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

        user = db.session.get(User, user_id)
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
        user = db.session.get(User, user_id)
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
        user = db.session.get(User, user_id)
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
            description=f'تم رفع مستند ({document_type}) للطالب {student.full_name_en}',
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

        # إضافة وكلاء تجريبيين (15 وكيل)
        agents = [
            Agent(name="أحمد محمد الوكيل", phone="+966501234567", email="ahmed@example.com", commission_percentage=5.0, address="الرياض، المملكة العربية السعودية", notes="وكيل متميز مع خبرة 5 سنوات", status="نشط"),
            Agent(name="فاطمة علي الوكيل", phone="+966507654321", email="fatima@example.com", commission_percentage=7.0, address="جدة، المملكة العربية السعودية", notes="وكيل محترف متخصص في الطلاب الدوليين", status="نشط"),
            Agent(name="محمد عبدالله الوكيل", phone="+966509876543", email="mohammed@example.com", commission_percentage=4.5, address="الدمام، المملكة العربية السعودية", notes="وكيل جديد مع إمكانيات عالية", status="نشط"),
            Agent(name="سارة أحمد الوكيل", phone="+966512345678", email="sara@example.com", commission_percentage=6.0, address="مكة المكرمة، المملكة العربية السعودية", notes="وكيل متخصص في الطب والهندسة", status="نشط"),
            Agent(name="عبدالرحمن خالد الوكيل", phone="+966523456789", email="abdulrahman@example.com", commission_percentage=5.5, address="المدينة المنورة، المملكة العربية السعودية", notes="وكيل خبير في الدراسات الإسلامية", status="نشط"),
            Agent(name="نورا سعد الوكيل", phone="+966534567890", email="nora@example.com", commission_percentage=6.5, address="الطائف، المملكة العربية السعودية", notes="وكيل متخصص في إدارة الأعمال", status="نشط"),
            Agent(name="يوسف عمر الوكيل", phone="+966545678901", email="youssef@example.com", commission_percentage=4.0, address="أبها، المملكة العربية السعودية", notes="وكيل جديد متحمس", status="نشط"),
            Agent(name="ريم محمود الوكيل", phone="+966556789012", email="reem@example.com", commission_percentage=7.5, address="تبوك، المملكة العربية السعودية", notes="وكيل متميز في التكنولوجيا", status="نشط"),
            Agent(name="خالد سالم الوكيل", phone="+966567890123", email="khalid@example.com", commission_percentage=5.0, address="حائل، المملكة العربية السعودية", notes="وكيل خبير في العلوم", status="نشط"),
            Agent(name="هند فهد الوكيل", phone="+966578901234", email="hind@example.com", commission_percentage=6.0, address="القصيم، المملكة العربية السعودية", notes="وكيل متخصص في الآداب", status="نشط"),
            Agent(name="عبدالعزيز ناصر الوكيل", phone="+966589012345", email="abdulaziz@example.com", commission_percentage=4.5, address="جازان، المملكة العربية السعودية", notes="وكيل محترف", status="نشط"),
            Agent(name="أمل حسن الوكيل", phone="+966590123456", email="amal@example.com", commission_percentage=6.5, address="نجران، المملكة العربية السعودية", notes="وكيل متميز في التربية", status="نشط"),
            Agent(name="سلطان راشد الوكيل", phone="+966501234568", email="sultan@example.com", commission_percentage=5.5, address="الباحة، المملكة العربية السعودية", notes="وكيل خبير", status="نشط"),
            Agent(name="لينا عادل الوكيل", phone="+966512345679", email="lina@example.com", commission_percentage=7.0, address="الجوف، المملكة العربية السعودية", notes="وكيل متخصص في الصيدلة", status="نشط"),
            Agent(name="ماجد فيصل الوكيل", phone="+966523456780", email="majed@example.com", commission_percentage=4.0, address="عرعر، المملكة العربية السعودية", notes="وكيل جديد واعد", status="غير نشط")
        ]

        for agent in agents:
            db.session.add(agent)

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

        # حفظ البيانات أولاً للحصول على المعرفات
        db.session.commit()

        # إضافة طلاب تجريبيين (25 طالب)
        import random
        from datetime import datetime, timedelta

        # أسماء عربية للطلاب
        first_names_male = ["محمد", "أحمد", "عبدالله", "عبدالرحمن", "يوسف", "خالد", "سعد", "فهد", "عمر", "سلطان", "ناصر", "فيصل", "عبدالعزيز", "راشد", "ماجد"]
        first_names_female = ["فاطمة", "عائشة", "خديجة", "مريم", "زينب", "سارة", "نورا", "هند", "ريم", "أمل", "لينا", "دانا", "رهف", "غلا", "شهد"]
        last_names = ["الأحمد", "المحمد", "العبدالله", "الخالد", "السعد", "الفهد", "العمر", "الناصر", "الفيصل", "الراشد", "الماجد", "الحسن", "العلي", "الصالح", "الكريم"]

        # جلب الوكلاء والمؤسسات
        all_agents = Agent.query.all()
        all_institutions = Institution.query.all()

        students_data = []
        for i in range(25):
            # اختيار جنس عشوائي
            gender = random.choice(["ذكر", "أنثى"])
            first_name = random.choice(first_names_male if gender == "ذكر" else first_names_female)
            last_name = random.choice(last_names)

            # اختيار وكيل ومؤسسة عشوائياً
            agent = random.choice(all_agents)
            institution = random.choice(all_institutions)

            # إنشاء بيانات الطالب
            birth_date = datetime.now() - timedelta(days=random.randint(6570, 10950))  # عمر بين 18-30 سنة
            enrollment_date = datetime.now() - timedelta(days=random.randint(30, 365))  # مسجل منذ شهر إلى سنة

            # العملة الوحيدة - الرنجت الماليزي
            currency_symbol = 'MYR'

            tuition_fees = random.choice([12000, 15000, 18000, 20000, 25000, 30000])
            paid_amount = random.randint(int(tuition_fees * 0.3), int(tuition_fees * 0.9))
            remaining_amount = tuition_fees - paid_amount

            # حساب الربح والعمولة
            profit_percentage = random.choice([15.0, 20.0, 25.0])
            net_profit = (paid_amount * profit_percentage) / 100
            agent_commission_amount = (paid_amount * agent.commission_percentage) / 100

            student = Student(
                full_name_en=f"{first_name} {last_name}",
                passport_number=f"P{random.randint(100000, 999999)}",
                nationality="سعودي" if random.random() > 0.3 else random.choice(["مصري", "سوري", "أردني", "لبناني", "فلسطيني"]),
                gender=gender,
                institution_id=institution.id,
                major=random.choice(["هندسة الحاسوب", "إدارة الأعمال", "الطب", "الصيدلة", "الهندسة المدنية", "علوم الحاسوب", "المحاسبة", "التسويق"]),
                level=random.choice(["السنة الأولى", "السنة الثانية", "السنة الثالثة", "السنة الرابعة"]),
                enrollment_date=enrollment_date,
                status="نشط",
                tuition_fees=tuition_fees,
                currency_symbol=currency_symbol,
                paid_amount=paid_amount,
                remaining_amount=remaining_amount,
                profit_percentage=profit_percentage,
                net_profit=net_profit,
                agent_id=agent.id,
                agent_name=agent.name,  # للتوافق مع البيانات القديمة
                agent_commission=agent.commission_percentage,
                agent_commission_amount=agent_commission_amount,
                study_duration_months=random.choice([24, 36, 48, 60]),
                notes=f"طالب {gender} متميز في تخصص {random.choice(['الرياضيات', 'العلوم', 'الأدب', 'التكنولوجيا'])}"
            )
            students_data.append(student)

        # إضافة الطلاب إلى قاعدة البيانات
        for student in students_data:
            db.session.add(student)

        db.session.commit()

        # إضافة مدفوعات تجريبية لبعض الطلاب
        students = Student.query.all()
        for student in students[:15]:  # أول 15 طالب
            # إضافة مدفوعات إضافية
            for j in range(random.randint(1, 3)):
                payment_amount = random.randint(1000, 5000)
                payment = Payment(
                    student_id=student.id,
                    amount=payment_amount,
                    payment_date=datetime.now() - timedelta(days=random.randint(1, 180)),
                    payment_method=random.choice(["نقد", "تحويل بنكي", "شيك", "بطاقة ائتمان"]),
                    notes=f"دفعة {j+1} للطالب {student.full_name_en}"
                )
                db.session.add(payment)

                # تحديث المبالغ
                student.paid_amount += payment_amount
                student.remaining_amount = student.tuition_fees - student.paid_amount
                student.net_profit = (student.paid_amount * student.profit_percentage) / 100
                student.agent_commission_amount = (student.paid_amount * student.agent_commission) / 100

        db.session.commit()
        print("تم إضافة البيانات التجريبية بنجاح!")

# ==================== إدارة الوكلاء ====================

# قائمة الوكلاء
@app.route('/agents')
@login_required
@admin_required
def agents_list():
    """عرض قائمة الوكلاء مع البحث"""
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '')

    # بناء الاستعلام
    query = Agent.query

    if search:
        query = query.filter(
            db.or_(
                Agent.name.contains(search),
                Agent.phone.contains(search),
                Agent.email.contains(search)
            )
        )

    if status_filter:
        query = query.filter(Agent.status == status_filter)

    agents = query.order_by(Agent.created_at.desc()).all()

    # حساب إحصائيات لكل وكيل
    agents_stats = []
    for agent in agents:
        students = Student.query.filter_by(agent_id=agent.id).all()
        students_count = len(students)
        total_commission = db.session.query(db.func.sum(Student.agent_commission_amount)).filter_by(agent_id=agent.id).scalar() or 0
        agents_stats.append({
            'agent': agent,
            'students': students,
            'students_count': students_count,
            'total_commission': total_commission
        })

    return render_template('students/agents_list.html',
                         agents_stats=agents_stats,
                         search=search,
                         status_filter=status_filter)

# إضافة وكيل جديد
@app.route('/add_agent', methods=['GET', 'POST'])
@login_required
@admin_required
def add_agent():
    """إضافة وكيل جديد"""
    if request.method == 'POST':
        try:
            commission_type = request.form.get('commission_type', 'percentage')
            commission_percentage = 0.0
            commission_fixed = 0.0

            if commission_type == 'percentage':
                commission_percentage = float(request.form.get('commission_percentage', 5.0))
            else:
                commission_fixed = float(request.form.get('commission_fixed', 0.0))

            agent = Agent(
                name=request.form.get('name').strip(),
                phone=request.form.get('phone', '').strip() or None,
                email=request.form.get('email', '').strip() or None,
                commission_type=commission_type,
                commission_percentage=commission_percentage,
                commission_fixed=commission_fixed,
                address=request.form.get('address', '').strip() or None,
                notes=request.form.get('notes', '').strip() or None,
                status=request.form.get('status', 'نشط')
            )

            db.session.add(agent)
            db.session.commit()

            # تم إضافة الوكيل بنجاح

            flash('تم إضافة الوكيل بنجاح!', 'success')
            return redirect(url_for('agents_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'خطأ في إضافة الوكيل: {str(e)}', 'error')

    return render_template('students/add_agent.html')

# تعديل وكيل
@app.route('/edit_agent/<int:agent_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_agent(agent_id):
    """تعديل بيانات وكيل"""
    agent = Agent.query.get_or_404(agent_id)

    if request.method == 'POST':
        try:
            agent.name = request.form.get('name').strip()
            agent.phone = request.form.get('phone', '').strip() or None
            agent.email = request.form.get('email', '').strip() or None
            agent.commission_percentage = float(request.form.get('commission_percentage', 5.0))
            agent.address = request.form.get('address', '').strip() or None
            agent.notes = request.form.get('notes', '').strip() or None
            agent.status = request.form.get('status', 'نشط')

            db.session.commit()

            # تم تعديل الوكيل بنجاح

            flash('تم تحديث بيانات الوكيل بنجاح!', 'success')
            return redirect(url_for('agents_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'خطأ في تحديث بيانات الوكيل: {str(e)}', 'error')

    # حساب إحصائيات الوكيل
    total_students = Student.query.filter_by(agent_id=agent.id).count()
    active_students = Student.query.filter_by(agent_id=agent.id, status='نشط').count()
    total_fees = db.session.query(db.func.sum(Student.tuition_fees)).filter_by(agent_id=agent.id).scalar() or 0
    total_commission = db.session.query(db.func.sum(Student.agent_commission_amount)).filter_by(agent_id=agent.id).scalar() or 0

    agent_stats = {
        'total_students': total_students,
        'active_students': active_students,
        'total_fees': total_fees,
        'total_commission': total_commission
    }

    return render_template('students/edit_agent.html', agent=agent, agent_stats=agent_stats)

# حذف وكيل
@app.route('/delete_agent/<int:agent_id>', methods=['POST'])
@login_required
@admin_required
def delete_agent(agent_id):
    """حذف وكيل"""
    agent = Agent.query.get_or_404(agent_id)

    # التحقق من وجود طلاب مرتبطين بالوكيل
    students_count = Student.query.filter_by(agent_id=agent_id).count()
    if students_count > 0:
        flash(f'لا يمكن حذف الوكيل لأنه مرتبط بـ {students_count} طالب', 'error')
        return redirect(url_for('agents_list'))

    try:
        agent_name = agent.name
        db.session.delete(agent)
        db.session.commit()

        # تم حذف الوكيل بنجاح

        flash('تم حذف الوكيل بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ في حذف الوكيل: {str(e)}', 'error')

    return redirect(url_for('agents_list'))

# تصدير بيانات الوكلاء
@app.route('/export_agents')
@login_required
@admin_required
def export_agents():
    """تصدير بيانات الوكلاء إلى CSV"""
    import csv
    from io import StringIO
    from flask import make_response

    agents = Agent.query.order_by(Agent.name).all()

    output = StringIO()
    writer = csv.writer(output)

    # كتابة العناوين
    writer.writerow(['الاسم', 'الهاتف', 'البريد الإلكتروني', 'نسبة العمولة', 'العنوان', 'الحالة', 'تاريخ الإنشاء'])

    # كتابة البيانات
    for agent in agents:
        writer.writerow([
            agent.name,
            agent.phone or '',
            agent.email or '',
            f"{agent.commission_percentage}%",
            agent.address or '',
            agent.status,
            agent.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    output.seek(0)

    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=agents_export.csv'

    return response

# صفحة اختبار الحقول الجديدة
@app.route('/test_agent_fields')
def test_agent_fields_page():
    """صفحة اختبار الحقول الجديدة"""
    with open('test_page.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    create_database()
    create_default_users()
    # add_sample_data()  # معطل مؤقتاً للسماح بإضافة البيانات يدوياً

    # تشغيل التطبيق
    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

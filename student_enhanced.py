#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة الطلاب المحسن مع الوكلاء ومدة الدراسة
Enhanced Student Management System with Agents and Study Duration
Khalid Soft - نظام إدارة الطلاب المحسن
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
app.config['SECRET_KEY'] = 'khalid-soft-student-enhanced-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students_enhanced.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# إنشاء مجلد الرفع إذا لم يكن موجوداً
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# دالة مساعدة للتحقق من تسجيل الدخول
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# دالة مساعدة للتحقق من صلاحيات المدير
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ===== نماذج قاعدة البيانات المحسنة =====

class User(db.Model):
    """نموذج المستخدمين"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='employee')  # admin, employee
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Agent(db.Model):
    """نموذج الوكلاء - الأشخاص الذين يحضرون الطلاب"""
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)           # اسم الوكيل
    phone = db.Column(db.String(20), nullable=True)            # رقم الهاتف
    email = db.Column(db.String(120), nullable=True)           # البريد الإلكتروني
    address = db.Column(db.Text, nullable=True)                # العنوان
    default_commission = db.Column(db.Float, default=10.0)     # نسبة العمولة الافتراضية %
    is_active = db.Column(db.Boolean, default=True)            # حالة الوكيل
    notes = db.Column(db.Text, nullable=True)                  # ملاحظات
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع الطلاب
    students = db.relationship('Student', backref='agent', lazy=True)
    
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
    """نموذج الطلاب المحسن مع الوكيل ومدة الدراسة"""
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
    
    # مدة الدراسة - الحقل الجديد
    study_duration_value = db.Column(db.Integer, nullable=False, default=12)  # القيمة الرقمية
    study_duration_unit = db.Column(db.String(10), nullable=False, default='months')  # الوحدة (months/years)
    
    # بيانات الوكيل - الحقول الجديدة
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)  # الوكيل
    agent_commission_percentage = db.Column(db.Float, default=0.0)  # نسبة عمولة الوكيل %
    agent_commission_amount = db.Column(db.Float, default=0.0)      # مبلغ عمولة الوكيل
    
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
    
    @property
    def study_duration_display(self):
        """عرض مدة الدراسة بشكل مقروء"""
        if self.study_duration_unit == 'years':
            unit_ar = 'سنة' if self.study_duration_value == 1 else 'سنوات'
            return f"{self.study_duration_value} {unit_ar}"
        else:
            unit_ar = 'شهر' if self.study_duration_value == 1 else 'شهور'
            return f"{self.study_duration_value} {unit_ar}"
    
    def calculate_financials(self):
        """حساب البيانات المالية تلقائياً"""
        # حساب المبلغ المتبقي
        self.remaining_amount = self.tuition_fees - self.paid_amount
        
        # حساب عمولة الوكيل
        if self.agent_commission_percentage > 0:
            self.agent_commission_amount = self.tuition_fees * (self.agent_commission_percentage / 100)
        
        # حساب الربح الصافي (بعد خصم عمولة الوكيل)
        gross_profit = self.tuition_fees * (self.profit_percentage / 100)
        self.net_profit = gross_profit - self.agent_commission_amount

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

# ===== المسارات والوظائف =====

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    """لوحة التحكم الرئيسية"""
    # إحصائيات عامة
    total_students = Student.query.count()
    total_agents = Agent.query.count()
    total_institutions = Institution.query.count()
    
    # إحصائيات مالية
    total_fees = db.session.query(db.func.sum(Student.tuition_fees)).scalar() or 0
    total_paid = db.session.query(db.func.sum(Student.paid_amount)).scalar() or 0
    total_remaining = db.session.query(db.func.sum(Student.remaining_amount)).scalar() or 0
    total_profit = db.session.query(db.func.sum(Student.net_profit)).scalar() or 0
    total_agent_commission = db.session.query(db.func.sum(Student.agent_commission_amount)).scalar() or 0
    
    # الطلاب الجدد (آخر 30 يوم)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_students = Student.query.filter(Student.created_at >= thirty_days_ago).count()
    
    # أفضل الوكلاء (حسب عدد الطلاب)
    top_agents = db.session.query(
        Agent.name,
        db.func.count(Student.id).label('student_count'),
        db.func.sum(Student.agent_commission_amount).label('total_commission')
    ).join(Student).group_by(Agent.id).order_by(db.desc('student_count')).limit(5).all()
    
    return render_template('dashboard_enhanced.html',
                         total_students=total_students,
                         total_agents=total_agents,
                         total_institutions=total_institutions,
                         total_fees=total_fees,
                         total_paid=total_paid,
                         total_remaining=total_remaining,
                         total_profit=total_profit,
                         total_agent_commission=total_agent_commission,
                         new_students=new_students,
                         top_agents=top_agents)

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    """إضافة طالب جديد"""
    if request.method == 'POST':
        try:
            # إنشاء طالب جديد
            student = Student(
                first_name_ar=request.form['first_name_ar'],
                last_name_ar=request.form['last_name_ar'],
                first_name_en=request.form.get('first_name_en'),
                last_name_en=request.form.get('last_name_en'),
                passport_number=request.form['passport_number'],
                national_id=request.form.get('national_id'),
                nationality=request.form.get('nationality'),
                gender=request.form.get('gender'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                address=request.form.get('address'),
                institution_id=int(request.form['institution_id']),
                student_id_number=request.form.get('student_id_number'),
                major=request.form.get('major'),
                level=request.form.get('level'),
                status=request.form.get('status', 'نشط'),
                tuition_fees=float(request.form.get('tuition_fees', 0)),
                profit_percentage=float(request.form.get('profit_percentage', 20)),
                notes=request.form.get('notes')
            )
            
            # مدة الدراسة
            student.study_duration_value = int(request.form.get('study_duration_value', 12))
            student.study_duration_unit = request.form.get('study_duration_unit', 'months')
            
            # بيانات الوكيل
            if request.form.get('agent_id'):
                student.agent_id = int(request.form['agent_id'])
                student.agent_commission_percentage = float(request.form.get('agent_commission_percentage', 0))
            
            # التواريخ
            if request.form.get('birth_date'):
                student.birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
            if request.form.get('enrollment_date'):
                student.enrollment_date = datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()
            if request.form.get('graduation_date'):
                student.graduation_date = datetime.strptime(request.form['graduation_date'], '%Y-%m-%d').date()
            
            # حساب البيانات المالية
            student.calculate_financials()
            
            db.session.add(student)
            db.session.commit()
            
            flash('تم تسجيل الطالب بنجاح!', 'success')
            return redirect(url_for('students'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'error')
    
    # جلب البيانات للنموذج
    institutions = Institution.query.filter_by().all()
    agents = Agent.query.filter_by(is_active=True).all()
    
    return render_template('add_student_enhanced.html', 
                         institutions=institutions, 
                         agents=agents)

@app.route('/students')
@login_required
def students():
    """عرض قائمة الطلاب"""
    students_list = Student.query.order_by(Student.created_at.desc()).all()
    return render_template('students_enhanced.html', students=students_list)

@app.route('/agents')
@login_required
def agents():
    """عرض قائمة الوكلاء"""
    agents_list = Agent.query.order_by(Agent.created_at.desc()).all()
    return render_template('agents.html', agents=agents_list)

@app.route('/add_agent', methods=['POST'])
@login_required
def add_agent():
    """إضافة وكيل جديد"""
    try:
        agent = Agent(
            name=request.form['name'],
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            default_commission=float(request.form.get('default_commission', 10)),
            notes=request.form.get('notes')
        )
        
        db.session.add(agent)
        db.session.commit()
        
        flash('تم إضافة الوكيل بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'error')
    
    return redirect(url_for('agents'))

def create_default_data():
    """إنشاء البيانات الافتراضية"""
    # إنشاء مستخدم مدير افتراضي
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@khalidsoft.com',
            full_name='مدير النظام',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # إنشاء مستخدم موظف افتراضي
    if not User.query.filter_by(username='employee').first():
        employee = User(
            username='employee',
            email='employee@khalidsoft.com',
            full_name='موظف النظام',
            role='employee'
        )
        employee.set_password('employee123')
        db.session.add(employee)
    
    # إنشاء مؤسسة افتراضية
    if not Institution.query.first():
        institution = Institution(
            name_ar='جامعة الملك سعود',
            name_en='King Saud University',
            type='جامعة',
            city='الرياض',
            country='السعودية'
        )
        db.session.add(institution)
    
    # إنشاء وكيل افتراضي
    if not Agent.query.first():
        agent = Agent(
            name='أحمد محمد - وكيل افتراضي',
            phone='+966501234567',
            email='agent@example.com',
            default_commission=15.0,
            notes='وكيل افتراضي للاختبار'
        )
        db.session.add(agent)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_data()
    
    app.run(host='0.0.0.0', port=5004, debug=True)

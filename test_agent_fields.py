#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الحقول الجديدة للوكيل ومدة الدراسة
Test script for new agent and study duration fields
"""

from student_management import app, db, Student, Institution

def test_agent_fields():
    """اختبار الحقول الجديدة"""
    with app.app_context():
        # التحقق من وجود الحقول في نموذج Student
        student_columns = [column.name for column in Student.__table__.columns]
        
        print("🔍 فحص الحقول الموجودة في نموذج Student:")
        print("=" * 50)
        
        required_fields = [
            'agent_name',
            'agent_commission', 
            'agent_commission_amount',
            'study_duration_months'
        ]
        
        for field in required_fields:
            if field in student_columns:
                print(f"✅ {field} - موجود")
            else:
                print(f"❌ {field} - غير موجود")
        
        print("\n📋 جميع الحقول الموجودة:")
        print("-" * 30)
        for column in student_columns:
            print(f"  • {column}")
        
        # اختبار إنشاء طالب جديد مع الحقول الجديدة
        print("\n🧪 اختبار إنشاء طالب جديد:")
        print("=" * 50)
        
        try:
            # البحث عن مؤسسة موجودة
            institution = Institution.query.first()
            if not institution:
                print("❌ لا توجد مؤسسات في قاعدة البيانات")
                return
            
            # إنشاء طالب جديد
            test_student = Student(
                first_name_ar="أحمد",
                last_name_ar="محمد",
                passport_number="TEST123456",
                institution_id=institution.id,
                agent_name="وكيل تجريبي",
                agent_commission=5.0,
                study_duration_months=24,
                tuition_fees=10000.0,
                paid_amount=5000.0
            )
            
            # حساب المبالغ
            test_student.remaining_amount = test_student.tuition_fees - test_student.paid_amount
            test_student.net_profit = (test_student.paid_amount * 20.0) / 100  # 20% ربح افتراضي
            test_student.agent_commission_amount = (test_student.paid_amount * test_student.agent_commission) / 100
            
            db.session.add(test_student)
            db.session.commit()
            
            print("✅ تم إنشاء الطالب التجريبي بنجاح!")
            print(f"   الاسم: {test_student.full_name_ar}")
            print(f"   الوكيل: {test_student.agent_name}")
            print(f"   نسبة العمولة: {test_student.agent_commission}%")
            print(f"   مبلغ العمولة: ${test_student.agent_commission_amount:.2f}")
            print(f"   مدة الدراسة: {test_student.study_duration_months} شهر")
            print(f"   مدة الدراسة: {test_student.study_duration_months / 12:.1f} سنة")
            
            # حذف الطالب التجريبي
            db.session.delete(test_student)
            db.session.commit()
            print("✅ تم حذف الطالب التجريبي")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء الطالب: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    print("🎓 اختبار نظام إدارة الطلاب - Khalid Soft")
    print("🧪 اختبار الحقول الجديدة للوكيل ومدة الدراسة")
    print("=" * 60)
    test_agent_fields()
    print("=" * 60)
    print("✅ انتهى الاختبار")

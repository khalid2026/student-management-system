import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useAuth } from '../contexts/AuthContext';

export default function RegisterScreen({ navigation }) {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    password: '',
    confirmPassword: '',
    vehicleType: '',
    vehicleNumber: '',
  });
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  const handleRegister = async () => {
    // التحقق من البيانات
    if (!formData.name || !formData.phone || !formData.password) {
      Alert.alert('خطأ', 'الرجاء ملء جميع الحقول المطلوبة');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      Alert.alert('خطأ', 'كلمة المرور غير متطابقة');
      return;
    }

    if (formData.password.length < 6) {
      Alert.alert('خطأ', 'كلمة المرور يجب أن تكون 6 أحرف على الأقل');
      return;
    }

    console.log('🟡 RegisterScreen: Starting registration...');
    console.log('🟡 Form data:', formData);

    setLoading(true);
    const result = await register({
      name: formData.name,
      phone: formData.phone,
      password: formData.password,
      vehicleType: formData.vehicleType,
      vehicleNumber: formData.vehicleNumber,
    });
    setLoading(false);

    console.log('🟡 RegisterScreen: Registration result:', result);

    if (!result.success) {
      console.error('🔴 RegisterScreen: Registration failed:', result.error);
      Alert.alert('خطأ', result.error);
    } else {
      console.log('✅ RegisterScreen: Registration successful!');
      Alert.alert('نجح', 'تم التسجيل بنجاح!');
    }
  };

  const updateField = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>إنشاء حساب جديد</Text>
          <Text style={styles.subtitle}>انضم إلى فريق وصل للتوصيل</Text>
        </View>

        <View style={styles.form}>
          <View style={styles.inputContainer}>
            <Text style={styles.label}>الاسم الكامل *</Text>
            <TextInput
              style={styles.input}
              placeholder="أدخل اسمك الكامل"
              value={formData.name}
              onChangeText={(value) => updateField('name', value)}
              textAlign="right"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.label}>رقم الهاتف *</Text>
            <TextInput
              style={styles.input}
              placeholder="7xxxxxxxx"
              value={formData.phone}
              onChangeText={(value) => updateField('phone', value)}
              keyboardType="phone-pad"
              textAlign="right"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.label}>كلمة المرور *</Text>
            <TextInput
              style={styles.input}
              placeholder="6 أحرف على الأقل"
              value={formData.password}
              onChangeText={(value) => updateField('password', value)}
              secureTextEntry
              textAlign="right"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.label}>تأكيد كلمة المرور *</Text>
            <TextInput
              style={styles.input}
              placeholder="أعد إدخال كلمة المرور"
              value={formData.confirmPassword}
              onChangeText={(value) => updateField('confirmPassword', value)}
              secureTextEntry
              textAlign="right"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.label}>نوع المركبة</Text>
            <TextInput
              style={styles.input}
              placeholder="دراجة نارية / سيارة / شاحنة"
              value={formData.vehicleType}
              onChangeText={(value) => updateField('vehicleType', value)}
              textAlign="right"
            />
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.label}>رقم اللوحة</Text>
            <TextInput
              style={styles.input}
              placeholder="رقم لوحة المركبة"
              value={formData.vehicleNumber}
              onChangeText={(value) => updateField('vehicleNumber', value)}
              textAlign="right"
            />
          </View>

          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleRegister}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>إنشاء الحساب</Text>
            )}
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.linkButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.linkText}>
              لديك حساب؟ <Text style={styles.linkTextBold}>سجل دخول</Text>
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  form: {
    width: '100%',
  },
  inputContainer: {
    marginBottom: 15,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 6,
    textAlign: 'right',
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  button: {
    backgroundColor: '#27ae60',
    borderRadius: 10,
    padding: 15,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonDisabled: {
    backgroundColor: '#95a5a6',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  linkButton: {
    marginTop: 20,
    marginBottom: 30,
    alignItems: 'center',
  },
  linkText: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  linkTextBold: {
    color: '#3498db',
    fontWeight: 'bold',
  },
});


import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { profileService } from '../services/api';

export default function ProfileScreen({ navigation }) {
  const { driver, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    vehicleType: '',
    vehicleNumber: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const statsData = await profileService.getStats();
      setStats(statsData);
      
      // تحميل بيانات السائق
      if (driver) {
        setFormData({
          name: driver.name || '',
          phone: driver.phone || '',
          vehicleType: driver.vehicleType || '',
          vehicleNumber: driver.vehicleNumber || '',
        });
      }
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      await profileService.updateProfile(formData);
      Alert.alert('نجح', 'تم تحديث البيانات بنجاح');
      setEditing(false);
      loadData();
    } catch (error) {
      Alert.alert('خطأ', 'فشل تحديث البيانات');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    Alert.alert('تسجيل الخروج', 'هل أنت متأكد من تسجيل الخروج؟', [
      { text: 'إلغاء', style: 'cancel' },
      { text: 'تسجيل الخروج', onPress: logout, style: 'destructive' },
    ]);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* رأس الصفحة */}
      <View style={styles.header}>
        <View style={styles.avatarContainer}>
          <Text style={styles.avatar}>👤</Text>
        </View>
        <Text style={styles.driverName}>{driver?.name || 'السائق'}</Text>
        <Text style={styles.driverPhone}>{driver?.phone}</Text>
      </View>

      {/* الإحصائيات */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>📦</Text>
          <Text style={styles.statValue}>{stats?.totalOrders || 0}</Text>
          <Text style={styles.statLabel}>إجمالي الطلبات</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statIcon}>💰</Text>
          <Text style={styles.statValue}>{stats?.totalEarnings || 0}</Text>
          <Text style={styles.statLabel}>الأرباح (ريال)</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statIcon}>⭐</Text>
          <Text style={styles.statValue}>{stats?.rating || '0.0'}</Text>
          <Text style={styles.statLabel}>التقييم</Text>
        </View>
      </View>

      {/* معلومات الحساب */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>معلومات الحساب</Text>
          {!editing && (
            <TouchableOpacity onPress={() => setEditing(true)}>
              <Text style={styles.editButton}>✏️ تعديل</Text>
            </TouchableOpacity>
          )}
        </View>

        <View style={styles.card}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>الاسم</Text>
            <TextInput
              style={[styles.input, !editing && styles.inputDisabled]}
              value={formData.name}
              onChangeText={(text) => setFormData({ ...formData, name: text })}
              editable={editing}
              textAlign="right"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>رقم الهاتف</Text>
            <TextInput
              style={[styles.input, styles.inputDisabled]}
              value={formData.phone}
              editable={false}
              textAlign="right"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>نوع المركبة</Text>
            <TextInput
              style={[styles.input, !editing && styles.inputDisabled]}
              value={formData.vehicleType}
              onChangeText={(text) =>
                setFormData({ ...formData, vehicleType: text })
              }
              editable={editing}
              textAlign="right"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>رقم المركبة</Text>
            <TextInput
              style={[styles.input, !editing && styles.inputDisabled]}
              value={formData.vehicleNumber}
              onChangeText={(text) =>
                setFormData({ ...formData, vehicleNumber: text })
              }
              editable={editing}
              textAlign="right"
            />
          </View>

          {editing && (
            <View style={styles.buttonRow}>
              <TouchableOpacity
                style={[styles.button, styles.cancelButton]}
                onPress={() => {
                  setEditing(false);
                  loadData();
                }}
              >
                <Text style={styles.buttonText}>إلغاء</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, styles.saveButton]}
                onPress={handleSave}
              >
                <Text style={styles.buttonText}>حفظ</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      </View>

      {/* الإعدادات */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>الإعدادات</Text>
        <View style={styles.card}>
          <TouchableOpacity style={styles.menuItem}>
            <Text style={styles.menuIcon}>🔔</Text>
            <Text style={styles.menuText}>الإشعارات</Text>
            <Text style={styles.menuArrow}>←</Text>
          </TouchableOpacity>

          <View style={styles.menuDivider} />

          <TouchableOpacity style={styles.menuItem}>
            <Text style={styles.menuIcon}>🌙</Text>
            <Text style={styles.menuText}>الوضع الليلي</Text>
            <Text style={styles.menuArrow}>←</Text>
          </TouchableOpacity>

          <View style={styles.menuDivider} />

          <TouchableOpacity style={styles.menuItem}>
            <Text style={styles.menuIcon}>🌐</Text>
            <Text style={styles.menuText}>اللغة</Text>
            <Text style={styles.menuArrow}>←</Text>
          </TouchableOpacity>

          <View style={styles.menuDivider} />

          <TouchableOpacity style={styles.menuItem}>
            <Text style={styles.menuIcon}>ℹ️</Text>
            <Text style={styles.menuText}>حول التطبيق</Text>
            <Text style={styles.menuArrow}>←</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* زر تسجيل الخروج */}
      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>🚪 تسجيل الخروج</Text>
      </TouchableOpacity>

      <View style={styles.footer}>
        <Text style={styles.footerText}>نظام وصل للتوصيل v1.0</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    backgroundColor: '#3498db',
    padding: 40,
    paddingTop: 60,
    alignItems: 'center',
  },
  avatarContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  avatar: {
    fontSize: 40,
  },
  driverName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  driverPhone: {
    fontSize: 14,
    color: '#ecf0f1',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 16,
    backgroundColor: '#fff',
    marginTop: -20,
    marginHorizontal: 16,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statCard: {
    alignItems: 'center',
  },
  statIcon: {
    fontSize: 24,
    marginBottom: 4,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  statLabel: {
    fontSize: 12,
    color: '#7f8c8d',
    marginTop: 4,
  },
  section: {
    marginTop: 16,
    paddingHorizontal: 16,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  editButton: {
    fontSize: 14,
    color: '#3498db',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 4,
  },
  input: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    color: '#2c3e50',
  },
  inputDisabled: {
    backgroundColor: '#ecf0f1',
    color: '#7f8c8d',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  button: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 4,
  },
  saveButton: {
    backgroundColor: '#27ae60',
  },
  cancelButton: {
    backgroundColor: '#95a5a6',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
  },
  menuIcon: {
    fontSize: 20,
    marginRight: 12,
  },
  menuText: {
    flex: 1,
    fontSize: 16,
    color: '#2c3e50',
  },
  menuArrow: {
    fontSize: 16,
    color: '#7f8c8d',
  },
  menuDivider: {
    height: 1,
    backgroundColor: '#ecf0f1',
  },
  logoutButton: {
    backgroundColor: '#e74c3c',
    marginHorizontal: 16,
    marginTop: 24,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  logoutText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  footer: {
    padding: 24,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#7f8c8d',
  },
});


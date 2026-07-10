import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  RefreshControl,
  Alert,
} from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { profileService } from '../services/api';

export default function HomeScreen({ navigation }) {
  const { driver, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await profileService.getStats();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadStats();
    setRefreshing(false);
  };

  const handleLogout = () => {
    Alert.alert('تسجيل الخروج', 'هل أنت متأكد من تسجيل الخروج؟', [
      { text: 'إلغاء', style: 'cancel' },
      { text: 'تسجيل الخروج', onPress: logout, style: 'destructive' },
    ]);
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* رأس الصفحة */}
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>مرحباً،</Text>
          <Text style={styles.driverName}>{driver?.name || 'السائق'}</Text>
        </View>
        <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
          <Text style={styles.logoutText}>🚪</Text>
        </TouchableOpacity>
      </View>

      {/* بطاقات الإحصائيات */}
      <View style={styles.statsContainer}>
        <View style={[styles.statCard, styles.statCardPrimary]}>
          <Text style={styles.statIcon}>📦</Text>
          <Text style={styles.statValue}>{stats?.totalOrders || 0}</Text>
          <Text style={styles.statLabel}>إجمالي الطلبات</Text>
        </View>

        <View style={[styles.statCard, styles.statCardSuccess]}>
          <Text style={styles.statIcon}>✅</Text>
          <Text style={styles.statValue}>{stats?.completedOrders || 0}</Text>
          <Text style={styles.statLabel}>طلبات مكتملة</Text>
        </View>

        <View style={[styles.statCard, styles.statCardWarning]}>
          <Text style={styles.statIcon}>💰</Text>
          <Text style={styles.statValue}>{stats?.earnings || 0} ريال</Text>
          <Text style={styles.statLabel}>الأرباح</Text>
        </View>

        <View style={[styles.statCard, styles.statCardInfo]}>
          <Text style={styles.statIcon}>⭐</Text>
          <Text style={styles.statValue}>{stats?.rating || '0.0'}</Text>
          <Text style={styles.statLabel}>التقييم</Text>
        </View>
      </View>

      {/* الإجراءات السريعة */}
      <View style={styles.actionsContainer}>
        <Text style={styles.sectionTitle}>الإجراءات السريعة</Text>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('AvailableOrders')}
        >
          <Text style={styles.actionIcon}>📋</Text>
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>الطلبات المتاحة</Text>
            <Text style={styles.actionSubtitle}>
              عرض الطلبات الجديدة المتاحة
            </Text>
          </View>
          <Text style={styles.actionArrow}>←</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('MyOrders')}
        >
          <Text style={styles.actionIcon}>🚗</Text>
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>طلباتي الحالية</Text>
            <Text style={styles.actionSubtitle}>
              الطلبات التي قبلتها وجاري توصيلها
            </Text>
          </View>
          <Text style={styles.actionArrow}>←</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('OrderHistory')}
        >
          <Text style={styles.actionIcon}>📜</Text>
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>سجل الطلبات</Text>
            <Text style={styles.actionSubtitle}>عرض جميع الطلبات السابقة</Text>
          </View>
          <Text style={styles.actionArrow}>←</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Profile')}
        >
          <Text style={styles.actionIcon}>👤</Text>
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>الملف الشخصي</Text>
            <Text style={styles.actionSubtitle}>عرض وتعديل بياناتك</Text>
          </View>
          <Text style={styles.actionArrow}>←</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#3498db',
    paddingTop: 50,
  },
  greeting: {
    fontSize: 16,
    color: '#fff',
  },
  driverName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  logoutButton: {
    padding: 10,
  },
  logoutText: {
    fontSize: 24,
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 10,
    marginTop: -30,
  },
  statCard: {
    width: '48%',
    margin: '1%',
    padding: 20,
    borderRadius: 15,
    alignItems: 'center',
  },
  statCardPrimary: {
    backgroundColor: '#3498db',
  },
  statCardSuccess: {
    backgroundColor: '#27ae60',
  },
  statCardWarning: {
    backgroundColor: '#f39c12',
  },
  statCardInfo: {
    backgroundColor: '#9b59b6',
  },
  statIcon: {
    fontSize: 30,
    marginBottom: 10,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  statLabel: {
    fontSize: 12,
    color: '#fff',
  },
  actionsContainer: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 15,
    textAlign: 'right',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  actionIcon: {
    fontSize: 30,
    marginRight: 15,
  },
  actionContent: {
    flex: 1,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'right',
  },
  actionSubtitle: {
    fontSize: 12,
    color: '#7f8c8d',
    marginTop: 2,
    textAlign: 'right',
  },
  actionArrow: {
    fontSize: 20,
    color: '#bdc3c7',
  },
});


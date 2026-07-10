import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  Linking,
} from 'react-native';
import { orderService } from '../services/api';

export default function OrderDetailsScreen({ route, navigation }) {
  const { orderId } = route.params;
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadOrderDetails();
  }, []);

  const loadOrderDetails = async () => {
    try {
      const data = await orderService.getOrderDetails(orderId);
      setOrder(data);
    } catch (error) {
      console.error('Error loading order details:', error);
      Alert.alert('خطأ', 'فشل تحميل تفاصيل الطلب');
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptOrder = async () => {
    Alert.alert(
      'قبول الطلب',
      'هل أنت متأكد من قبول هذا الطلب؟',
      [
        { text: 'إلغاء', style: 'cancel' },
        {
          text: 'قبول',
          onPress: async () => {
            setActionLoading(true);
            try {
              await orderService.acceptOrder(orderId);
              Alert.alert('نجح', 'تم قبول الطلب بنجاح');
              navigation.goBack();
            } catch (error) {
              Alert.alert('خطأ', error.response?.data?.message || 'فشل قبول الطلب');
            } finally {
              setActionLoading(false);
            }
          },
        },
      ]
    );
  };

  const handleRejectOrder = async () => {
    Alert.alert(
      'رفض الطلب',
      'هل أنت متأكد من رفض هذا الطلب؟',
      [
        { text: 'إلغاء', style: 'cancel' },
        {
          text: 'رفض',
          style: 'destructive',
          onPress: async () => {
            setActionLoading(true);
            try {
              await orderService.rejectOrder(orderId, 'السائق رفض الطلب');
              Alert.alert('تم', 'تم رفض الطلب');
              navigation.goBack();
            } catch (error) {
              Alert.alert('خطأ', 'فشل رفض الطلب');
            } finally {
              setActionLoading(false);
            }
          },
        },
      ]
    );
  };

  const handleUpdateStatus = async (newStatus) => {
    const statusMessages = {
      picked_up: 'تم استلام الطلب',
      in_transit: 'جاري التوصيل',
      delivered: 'تم التوصيل',
    };

    Alert.alert(
      'تحديث الحالة',
      `هل تريد تحديث الحالة إلى: ${statusMessages[newStatus]}؟`,
      [
        { text: 'إلغاء', style: 'cancel' },
        {
          text: 'تحديث',
          onPress: async () => {
            setActionLoading(true);
            try {
              await orderService.updateOrderStatus(orderId, newStatus);
              Alert.alert('نجح', 'تم تحديث حالة الطلب');
              loadOrderDetails();
            } catch (error) {
              Alert.alert('خطأ', 'فشل تحديث الحالة');
            } finally {
              setActionLoading(false);
            }
          },
        },
      ]
    );
  };

  const openMap = (latitude, longitude, label) => {
    const url = `https://www.google.com/maps/search/?api=1&query=${latitude},${longitude}`;
    Linking.openURL(url);
  };

  const callCustomer = (phone) => {
    Linking.openURL(`tel:${phone}`);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  if (!order) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>لم يتم العثور على الطلب</Text>
      </View>
    );
  }

  const statusColors = {
    pending: '#f39c12',
    accepted: '#3498db',
    picked_up: '#9b59b6',
    in_transit: '#e67e22',
    delivered: '#27ae60',
    cancelled: '#e74c3c',
  };

  const statusLabels = {
    pending: 'قيد الانتظار',
    accepted: 'مقبول',
    picked_up: 'تم الاستلام',
    in_transit: 'جاري التوصيل',
    delivered: 'تم التوصيل',
    cancelled: 'ملغي',
  };

  return (
    <ScrollView style={styles.container}>
      {/* رأس الصفحة */}
      <View style={styles.header}>
        <View style={styles.headerTop}>
          <View>
            <Text style={styles.orderNumber}>#{order.orderNumber}</Text>
            <Text style={styles.orderDate}>
              {new Date(order.createdAt).toLocaleString('ar-YE')}
            </Text>
          </View>
          <View
            style={[
              styles.statusBadge,
              { backgroundColor: statusColors[order.status] },
            ]}
          >
            <Text style={styles.statusText}>{statusLabels[order.status]}</Text>
          </View>
        </View>
      </View>

      {/* معلومات العميل */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>معلومات العميل</Text>
        <View style={styles.card}>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>الاسم:</Text>
            <Text style={styles.infoValue}>{order.customer?.name || 'غير متوفر'}</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>الهاتف:</Text>
            <TouchableOpacity onPress={() => callCustomer(order.customer?.phone)}>
              <Text style={[styles.infoValue, styles.phoneLink]}>
                {order.customer?.phone || 'غير متوفر'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* عنوان الاستلام */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>عنوان الاستلام</Text>
        <View style={styles.card}>
          <Text style={styles.addressText}>{order.pickupAddress?.address}</Text>
          <Text style={styles.cityText}>
            {order.pickupAddress?.city}, {order.pickupAddress?.district}
          </Text>
          <TouchableOpacity
            style={styles.mapButton}
            onPress={() =>
              openMap(
                order.pickupAddress?.coordinates?.latitude,
                order.pickupAddress?.coordinates?.longitude,
                'موقع الاستلام'
              )
            }
          >
            <Text style={styles.mapButtonText}>📍 فتح الخريطة</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* عنوان التوصيل */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>عنوان التوصيل</Text>
        <View style={styles.card}>
          <Text style={styles.addressText}>{order.deliveryAddress?.address}</Text>
          <Text style={styles.cityText}>
            {order.deliveryAddress?.city}, {order.deliveryAddress?.district}
          </Text>
          <TouchableOpacity
            style={styles.mapButton}
            onPress={() =>
              openMap(
                order.deliveryAddress?.coordinates?.latitude,
                order.deliveryAddress?.coordinates?.longitude,
                'موقع التوصيل'
              )
            }
          >
            <Text style={styles.mapButtonText}>📍 فتح الخريطة</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* تفاصيل الطلب */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>تفاصيل الطلب</Text>
        <View style={styles.card}>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>نوع الطلب:</Text>
            <Text style={styles.infoValue}>{order.orderType || 'توصيل عادي'}</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>المسافة:</Text>
            <Text style={styles.infoValue}>{order.distance?.toFixed(1)} كم</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>رسوم التوصيل:</Text>
            <Text style={[styles.infoValue, styles.priceText]}>
              {order.deliveryFee} ريال
            </Text>
          </View>
          {order.notes && (
            <View style={styles.notesContainer}>
              <Text style={styles.infoLabel}>ملاحظات:</Text>
              <Text style={styles.notesText}>{order.notes}</Text>
            </View>
          )}
        </View>
      </View>

      {/* أزرار الإجراءات */}
      <View style={styles.actionsContainer}>
        {order.status === 'pending' && (
          <>
            <TouchableOpacity
              style={[styles.actionButton, styles.acceptButton]}
              onPress={handleAcceptOrder}
              disabled={actionLoading}
            >
              {actionLoading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.actionButtonText}>✓ قبول الطلب</Text>
              )}
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.actionButton, styles.rejectButton]}
              onPress={handleRejectOrder}
              disabled={actionLoading}
            >
              <Text style={styles.actionButtonText}>✗ رفض الطلب</Text>
            </TouchableOpacity>
          </>
        )}

        {order.status === 'accepted' && (
          <TouchableOpacity
            style={[styles.actionButton, styles.updateButton]}
            onPress={() => handleUpdateStatus('picked_up')}
            disabled={actionLoading}
          >
            <Text style={styles.actionButtonText}>📦 تم الاستلام</Text>
          </TouchableOpacity>
        )}

        {order.status === 'picked_up' && (
          <TouchableOpacity
            style={[styles.actionButton, styles.updateButton]}
            onPress={() => handleUpdateStatus('in_transit')}
            disabled={actionLoading}
          >
            <Text style={styles.actionButtonText}>🚗 جاري التوصيل</Text>
          </TouchableOpacity>
        )}

        {order.status === 'in_transit' && (
          <TouchableOpacity
            style={[styles.actionButton, styles.deliveredButton]}
            onPress={() => handleUpdateStatus('delivered')}
            disabled={actionLoading}
          >
            <Text style={styles.actionButtonText}>✓ تم التوصيل</Text>
          </TouchableOpacity>
        )}
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
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    fontSize: 16,
    color: '#e74c3c',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  orderNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  orderDate: {
    fontSize: 14,
    color: '#7f8c8d',
    marginTop: 4,
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  section: {
    marginTop: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
    marginHorizontal: 16,
  },
  card: {
    backgroundColor: '#fff',
    padding: 16,
    marginHorizontal: 16,
    borderRadius: 8,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  infoLabel: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  infoValue: {
    fontSize: 14,
    color: '#2c3e50',
    fontWeight: '500',
  },
  phoneLink: {
    color: '#3498db',
    textDecorationLine: 'underline',
  },
  addressText: {
    fontSize: 16,
    color: '#2c3e50',
    marginBottom: 4,
  },
  cityText: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 12,
  },
  mapButton: {
    backgroundColor: '#ecf0f1',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  mapButtonText: {
    color: '#3498db',
    fontSize: 14,
    fontWeight: '500',
  },
  priceText: {
    color: '#27ae60',
    fontWeight: 'bold',
    fontSize: 16,
  },
  notesContainer: {
    marginTop: 8,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#ecf0f1',
  },
  notesText: {
    fontSize: 14,
    color: '#2c3e50',
    marginTop: 4,
    lineHeight: 20,
  },
  actionsContainer: {
    padding: 16,
    paddingBottom: 32,
  },
  actionButton: {
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 12,
  },
  acceptButton: {
    backgroundColor: '#27ae60',
  },
  rejectButton: {
    backgroundColor: '#e74c3c',
  },
  updateButton: {
    backgroundColor: '#3498db',
  },
  deliveredButton: {
    backgroundColor: '#27ae60',
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});


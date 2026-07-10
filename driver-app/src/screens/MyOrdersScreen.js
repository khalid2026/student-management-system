import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { orderService } from '../services/api';

export default function MyOrdersScreen({ navigation }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const data = await orderService.getMyOrders();
      setOrders(data);
    } catch (error) {
      console.error('Error loading my orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadOrders();
    setRefreshing(false);
  };

  const statusColors = {
    accepted: '#3498db',
    picked_up: '#9b59b6',
    in_transit: '#e67e22',
    delivered: '#27ae60',
  };

  const statusLabels = {
    accepted: 'مقبول',
    picked_up: 'تم الاستلام',
    in_transit: 'جاري التوصيل',
    delivered: 'تم التوصيل',
  };

  const statusIcons = {
    accepted: '✓',
    picked_up: '📦',
    in_transit: '🚗',
    delivered: '✅',
  };

  const renderOrderCard = ({ item }) => (
    <TouchableOpacity
      style={styles.orderCard}
      onPress={() => navigation.navigate('OrderDetails', { orderId: item._id })}
    >
      <View style={styles.orderHeader}>
        <View>
          <Text style={styles.orderId}>#{item.orderNumber}</Text>
          <Text style={styles.orderDate}>
            {new Date(item.createdAt).toLocaleDateString('ar-YE')}
          </Text>
        </View>
        <View
          style={[
            styles.statusBadge,
            { backgroundColor: statusColors[item.status] },
          ]}
        >
          <Text style={styles.statusText}>
            {statusIcons[item.status]} {statusLabels[item.status]}
          </Text>
        </View>
      </View>

      <View style={styles.divider} />

      <View style={styles.addressSection}>
        <View style={styles.addressRow}>
          <Text style={styles.addressIcon}>📍</Text>
          <View style={styles.addressContent}>
            <Text style={styles.addressLabel}>من:</Text>
            <Text style={styles.addressText} numberOfLines={1}>
              {item.pickupAddress?.address}
            </Text>
          </View>
        </View>

        <View style={styles.addressRow}>
          <Text style={styles.addressIcon}>🎯</Text>
          <View style={styles.addressContent}>
            <Text style={styles.addressLabel}>إلى:</Text>
            <Text style={styles.addressText} numberOfLines={1}>
              {item.deliveryAddress?.address}
            </Text>
          </View>
        </View>
      </View>

      <View style={styles.divider} />

      <View style={styles.orderFooter}>
        <View style={styles.infoItem}>
          <Text style={styles.infoIcon}>📏</Text>
          <Text style={styles.infoText}>{item.distance?.toFixed(1)} كم</Text>
        </View>
        <View style={styles.infoItem}>
          <Text style={styles.infoIcon}>💰</Text>
          <Text style={styles.priceText}>{item.deliveryFee} ريال</Text>
        </View>
        <View style={styles.infoItem}>
          <Text style={styles.infoIcon}>👤</Text>
          <Text style={styles.infoText}>{item.customer?.name}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>طلباتي الحالية</Text>
        <Text style={styles.headerSubtitle}>
          {orders.length} طلب نشط
        </Text>
      </View>

      {orders.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyIcon}>📦</Text>
          <Text style={styles.emptyText}>لا توجد طلبات نشطة</Text>
          <Text style={styles.emptySubtext}>
            اذهب إلى الطلبات المتاحة لقبول طلبات جديدة
          </Text>
        </View>
      ) : (
        <FlatList
          data={orders}
          renderItem={renderOrderCard}
          keyExtractor={(item) => item._id}
          contentContainerStyle={styles.listContainer}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
        />
      )}
    </View>
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
    padding: 20,
    paddingTop: 60,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#ecf0f1',
    textAlign: 'center',
    marginTop: 4,
  },
  listContainer: {
    padding: 16,
  },
  orderCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  orderHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  orderId: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  orderDate: {
    fontSize: 12,
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
  divider: {
    height: 1,
    backgroundColor: '#ecf0f1',
    marginVertical: 12,
  },
  addressSection: {
    marginBottom: 12,
  },
  addressRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  addressIcon: {
    fontSize: 20,
    marginRight: 8,
  },
  addressContent: {
    flex: 1,
  },
  addressLabel: {
    fontSize: 12,
    color: '#7f8c8d',
    marginBottom: 2,
  },
  addressText: {
    fontSize: 14,
    color: '#2c3e50',
  },
  orderFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  infoIcon: {
    fontSize: 16,
    marginRight: 4,
  },
  infoText: {
    fontSize: 14,
    color: '#2c3e50',
  },
  priceText: {
    fontSize: 14,
    color: '#27ae60',
    fontWeight: 'bold',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#7f8c8d',
    textAlign: 'center',
  },
});



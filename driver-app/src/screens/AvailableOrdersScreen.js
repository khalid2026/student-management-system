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

export default function AvailableOrdersScreen({ navigation }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const data = await orderService.getAvailableOrders();
      setOrders(data);
    } catch (error) {
      console.error('Error loading orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadOrders();
    setRefreshing(false);
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
        <View style={styles.priceContainer}>
          <Text style={styles.price}>{item.deliveryFee} ريال</Text>
          <Text style={styles.priceLabel}>رسوم التوصيل</Text>
        </View>
      </View>

      <View style={styles.locationContainer}>
        <View style={styles.locationRow}>
          <Text style={styles.locationIcon}>📍</Text>
          <View style={styles.locationInfo}>
            <Text style={styles.locationLabel}>من</Text>
            <Text style={styles.locationText}>{item.pickupAddress}</Text>
          </View>
        </View>

        <View style={styles.locationDivider} />

        <View style={styles.locationRow}>
          <Text style={styles.locationIcon}>🎯</Text>
          <View style={styles.locationInfo}>
            <Text style={styles.locationLabel}>إلى</Text>
            <Text style={styles.locationText}>{item.deliveryAddress}</Text>
          </View>
        </View>
      </View>

      <View style={styles.orderFooter}>
        <View style={styles.distanceContainer}>
          <Text style={styles.distanceIcon}>📏</Text>
          <Text style={styles.distanceText}>
            {item.distance ? `${item.distance} كم` : 'غير محدد'}
          </Text>
        </View>
        <TouchableOpacity style={styles.viewButton}>
          <Text style={styles.viewButtonText}>عرض التفاصيل</Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#3498db" />
        <Text style={styles.loadingText}>جاري تحميل الطلبات...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>الطلبات المتاحة</Text>
        <Text style={styles.headerSubtitle}>
          {orders.length} طلب متاح للتوصيل
        </Text>
      </View>

      {orders.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyIcon}>📦</Text>
          <Text style={styles.emptyText}>لا توجد طلبات متاحة حالياً</Text>
          <Text style={styles.emptySubtext}>
            سيتم إشعارك عند توفر طلبات جديدة
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
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#7f8c8d',
  },
  header: {
    backgroundColor: '#3498db',
    padding: 20,
    paddingTop: 50,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'right',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#fff',
    marginTop: 5,
    textAlign: 'right',
  },
  listContainer: {
    padding: 15,
  },
  orderCard: {
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  orderHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  orderId: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  orderDate: {
    fontSize: 12,
    color: '#7f8c8d',
    marginTop: 2,
  },
  priceContainer: {
    alignItems: 'flex-end',
  },
  price: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#27ae60',
  },
  priceLabel: {
    fontSize: 12,
    color: '#7f8c8d',
  },
  locationContainer: {
    marginBottom: 15,
  },
  locationRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  locationIcon: {
    fontSize: 20,
    marginRight: 10,
  },
  locationInfo: {
    flex: 1,
  },
  locationLabel: {
    fontSize: 12,
    color: '#7f8c8d',
    marginBottom: 2,
    textAlign: 'right',
  },
  locationText: {
    fontSize: 14,
    color: '#2c3e50',
    textAlign: 'right',
  },
  locationDivider: {
    height: 1,
    backgroundColor: '#ecf0f1',
    marginVertical: 10,
    marginLeft: 30,
  },
  orderFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  distanceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  distanceIcon: {
    fontSize: 16,
    marginRight: 5,
  },
  distanceText: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  viewButton: {
    backgroundColor: '#3498db',
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 8,
  },
  viewButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyIcon: {
    fontSize: 80,
    marginBottom: 20,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#7f8c8d',
    textAlign: 'center',
  },
});


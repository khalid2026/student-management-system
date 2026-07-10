import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TouchableOpacity, Alert } from 'react-native';
import { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🎉 مرحباً بك! 🎉</Text>
      <Text style={styles.subtitle}>تطبيق اختبار بسيط</Text>
      
      <View style={styles.counterContainer}>
        <Text style={styles.counterText}>العداد: {count}</Text>
      </View>

      <TouchableOpacity 
        style={styles.button}
        onPress={() => setCount(count + 1)}
      >
        <Text style={styles.buttonText}>اضغط هنا ➕</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={[styles.button, styles.resetButton]}
        onPress={() => setCount(0)}
      >
        <Text style={styles.buttonText}>إعادة تعيين 🔄</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={[styles.button, styles.alertButton]}
        onPress={() => Alert.alert('تنبيه', 'التطبيق يعمل بنجاح! ✅')}
      >
        <Text style={styles.buttonText}>اختبار Alert 🔔</Text>
      </TouchableOpacity>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  subtitle: {
    fontSize: 18,
    marginBottom: 40,
    color: '#666',
  },
  counterContainer: {
    backgroundColor: '#fff',
    padding: 30,
    borderRadius: 15,
    marginBottom: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  counterText: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#3498db',
  },
  button: {
    backgroundColor: '#3498db',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 10,
    marginVertical: 8,
    width: '80%',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  resetButton: {
    backgroundColor: '#e74c3c',
  },
  alertButton: {
    backgroundColor: '#2ecc71',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});


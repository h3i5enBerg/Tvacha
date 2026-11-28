import { Ionicons } from '@expo/vector-icons';
import { Tabs } from 'expo-router';

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#6E6E73',
        tabBarStyle: {
          backgroundColor: '#FFFFFF',
          borderTopColor: '#E5E5EA',
          borderTopWidth: 1,
        },
        headerStyle: { backgroundColor: '#F2F2F7' },
        headerTitleStyle: { color: '#1C1C1E', fontWeight: '600' },
        headerShadowVisible: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Tvacha',
          tabBarLabel: 'Home',
          tabBarIcon: ({ focused, size }) => (
            <Ionicons
              name="medkit-outline"
              size={size}
              color={focused ? '#007AFF' : '#6E6E73'}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="history"
        options={{
          title: 'Scan History',
          tabBarLabel: 'History',
          tabBarIcon: ({ focused, size }) => (
            <Ionicons
              name="time-outline"
              size={size}
              color={focused ? '#007AFF' : '#6E6E73'}
            />
          ),
        }}
      />
    </Tabs>
  );
}

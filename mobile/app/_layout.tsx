import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <StatusBar style="dark" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: '#F2F2F7' },
          headerTintColor: '#007AFF',
          headerTitleStyle: { color: '#1C1C1E', fontWeight: '600' },
          headerShadowVisible: false,
          contentStyle: { backgroundColor: '#F2F2F7' },
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen
          name="scan/camera"
          options={{ title: 'Capture Lesion', presentation: 'modal' }}
        />
        <Stack.Screen
          name="scan/symptoms"
          options={{ title: 'Symptom Check' }}
        />
        <Stack.Screen
          name="scan/[id]"
          options={{ title: 'Screening Summary' }}
        />
      </Stack>
    </SafeAreaProvider>
  );
}

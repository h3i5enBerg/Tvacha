import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Preliminary Skin Screening</Text>
        <Text style={styles.subtitle}>
          Capture a clear photo of the skin area and answer brief symptom
          questions for preliminary AYUSH-aligned triage guidance.
        </Text>
        <Pressable
          style={styles.primaryButton}
          onPress={() => router.push('/scan/camera')}
        >
          <Ionicons name="camera-outline" size={20} color="#FFFFFF" />
          <Text style={styles.primaryButtonText}>Start New Scan</Text>
        </Pressable>
      </View>

      <Text style={styles.disclaimer}>
        For preliminary screening only. Not a substitute for professional
        medical diagnosis.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F7',
    padding: 16,
    gap: 16,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#E5E5EA',
    padding: 16,
    gap: 12,
  },
  title: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1C1C1E',
  },
  subtitle: {
    fontSize: 15,
    lineHeight: 21,
    color: '#6E6E73',
  },
  primaryButton: {
    marginTop: 4,
    backgroundColor: '#007AFF',
    borderRadius: 12,
    minHeight: 48,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  primaryButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  disclaimer: {
    fontSize: 12,
    lineHeight: 17,
    color: '#6E6E73',
    paddingHorizontal: 4,
  },
});

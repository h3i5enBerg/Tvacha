import { useRouter } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';

export default function CameraScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Guided Lesion Capture</Text>
        <Text style={styles.subtitle}>
          Camera preview and circular lesion framing guide will be wired here.
        </Text>
        <Pressable
          style={styles.button}
          onPress={() => router.push('/scan/symptoms')}
        >
          <Text style={styles.buttonText}>Continue to Symptoms</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F7',
    padding: 16,
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
    fontSize: 18,
    fontWeight: '600',
    color: '#1C1C1E',
  },
  subtitle: {
    fontSize: 15,
    lineHeight: 21,
    color: '#6E6E73',
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    minHeight: 48,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});

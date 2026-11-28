import { useRouter } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';

export default function SymptomsScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Symptom Questionnaire</Text>
        <Text style={styles.subtitle}>
          Body location, duration, itching, pain, bleeding, and fever inputs
          will be collected here.
        </Text>
        <Pressable
          style={styles.button}
          onPress={() => router.push('/scan/preview-1')}
        >
          <Text style={styles.buttonText}>View Sample Result</Text>
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

export type TriageUrgency = 'low' | 'moderate' | 'high';

export const THEME_COLORS = {
  canvas: '#F2F2F7',
  surface: '#FFFFFF',
  border: '#E5E5EA',
  inkPrimary: '#1C1C1E',
  inkSecondary: '#6E6E73',
  accent: '#007AFF',
  offlineBadge: {
    background: '#EFEFF4',
    text: '#6E6E73',
  },
  triage: {
    low: {
      background: '#EAF7EE',
      text: '#1E7E34',
      label: 'Low Priority',
    },
    moderate: {
      background: '#FFF6E5',
      text: '#9A6700',
      label: 'Monitor Closely',
    },
    high: {
      background: '#FDECEC',
      text: '#C62828',
      label: 'Clinical Review',
    },
  },
} as const;

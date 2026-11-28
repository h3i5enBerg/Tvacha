import { Ionicons } from '@expo/vector-icons';
import { Text, View } from 'react-native';

import { THEME_COLORS, type TriageUrgency } from '../../constants/theme';

interface TriageBadgeProps {
  level: TriageUrgency;
}

const TRIAGE_ICONS: Record<TriageUrgency, keyof typeof Ionicons.glyphMap> = {
  low: 'checkmark-circle-outline',
  moderate: 'alert-circle-outline',
  high: 'warning-outline',
};

export function TriageBadge({ level }: TriageBadgeProps) {
  const palette = THEME_COLORS.triage[level];

  return (
    <View
      className="self-start flex-row items-center gap-1.5 rounded-full px-3 py-1"
      style={{ backgroundColor: palette.background }}
    >
      <Ionicons name={TRIAGE_ICONS[level]} size={14} color={palette.text} />
      <Text
        className="text-xs font-semibold tracking-tight"
        style={{ color: palette.text }}
      >
        {palette.label}
      </Text>
    </View>
  );
}

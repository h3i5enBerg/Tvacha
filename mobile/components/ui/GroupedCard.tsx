import type { ReactNode } from 'react';
import { View, type ViewProps } from 'react-native';

interface GroupedCardProps extends ViewProps {
  children: ReactNode;
  className?: string;
}

export function GroupedCard({
  children,
  className = '',
  style,
  ...props
}: GroupedCardProps) {
  return (
    <View
      className={`bg-surface rounded-2xl border border-border p-4 ${className}`.trim()}
      style={style}
      {...props}
    >
      {children}
    </View>
  );
}

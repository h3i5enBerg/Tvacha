---
name: apple-design
description: Strict Apple Human Interface Guidelines (Apple Health aesthetic) for the Ministry of AYUSH preliminary dermatological screening mobile application. Apply whenever designing, building, or reviewing React Native / NativeWind UI components and screens.
---

# Apple Health / iOS HIG Design Skill

This skill enforces a calm, clinical, native iOS aesthetic modeled on **Apple Health** for the Ministry of AYUSH preliminary dermatological screening app (`mobile/`).

## 1. Color System (iOS System Palette)

| Token | Hex | Usage |
| :--- | :--- | :--- |
| **Grouped Canvas** | `#F2F2F7` | Primary screen background (`systemGroupedBackground`) |
| **Card Surface** | `#FFFFFF` | Elevated grouped content cards (`secondarySystemGroupedBackground`) |
| **Hairline Border** | `#E5E5EA` | `1px` crisp card & list separators (preferred over drop shadows) |
| **Primary Text** | `#1C1C1E` | Headings, primary labels, numeric readouts |
| **Secondary Text** | `#6E6E73` | Captions, metadata, timestamps, medical disclaimers |
| **System Blue Accent** | `#007AFF` | Primary CTAs, active tab icons, interactive links |

### Muted Semantic Triage Badges
Use low-saturation tinted backgrounds with crisp, accessible foreground text—never neon or saturated blocks:
- **Routine / Low Urgency:** Muted green tint (e.g., `#EAF7EE` background, `#1E7E34` text)
- **Moderate / Monitor:** Muted amber tint (e.g., `#FFF6E5` background, `#9A6700` text)
- **Urgent / Red-Flag Triage:** Muted red tint (e.g., `#FDECEC` background, `#C62828` text)
- **Offline / Pending Sync:** Muted neutral/slate tint (e.g., `#EFEFF4` background, `#6E6E73` text)

## 2. Layout, Surfaces & Typography
- **Grouped Inset Cards:** Use generous horizontal margins (`16px`), clean internal padding (`16px`), `12px–16px` corner radius, and `1px` `#E5E5EA` hairline borders.
- **Typography Hierarchy:** Follow iOS SF-style proportions—large bold screen titles, semibold section headers, `15px–17px` body copy, and `12px–13px` secondary metadata.
- **Tabular Numerals:** Always apply `fontVariant: ['tabular-nums']` (or NativeWind `tabular-nums`) for confidence percentages, timestamps, and clinical metrics so numbers align cleanly without jitter.
- **Safe Areas & Touch Targets:** Respect iOS safe-area insets and ensure interactive targets are at least `44x44pt`.

## 3. Strict Anti-AI-Slop Bans
Do **not** use any of the following:
- **No purple/blue gradients** or multi-stop decorative background gradients.
- **No glassmorphism** (frosted blur cards over busy backgrounds).
- **No glowing borders**, neon accents, or cyberpunk/futuristic flourishes.
- **No heavy drop shadows**—rely on `#F2F2F7` vs. `#FFFFFF` contrast and `1px` `#E5E5EA` borders.
- **No emojis** in headings, buttons, badges, or navigation labels. Use clean, monochrome `@expo/vector-icons` (e.g., `Ionicons` or `Feather`) sized consistently.

## 4. Clinical UX Principles
- **Clarity over decoration:** Preliminary screening results must present Top-3 differential conditions with tabular confidence bars, symptom-adjusted urgency, and AYUSH + general care guidance in scannable grouped cards.
- **Explicit Disclaimer:** Every screening result and report must include a calm, readable `#6E6E73` disclaimer stating it is for preliminary screening only and not a medical diagnosis.
- **Offline Transparency:** Clearly indicate `pending_sync` status on locally saved scans so rural/low-connectivity users know their data is safely stored on-device.

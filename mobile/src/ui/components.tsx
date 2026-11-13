import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import React from 'react';
import { ActivityIndicator, Image, Pressable, StyleSheet, Text, View, type StyleProp, type ViewStyle } from 'react-native';
import { theme, type GradientKey } from '../theme';
import type { RequestStatus, SyncState } from '../types';

export type IconName = React.ComponentProps<typeof Ionicons>['name'];

/**
 * The Couchbase Cruises lockup: the Couchbase logo (mark and wordmark, as it
 * appears in the couchbase.com header) followed by "Cruises". The logo is
 * `assets/images/couchbase-logo-white.png` on dark surfaces and
 * `couchbase-logo-black.png` on light ones - both rendered from the SVG in
 * `assets/brand/`. `brand-logo.png` is the round mark on its own.
 */
const LOGO_ON_DARK = require('../../assets/images/couchbase-logo-white.png');
const LOGO_ON_LIGHT = require('../../assets/images/couchbase-logo-black.png');
const LOGO_ASPECT = 1440 / 271;

export function Wordmark({ light = true, size = 15 }: { light?: boolean; size?: number }) {
  const c = light ? theme.color.onDark : theme.color.text;
  const h = size * 1.75;
  return (
    <View style={{ flexDirection: 'row', alignItems: 'center', gap: size * 0.5 }} accessibilityRole="header" accessibilityLabel="Couchbase Cruises">
      <Image source={light ? LOGO_ON_DARK : LOGO_ON_LIGHT} style={{ width: h * LOGO_ASPECT, height: h }} resizeMode="contain" accessibilityLabel="Couchbase" />
      <Text style={{ color: c, fontSize: size * 1.52, lineHeight: h, fontWeight: '400', fontFamily: theme.font.display, letterSpacing: -0.2, opacity: 0.92 }}>Cruises</Text>
    </View>
  );
}

export function Card({ children, style }: { children: React.ReactNode; style?: StyleProp<ViewStyle> }) {
  return <View style={[styles.card, style]}>{children}</View>;
}

export function GradientArt({ palette, icon, height = 96, children }: { palette: string; icon: IconName; height?: number; children?: React.ReactNode }) {
  const colors = (theme.gradient as Record<string, readonly [string, string]>)[palette] ?? theme.gradient.hero;
  return (
    <LinearGradient colors={colors as unknown as [string, string]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ height, borderTopLeftRadius: theme.radius, borderTopRightRadius: theme.radius, padding: 14, justifyContent: 'space-between' }}>
      <View style={styles.waves} pointerEvents="none">
        <Ionicons name={icon} size={height * 0.95} color="rgba(255,255,255,0.13)" />
      </View>
      {children}
    </LinearGradient>
  );
}

export function Pill({ label, tone = 'neutral', icon }: { label: string; tone?: 'neutral' | 'club' | 'accent' | 'ok' | 'warn' | 'danger' | 'info' | 'dark'; icon?: IconName }) {
  const map = {
    neutral: [theme.color.bg, theme.color.muted],
    club: [theme.color.clubSoft, theme.color.club],
    accent: [theme.color.accentSoft, theme.color.brandDark],
    ok: [theme.color.okSoft, theme.color.ok],
    warn: [theme.color.warnSoft, theme.color.warn],
    danger: [theme.color.dangerSoft, theme.color.danger],
    info: [theme.color.infoSoft, theme.color.info],
    dark: ['rgba(255,255,255,0.16)', theme.color.onDark],
  } as const;
  const [bg, fg] = map[tone];
  return (
    <View style={[styles.pill, { backgroundColor: bg }]}>
      {icon ? <Ionicons name={icon} size={11} color={fg} /> : null}
      <Text style={{ color: fg, fontSize: theme.type.xs, fontWeight: '700' }}>{label}</Text>
    </View>
  );
}

export function Button({ label, onPress, kind = 'primary', icon, disabled, busy, small }: {
  label: string; onPress: () => void; kind?: 'primary' | 'dark' | 'ghost' | 'light'; icon?: IconName; disabled?: boolean; busy?: boolean; small?: boolean;
}) {
  // couchbase.com's call to action: Couchbase red, white label, softly rounded corners.
  const bg = { primary: theme.color.accent, dark: theme.color.dark, ghost: 'transparent', light: theme.color.surface }[kind];
  const fg = { primary: theme.color.onAccent, dark: theme.color.onDark, ghost: theme.color.text, light: theme.color.text }[kind];
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled || busy}
      style={({ pressed }) => [
        styles.btn,
        small && styles.btnSmall,
        { backgroundColor: bg, opacity: disabled ? 0.45 : pressed ? 0.85 : 1 },
        kind === 'ghost' && { borderWidth: 1, borderColor: theme.color.border },
      ]}
    >
      {busy ? <ActivityIndicator color={fg} /> : icon ? <Ionicons name={icon} size={small ? 14 : 17} color={fg} /> : null}
      <Text style={{ color: fg, fontWeight: '600', fontFamily: theme.font.display, fontSize: small ? theme.type.sm : theme.type.md }}>{label}</Text>
    </Pressable>
  );
}

export function SectionTitle({ title, action }: { title: string; action?: React.ReactNode }) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionText}>{title.toUpperCase()}</Text>
      {action}
    </View>
  );
}

const SYNC_LABEL: Record<SyncState['status'], [string, 'ok' | 'warn' | 'danger' | 'neutral' | 'info']> = {
  connecting: ['Connecting', 'info'],
  connected: ['Synced', 'ok'],
  idle: ['Synced', 'ok'],
  busy: ['Syncing', 'info'],
  offline: ['Offline', 'warn'],
  paused: ['Offline mode', 'warn'],
  error: ['Sync error', 'danger'],
  stopped: ['Local only', 'neutral'],
};

export function SyncBadge({ sync, dark }: { sync: SyncState; dark?: boolean }) {
  const [label, tone] = SYNC_LABEL[sync.status];
  const text = sync.pendingPush ? `${label} · ${sync.pendingPush} to send` : label;
  const dot = { ok: '#3DDC84', warn: theme.color.highlight, danger: '#FF6B6B', neutral: theme.color.faint, info: theme.color.clubSoft }[tone];
  return (
    <View style={[styles.sync, dark ? { backgroundColor: 'rgba(255,255,255,0.12)' } : { backgroundColor: theme.color.bg }]}>
      <View style={[styles.dot, { backgroundColor: dot }]} />
      <Text style={{ color: dark ? theme.color.onDark : theme.color.text, fontSize: theme.type.xs, fontWeight: '700' }}>
        {sync.engine === 'couchbase-lite' ? 'Couchbase Lite · ' : 'Preview · '}
        {text}
      </Text>
    </View>
  );
}

export const STATUS_UI: Record<RequestStatus, { label: string; tone: 'neutral' | 'club' | 'accent' | 'ok' | 'warn' | 'danger' | 'info'; icon: IconName }> = {
  pending: { label: 'Waiting to sync', tone: 'warn', icon: 'cloud-upload-outline' },
  processing: { label: 'Processing', tone: 'info', icon: 'sync' },
  awaiting_approval: { label: 'Awaiting supervisor', tone: 'warn', icon: 'shield-checkmark-outline' },
  confirmed: { label: 'Confirmed', tone: 'ok', icon: 'checkmark-circle' },
  accepted: { label: 'Accepted', tone: 'ok', icon: 'checkmark-circle' },
  submitted: { label: 'Bid submitted', tone: 'info', icon: 'time-outline' },
  failed: { label: 'Not completed', tone: 'danger', icon: 'alert-circle' },
};

export function Empty({ icon, title, body }: { icon: IconName; title: string; body: string }) {
  return (
    <View style={{ alignItems: 'center', padding: theme.space.xl, gap: 6 }}>
      <Ionicons name={icon} size={34} color={theme.color.faint} />
      <Text style={{ fontWeight: '800', color: theme.color.text, fontSize: theme.type.md }}>{title}</Text>
      <Text style={{ color: theme.color.muted, textAlign: 'center' }}>{body}</Text>
    </View>
  );
}

export const money = (n: number | undefined | null) =>
  n == null ? '' : `$${Number(n).toLocaleString('en-US', { maximumFractionDigits: n % 1 ? 2 : 0 })}`;

export function fmtDate(iso: string, opts: Intl.DateTimeFormatOptions = { weekday: 'short', month: 'short', day: 'numeric' }) {
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number);
  return new Date(y, m - 1, d).toLocaleDateString('en-US', opts);
}

const styles = StyleSheet.create({
  card: { backgroundColor: theme.color.surface, borderRadius: theme.radius, ...theme.shadow.card },
  waves: { position: 'absolute', right: -6, bottom: -14 },
  pill: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: 8, paddingVertical: 3, borderRadius: 999, alignSelf: 'flex-start' },
  btn: { flexDirection: 'row', gap: 8, alignItems: 'center', justifyContent: 'center', paddingVertical: 14, paddingHorizontal: 18, borderRadius: theme.radiusBtn },
  btnSmall: { paddingVertical: 8, paddingHorizontal: 14, borderRadius: theme.radiusSm },
  section: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: theme.space.xl, marginBottom: theme.space.sm },
  sectionText: { color: theme.color.muted, fontSize: theme.type.xs, fontWeight: '800', letterSpacing: 1.4 },
  sync: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 10, paddingVertical: 5, borderRadius: 999, alignSelf: 'flex-start' },
  dot: { width: 7, height: 7, borderRadius: 4 },
});

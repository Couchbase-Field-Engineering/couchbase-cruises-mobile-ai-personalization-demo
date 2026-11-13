import { Platform, type ViewStyle } from 'react-native';

/**
 * Styled after couchbase.com (Nov 2026). The site's palette, taken from its
 * stylesheet: black hero sections with white type, Couchbase red (#EC1218)
 * for every call to action (white label, 12-15px corner radius), dark red
 * (#7C0206 / #560003) for depth, orange (#FC9D0C) as the warm highlight,
 * peach (#FFF0DA) and cream (#EAD8BE) panels, white-smoke (#F7F7F7) page
 * background and light-grey (#D2D5D9) rules. Headlines on the site are
 * Centra No2 Medium and body copy is Inter; Centra is a licensed face, so it
 * is named first and the platform sans stands in when it isn't installed.
 */
const shadowCard: ViewStyle = Platform.select({
  ios: { shadowColor: '#000000', shadowOpacity: 0.1, shadowRadius: 16, shadowOffset: { width: 0, height: 7 } },
  android: { elevation: 3 },
  default: { boxShadow: '0 7px 20px rgba(0,0,0,0.10)' } as ViewStyle,
}) as ViewStyle;

export const theme = {
  color: {
    dark: '#000000',          // hero and dark surfaces
    brand: '#EC1218',         // Couchbase red: links, icons, selected states
    brandDark: '#B30005',     // pressed / active red
    accent: '#EC1218',        // primary call to action (white label)
    accentSoft: '#FFD5D6',
    onAccent: '#FFFFFF',
    darkRed: '#7C0206',
    darkestRed: '#560003',
    highlight: '#FC9D0C',     // orange: warm emphasis
    highlightText: '#A35600', // orange, darkened for text on white
    club: '#560003',          // Crimson Club loyalty pills
    clubSoft: '#FBCE90',      // dark peach
    info: '#333333',          // neutral informational pills
    infoSoft: '#FFF0DA',      // peach panels
    cream: '#EAD8BE',
    sand: '#9B9382',
    bg: '#F7F7F7',            // white smoke
    surface: '#FFFFFF',
    text: '#000000',
    muted: '#5A5A5A',
    faint: '#858585',
    border: '#D2D5D9',
    ok: '#13804B',
    okSoft: '#E6F6EE',
    warn: '#A35600',
    warnSoft: '#FFF0DA',
    danger: '#B30005',
    dangerSoft: '#FFD5D6',
    onDark: '#FFFFFF',
    onDarkMuted: 'rgba(255,255,255,0.74)',
  },
  // Offer artwork and hero backgrounds, all drawn from the site palette. The
  // keys are the `palette` values the backend puts on each offer.
  gradient: {
    hero: ['#000000', '#560003'] as const,
    suite: ['#560003', '#EC1218'] as const,
    ocean: ['#EC1218', '#FC9D0C'] as const,
    dining: ['#000000', '#7C0206'] as const,
    drinks: ['#B30005', '#FC9D0C'] as const,
    spa: ['#333333', '#9B9382'] as const,
    deck: ['#000000', '#333333'] as const,
  },
  font: {
    display: Platform.select({ ios: 'Avenir Next', android: 'sans-serif-medium', default: "'Centra No2', Inter, 'Avenir Next', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif" }) as string,
  },
  space: { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, xxl: 32 },
  type: { xs: 11, sm: 13, md: 15, lg: 17, xl: 20, title: 26, hero: 34 },
  radius: 24,
  radiusSm: 12,
  radiusBtn: 14,
  shadow: { card: shadowCard },
} as const;

export type GradientKey = keyof typeof theme.gradient;

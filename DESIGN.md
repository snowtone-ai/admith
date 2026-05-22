---
version: alpha
name: Admith-design-system
description: |
  Admith's visual identity rests on a deep blue-black canvas (#06060B) that
  evokes a pre-dawn void — the moment before a new market materialises.
  A single chromatic accent, Aurora Violet (#7C3AED), marks moments of value
  creation: successful negotiations, agent consensus, and the signature
  negative-to-positive conversion. Four semantic colors — Emerald (gain),
  Rose (loss), Amber (urgency), and Cyan (live data) — carry all operational
  meaning. Display type is set in Manrope (600–800) with aggressive negative
  tracking to project authority. Inter handles body and UI text for maximum
  data-density readability. JetBrains Mono powers prices, agent IDs, and
  protocol identifiers. Japanese text falls to Noto Sans JP at matching
  optical weights. Surfaces follow a strict 5-step elevation ladder using
  translucent blue-black tints, separated by hairline borders at 6–12%
  white opacity. Depth comes from atmospheric glow — soft radial gradients
  behind active elements — never from drop shadows. Cards use 12px radius
  universally. The system is dark-first; a light mode exists as an inverse
  mapping but is never the default. The signature motion is the Value
  Conversion Animation: a Rose-to-Emerald color transition with an Aurora
  Violet flash at the inflection point, used whenever negative value
  converts to positive.

colors:
  # ── Canvas & Surfaces ──────────────────────────────────
  canvas:             "#06060B"
  surface-1:          "#0C0D14"
  surface-2:          "#12131D"
  surface-3:          "#1A1B28"
  surface-4:          "#222336"
  overlay:            "rgba(6, 6, 11, 0.80)"

  # ── Ink (Text) ─────────────────────────────────────────
  ink:                "#F0F1F5"
  ink-muted:          "#A0A4B8"
  ink-subtle:         "#6B6F82"
  ink-ghost:          "#3D4055"

  # ── Hairlines & Borders ────────────────────────────────
  hairline:           "rgba(255, 255, 255, 0.06)"
  hairline-strong:    "rgba(255, 255, 255, 0.12)"
  hairline-focus:     "rgba(255, 255, 255, 0.20)"

  # ── Brand Accent — Aurora Violet ───────────────────────
  accent:             "#7C3AED"
  accent-hover:       "#8B5CF6"
  accent-pressed:     "#6D28D9"
  accent-glow:        "rgba(124, 58, 237, 0.20)"
  on-accent:          "#FFFFFF"

  # ── Semantic — Positive (Gain / Conversion) ────────────
  positive:           "#10B981"
  positive-subtle:    "rgba(16, 185, 129, 0.12)"
  positive-glow:      "rgba(16, 185, 129, 0.20)"
  on-positive:        "#FFFFFF"

  # ── Semantic — Negative (Loss / Waste / Cost) ──────────
  negative:           "#F43F5E"
  negative-subtle:    "rgba(244, 63, 94, 0.12)"
  negative-glow:      "rgba(244, 63, 94, 0.20)"
  on-negative:        "#FFFFFF"

  # ── Semantic — Warning (Deadline / Expiry / Urgency) ───
  warning:            "#F59E0B"
  warning-subtle:     "rgba(245, 158, 11, 0.12)"
  warning-glow:       "rgba(245, 158, 11, 0.20)"
  on-warning:         "#0C0D14"

  # ── Semantic — Info (Live Data / Real-time) ────────────
  info:               "#06B6D4"
  info-subtle:        "rgba(6, 182, 212, 0.12)"
  info-glow:          "rgba(6, 182, 212, 0.20)"
  on-info:            "#FFFFFF"

  # ── Inverse (Light Mode) ──────────────────────────────
  inverse-canvas:     "#FAFBFE"
  inverse-surface-1:  "#F0F1F5"
  inverse-surface-2:  "#E4E5EC"
  inverse-ink:        "#0C0D14"
  inverse-ink-muted:  "#4A4D5E"
  inverse-hairline:   "rgba(0, 0, 0, 0.08)"

typography:
  # ── Display ────────────────────────────────────────────
  display-hero:
    fontFamily: "'Manrope', 'Noto Sans JP', sans-serif"
    fontSize: 72px
    fontWeight: 800
    lineHeight: 1.0
    letterSpacing: -3.0px
  display-xl:
    fontFamily: "'Manrope', 'Noto Sans JP', sans-serif"
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -2.0px
  display-lg:
    fontFamily: "'Manrope', 'Noto Sans JP', sans-serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.10
    letterSpacing: -1.2px
  display-md:
    fontFamily: "'Manrope', 'Noto Sans JP', sans-serif"
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.8px

  # ── Headings ───────────────────────────────────────────
  heading-lg:
    fontFamily: "'Manrope', 'Noto Sans JP', sans-serif"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: -0.4px
  heading-md:
    fontFamily: "'Manrope', 'Noto Sans JP', sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.30
    letterSpacing: -0.3px
  heading-sm:
    fontFamily: "'Manrope', 'Noto Sans JP', sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.35
    letterSpacing: -0.1px

  # ── Body ───────────────────────────────────────────────
  body-lg:
    fontFamily: "'Inter', 'Noto Sans JP', sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: -0.1px
  body:
    fontFamily: "'Inter', 'Noto Sans JP', sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  body-sm:
    fontFamily: "'Inter', 'Noto Sans JP', sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0

  # ── UI ─────────────────────────────────────────────────
  label:
    fontFamily: "'Inter', 'Noto Sans JP', sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: 0.02em
  caption:
    fontFamily: "'Inter', 'Noto Sans JP', sans-serif"
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.40
    letterSpacing: 0.02em
  button:
    fontFamily: "'Inter', 'Noto Sans JP', sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: 0
  eyebrow:
    fontFamily: "'JetBrains Mono', 'Noto Sans JP', monospace"
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.30
    letterSpacing: 0.08em
    textTransform: uppercase

  # ── Data & Code ────────────────────────────────────────
  mono:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.50
    letterSpacing: 0
  mono-sm:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.40
    letterSpacing: 0
  price:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: -0.02em
    fontFeature: "tnum, lnum"
  price-lg:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.10
    letterSpacing: -0.03em
    fontFeature: "tnum, lnum"

rounded:
  none: 0
  xs:   2px
  sm:   4px
  md:   8px
  lg:   12px
  xl:   16px
  xxl:  24px
  pill:  9999px

spacing:
  xxs:     2px
  xs:      4px
  sm:      8px
  md:      12px
  base:    16px
  lg:      24px
  xl:      32px
  xxl:     48px
  section: 80px
  hero:    120px

components:
  # ── Buttons ────────────────────────────────────────────
  button-accent:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 10px 20px
    height: 40px
  button-accent-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
  button-accent-pressed:
    backgroundColor: "{colors.accent-pressed}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
  button-surface:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 10px 20px
    height: 40px
  button-surface-hover:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
  button-ghost:
    backgroundColor: transparent
    textColor: "{colors.ink-muted}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 10px 16px
    height: 40px
  button-ghost-hover:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
  button-danger:
    backgroundColor: "{colors.negative}"
    textColor: "{colors.on-negative}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 10px 20px
    height: 40px

  # ── Cards ──────────────────────────────────────────────
  card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: 24px
  card-hover:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
  card-elevated:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: 24px
  card-interactive:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: 20px

  # ── Admith-Specific: Resource Card ─────────────────────
  resource-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: 20px
  resource-card-negative:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.negative}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: 20px
  resource-card-positive:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.positive}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: 20px

  # ── Admith-Specific: Stat Card ─────────────────────────
  stat-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.price-lg}"
    rounded: "{rounded.lg}"
    padding: 24px
  stat-card-positive:
    backgroundColor: "{colors.positive-subtle}"
    textColor: "{colors.positive}"
    typography: "{typography.price-lg}"
    rounded: "{rounded.lg}"
    padding: 24px
  stat-card-negative:
    backgroundColor: "{colors.negative-subtle}"
    textColor: "{colors.negative}"
    typography: "{typography.price-lg}"
    rounded: "{rounded.lg}"
    padding: 24px

  # ── Admith-Specific: Agent Badge ───────────────────────
  agent-badge:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.mono-sm}"
    rounded: "{rounded.pill}"
    padding: 4px 10px
  agent-badge-active:
    backgroundColor: "{colors.accent-glow}"
    textColor: "{colors.accent}"
    typography: "{typography.mono-sm}"
    rounded: "{rounded.pill}"
    padding: 4px 10px
  agent-badge-negotiating:
    backgroundColor: "{colors.warning-subtle}"
    textColor: "{colors.warning}"
    typography: "{typography.mono-sm}"
    rounded: "{rounded.pill}"
    padding: 4px 10px

  # ── Admith-Specific: Value Indicator ───────────────────
  value-negative:
    backgroundColor: transparent
    textColor: "{colors.negative}"
    typography: "{typography.price}"
  value-positive:
    backgroundColor: transparent
    textColor: "{colors.positive}"
    typography: "{typography.price}"
  value-neutral:
    backgroundColor: transparent
    textColor: "{colors.ink-muted}"
    typography: "{typography.price}"

  # ── Admith-Specific: Negotiation Timeline ──────────────
  negotiation-step:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 12px 16px
  negotiation-step-active:
    backgroundColor: "{colors.accent-glow}"
    textColor: "{colors.accent}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 12px 16px
  negotiation-step-completed:
    backgroundColor: "{colors.positive-subtle}"
    textColor: "{colors.positive}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 12px 16px

  # ── Inputs & Forms ─────────────────────────────────────
  text-input:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: 10px 14px
    height: 40px
  text-input-focused:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
  select:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: 10px 14px
    height: 40px

  # ── Navigation ─────────────────────────────────────────
  top-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    height: 56px
  sidebar:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.label}"
    width: 240px
  sidebar-item:
    backgroundColor: transparent
    textColor: "{colors.ink-muted}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 8px 12px
  sidebar-item-active:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 8px 12px

  # ── Status Badge ───────────────────────────────────────
  badge-default:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: 2px 8px
  badge-positive:
    backgroundColor: "{colors.positive-subtle}"
    textColor: "{colors.positive}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: 2px 8px
  badge-negative:
    backgroundColor: "{colors.negative-subtle}"
    textColor: "{colors.negative}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: 2px 8px
  badge-warning:
    backgroundColor: "{colors.warning-subtle}"
    textColor: "{colors.warning}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: 2px 8px
  badge-info:
    backgroundColor: "{colors.info-subtle}"
    textColor: "{colors.info}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: 2px 8px

  # ── Tooltip & Popover ──────────────────────────────────
  tooltip:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink}"
    typography: "{typography.caption}"
    rounded: "{rounded.md}"
    padding: 8px 12px

  # ── Table ──────────────────────────────────────────────
  table-header:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink-subtle}"
    typography: "{typography.eyebrow}"
    padding: 12px 16px
  table-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    padding: 12px 16px
  table-row-hover:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    padding: 12px 16px

  # ── Modal / Dialog ─────────────────────────────────────
  modal:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.xl}"
    padding: 32px

  # ── Footer ─────────────────────────────────────────────
  footer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink-subtle}"
    typography: "{typography.body-sm}"
    padding: 48px 24px
---

# Admith Design System

> **"The Invisible Hand, Made Visible"**
> AIエージェントが見えない場所で取引を完結させる。UIはその結果と状態だけを静かに示す。

## Design Philosophy

Admithは、人間の認知速度ではアクセスできなかったリソースにAIエージェントが到達し、新市場を創出するプラットフォームである。デザインは以下の3原則に従う。

1. **Data as Protagonist** — データと数値がUIの主役。装飾ではなく、情報が視覚的ヒエラルキーの頂点に位置する。
2. **Conversion as Celebration** — 負の価値が正に転換する瞬間は、Admith体験の頂点であり、Auroraアニメーションで視覚的に祝福する。
3. **Atmospheric Depth** — 深みはドロップシャドウではなく、グローと半透明レイヤーで表現する。画面は「深淵の中で光る市場」を想起させる。

## Visual Theme

Admithの世界観は「夜明け前の市場」。真っ暗な空間に、取引が成立する瞬間だけ光が灯る。

- **Canvas**: 純粋な黒ではなく、わずかに青みを帯びた深黒 (#06060B) を使用。長時間のダッシュボード操作時の目の疲労を軽減し、純黒との微細なコントラストで奥行きを生む。
- **Accent**: Aurora Violet (#7C3AED) はブランドマーク、主要CTA、フォーカスリング、そして価値転換のフラッシュにのみ使用。デコレーション用途は禁止。
- **Semantic colors**: 操作的意味を持つ色は4色のみ。Emerald（利益・転換）、Rose（損失・廃棄）、Amber（期限・緊急）、Cyan（リアルタイム・データフロー）。

## Color Palette

### Surface Elevation Ladder

5段階のサーフェスで視覚ヒエラルキーを構築する。スキップは禁止。

| Level | Token | Hex | Usage |
|---|---|---|---|
| 0 — Canvas | `{colors.canvas}` | #06060B | ページ背景 |
| 1 — Recessed | `{colors.surface-1}` | #0C0D14 | カード、サイドバー、テーブル背景 |
| 2 — Raised | `{colors.surface-2}` | #12131D | ホバー状態、モーダル、アクティブカード |
| 3 — Elevated | `{colors.surface-3}` | #1A1B28 | ツールチップ、ドロップダウン |
| 4 — Floating | `{colors.surface-4}` | #222336 | ポップオーバー、コマンドパレット |

### Glow System

アクティブな要素にはboxShadowでグローを適用する。background-colorでは表現しない。

```css
/* アクセントグロー — 価値転換・CTA */
box-shadow: 0 0 20px {colors.accent-glow}, 0 0 60px rgba(124, 58, 237, 0.08);

/* ポジティブグロー — 利益確定 */
box-shadow: 0 0 20px {colors.positive-glow}, 0 0 60px rgba(16, 185, 129, 0.08);

/* ネガティブグロー — 損失・廃棄 */
box-shadow: 0 0 20px {colors.negative-glow}, 0 0 60px rgba(244, 63, 94, 0.08);

/* 情報グロー — ライブデータ */
box-shadow: 0 0 20px {colors.info-glow}, 0 0 60px rgba(6, 182, 212, 0.08);
```

## Typography

### Font Stack

```css
/* Display — ヒーロー、見出し、セクションタイトル */
--font-display: 'Manrope', 'Noto Sans JP', sans-serif;

/* Body — 本文、説明文、UIラベル */
--font-body: 'Inter', 'Noto Sans JP', sans-serif;

/* Mono — 価格、エージェントID、プロトコル識別子、コード */
--font-mono: 'JetBrains Mono', monospace;
```

### Loading (Google Fonts)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Tailwind CSS Configuration

```js
// tailwind.config.ts
{
  theme: {
    extend: {
      fontFamily: {
        display: ['Manrope', 'Noto Sans JP', 'sans-serif'],
        body:    ['Inter', 'Noto Sans JP', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
      colors: {
        canvas:    '#06060B',
        surface: {
          1: '#0C0D14',
          2: '#12131D',
          3: '#1A1B28',
          4: '#222336',
        },
        ink: {
          DEFAULT: '#F0F1F5',
          muted:   '#A0A4B8',
          subtle:  '#6B6F82',
          ghost:   '#3D4055',
        },
        accent: {
          DEFAULT: '#7C3AED',
          hover:   '#8B5CF6',
          pressed: '#6D28D9',
        },
        positive: {
          DEFAULT: '#10B981',
          subtle:  'rgba(16, 185, 129, 0.12)',
        },
        negative: {
          DEFAULT: '#F43F5E',
          subtle:  'rgba(244, 63, 94, 0.12)',
        },
        warning: {
          DEFAULT: '#F59E0B',
          subtle:  'rgba(245, 158, 11, 0.12)',
        },
        info: {
          DEFAULT: '#06B6D4',
          subtle:  'rgba(6, 182, 212, 0.12)',
        },
      },
      borderRadius: {
        DEFAULT: '8px',
        lg:      '12px',
        xl:      '16px',
        xxl:     '24px',
      },
      spacing: {
        'section': '80px',
        'hero':    '120px',
      },
    },
  },
}
```

### CSS Variables

```css
:root {
  /* Canvas & Surfaces */
  --color-canvas: #06060B;
  --color-surface-1: #0C0D14;
  --color-surface-2: #12131D;
  --color-surface-3: #1A1B28;
  --color-surface-4: #222336;
  --color-overlay: rgba(6, 6, 11, 0.80);

  /* Ink */
  --color-ink: #F0F1F5;
  --color-ink-muted: #A0A4B8;
  --color-ink-subtle: #6B6F82;
  --color-ink-ghost: #3D4055;

  /* Hairlines */
  --color-hairline: rgba(255, 255, 255, 0.06);
  --color-hairline-strong: rgba(255, 255, 255, 0.12);
  --color-hairline-focus: rgba(255, 255, 255, 0.20);

  /* Accent */
  --color-accent: #7C3AED;
  --color-accent-hover: #8B5CF6;
  --color-accent-pressed: #6D28D9;
  --color-accent-glow: rgba(124, 58, 237, 0.20);

  /* Semantic */
  --color-positive: #10B981;
  --color-positive-subtle: rgba(16, 185, 129, 0.12);
  --color-negative: #F43F5E;
  --color-negative-subtle: rgba(244, 63, 94, 0.12);
  --color-warning: #F59E0B;
  --color-warning-subtle: rgba(245, 158, 11, 0.12);
  --color-info: #06B6D4;
  --color-info-subtle: rgba(6, 182, 212, 0.12);

  /* Typography */
  --font-display: 'Manrope', 'Noto Sans JP', sans-serif;
  --font-body: 'Inter', 'Noto Sans JP', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 9999px;

  /* Transitions */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-conversion: 800ms;
}
```

## Component Specifications

### Buttons

すべてのCTAは `{rounded.md}` (8px)。ボタンの最小高さは40px。Touch viewportでは44px。

- **Accent button**: ブランドアクション（取引開始、確定、接続）にのみ使用。1画面に1つが理想。
- **Surface button**: 二次的アクション（キャンセル、フィルター、切り替え）。
- **Ghost button**: 三次的アクション（リンク的ナビゲーション、追加オプション）。
- **Danger button**: 破壊的アクション（削除、取引取消）。使用前に確認ダイアログを伴う。

### Cards

全カードは `{rounded.lg}` (12px) + 1px `{colors.hairline}` ボーダー。ドロップシャドウは使用しない。

- ホバー時: background が1段階上のサーフェスに遷移 + hairline-strong に変化。
- アクティブ/選択時: 左辺に 2px `{colors.accent}` ボーダーアクセント。

### Admith固有コンポーネント

**Resource Card** — リソースの一覧表示単位。
- 上部: リソース名 (`{typography.heading-sm}`) + カテゴリバッジ
- 中部: 現在価値 (`{typography.price}`) — 正は Emerald、負は Rose
- 下部: 期限タイマー + エージェントアクション状態

**Stat Card** — ダッシュボードのKPI表示。
- 数値: `{typography.price-lg}` JetBrains Mono
- ラベル: `{typography.eyebrow}` uppercase
- 変化率: badge-positive または badge-negative

**Agent Badge** — エージェントの状態表示ピル。
- Idle: `{components.agent-badge}`
- Active: `{components.agent-badge-active}` + 2s pulsing glow animation
- Negotiating: `{components.agent-badge-negotiating}` + subtle shimmer

**Value Conversion Indicator** — Admithの核心表現。
- 負の値: Rose + `−` prefix + 下向き矢印
- 正の値: Emerald + `+` prefix + 上向き矢印
- 転換の瞬間: Rose → Aurora Violet flash (300ms) → Emerald (500ms ease-out)

**Negotiation Timeline** — エージェント交渉の進行表示。
- 垂直タイムライン。各ステップは丸い接続ドット。
- 完了: Emerald ドット + `{components.negotiation-step-completed}`
- アクティブ: Aurora Violet ドット + pulsing glow + `{components.negotiation-step-active}`
- 未到達: ghost ドット + `{colors.ink-ghost}`

### Inputs & Forms

- 全入力: `{colors.surface-1}` + 1px `{colors.hairline}` ボーダー
- フォーカス時: 2px `{colors.accent}` アウトライン (50% opacity)
- エラー時: 2px `{colors.negative}` アウトライン + Rose テキスト
- ラベル: `{typography.label}` + `{colors.ink-muted}`
- プレースホルダー: `{colors.ink-ghost}`

### Tables

- ヘッダー: `{typography.eyebrow}` + `{colors.surface-1}` + sticky
- 行の境界: 1px `{colors.hairline}` bottom border
- ホバー: `{colors.surface-1}` 背景遷移
- ソート可能列: ヘッダーにホバーで `{colors.ink-muted}` → `{colors.ink}` 遷移
- 数値列: 右揃え + `{typography.mono}` + tabular-nums

### Navigation

**Top Nav**: 56px高。`{colors.canvas}` 背景。下部に 1px `{colors.hairline}`。
- 左: Admithロゴ（Manrope 700 + Aurora Violet アクセント）
- 中: ナビリンク（`{typography.label}`）
- 右: 通知 + ユーザーアバター

**Sidebar**: 240px幅。`{colors.surface-1}` 背景。
- アイテム: `{typography.label}` + `{colors.ink-muted}`
- アクティブ: `{colors.surface-2}` 背景 + `{colors.ink}` テキスト + 左辺 2px `{colors.accent}`

## Admith Signature Animations

### 1. Value Conversion Animation（最重要）

負のコスト/廃棄が正の価値に転換する瞬間のシグネチャーアニメーション。

```css
@keyframes value-conversion {
  0%   { color: var(--color-negative); text-shadow: 0 0 8px rgba(244, 63, 94, 0.4); }
  40%  { color: var(--color-accent); text-shadow: 0 0 20px rgba(124, 58, 237, 0.6); transform: scale(1.05); }
  100% { color: var(--color-positive); text-shadow: 0 0 12px rgba(16, 185, 129, 0.3); transform: scale(1); }
}

.value-converting {
  animation: value-conversion var(--duration-conversion) var(--ease-out) forwards;
}
```

### 2. Agent Pulse

アクティブなエージェントの存在を示す呼吸アニメーション。

```css
@keyframes agent-pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--color-accent-glow); }
  50%      { box-shadow: 0 0 0 6px transparent; }
}

.agent-active {
  animation: agent-pulse 2s var(--ease-in-out) infinite;
}
```

### 3. Data Stream

リアルタイムデータフローの微細なシマー。

```css
@keyframes data-shimmer {
  0%   { opacity: 0.5; }
  50%  { opacity: 1; }
  100% { opacity: 0.5; }
}

.data-live {
  animation: data-shimmer 3s var(--ease-in-out) infinite;
}
```

### 4. Surface Hover

カードやリスト項目のホバー遷移。

```css
.hoverable {
  transition: background-color var(--duration-fast) var(--ease-out),
              border-color var(--duration-fast) var(--ease-out);
}
```

## Layout

### Grid System

- Max content width: 1440px (padding 24px)
- Dashboard: 12-column CSS Grid (`gap: 16px`)
- Card grids: `auto-fill, minmax(320px, 1fr)` で自動レスポンシブ
- Sidebar + Content: `240px 1fr` 固定 + フレキシブル

### Spacing Rhythm

垂直リズムは8pxグリッドを基本とする。
- コンポーネント内: `{spacing.sm}` (8px) 〜 `{spacing.base}` (16px)
- セクション間: `{spacing.section}` (80px)
- ヒーローセクション: `{spacing.hero}` (120px)

### Depth Model

Admithではドロップシャドウを一切使用しない。奥行きは以下で表現する:
1. サーフェス段階（色の明度差）
2. ヘアラインボーダー（微細な白のライン）
3. グロー（背後からの光の滲み）
4. Overlay（コンテキスト上のモーダル/ポップオーバー）

## Do's and Don'ts

### Do

- `{colors.canvas}` (#06060B) を全ページの最深面として使用せよ。青みのティントは意図的。
- `{colors.accent}` Aurora Violet の用途を厳格に制限せよ: ブランドマーク、主要CTA、フォーカスリング、Value Conversion Flash。それ以外は禁止。
- 5段階のサーフェスラダーで階層を表現し、レベルスキップを避けよ。
- 価格と数値データには必ず `{typography.price}` / `{typography.mono}` (JetBrains Mono) + tabular-nums を使用せよ。
- Display weight 600-800 と body weight 400 を対比させよ。
- Display タイポグラフィには積極的にネガティブ letter-spacing を適用せよ。
- 負の値には必ず Rose (#F43F5E)、正の値には必ず Emerald (#10B981) を使用せよ。この対応を崩すな。
- カードは常に `{rounded.lg}` (12px) + 1px `{colors.hairline}` ボーダー。
- 奥行きはグローで。ドロップシャドウは使うな。
- アニメーションは控えめに。ただし Value Conversion Animation だけは大胆に表現せよ。
- 日本語テキストでは Noto Sans JP がフォールバック。英語と日本語の混在レイアウトでは行間 1.7 以上を確保。
- すべてのインタラクティブ要素に `:focus-visible` リングを提供せよ (2px `{colors.accent}` at 50% opacity)。
- カラーコントラストは最低 WCAG AA を満たせ。

### Don't

- 純黒 #000000 をキャンバスに使うな。
- Aurora Violet をセクション背景やカードフィルに使うな。
- 2つ目のクロマティックアクセント（オレンジ、ピンク等）を追加するな。セマンティック色以外に色を増やすな。
- ドロップシャドウを使うな。一切。
- 装飾的なグラジエント背景を使うな。グローはインタラクティブ要素の背後にのみ。
- カードの角丸をpill (9999px) にするな。常に `{rounded.lg}` (12px)。
- Light mode をデフォルトにするな。Dark-first。
- Manrope を body テキストに使うな。Display 専用。
- Inter を見出しに使うな。Body/UI 専用。
- JetBrains Mono を説明文に使うな。価格・ID・コード専用。
- エージェントの交渉ステータスに色で意味を表現する際、セマンティック色以外を使うな。
- アニメーション duration を 1 秒以上にするな（Value Conversion の 800ms が最長）。

## Responsive Behavior

### Breakpoints

| Name | Width | Key Changes |
|---|---|---|
| Desktop-XL | ≥1440px | 12-column grid。フルサイドバー表示 |
| Desktop | ≥1280px | 12-column 維持。カード3-up |
| Tablet | ≥1024px | カード 3-up → 2-up。サイドバーがオーバーレイに |
| Mobile-Lg | ≥768px | カード 2-up → 1-up。ナビハンバーガー化。stat-card は横スクロール |
| Mobile | ≥375px | 単一カラム。display-hero → display-md にスケール |

### Touch Targets

- CTAs: ≥44px tap height on touch viewports
- Table rows: ≥48px tap height on touch
- Sidebar items: ≥44px on touch
- Input fields: ≥44px on touch

### Collapsing Strategy

- **Top nav**: 768px以下でハンバーガー化
- **Sidebar**: 1024px以下でオーバーレイ
- **Card grids**: auto-fill で自動 1-up まで縮小
- **Stat cards**: 768px以下で水平スクロール
- **Display type**: hero 72px → mobile 32px

### Image & Chart Behavior

- チャートはアスペクト比を維持してリフロー
- ダッシュボードグラフは最小幅 280px を確保
- エージェントアバターは 32px (desktop) / 28px (mobile)

## Admith Brand

### Logo

- タイプマーク: "Admith" in Manrope 700, `{colors.ink}`
- "A" の文字に Aurora Violet (#7C3AED) を適用するオプションあり（アイコン文脈で）
- 最小サイズ: 高さ 20px
- クリアスペース: ロゴ高さの 50% を四方に確保
- ダーク背景上: `{colors.ink}` テキスト
- ライト背景上: `{colors.inverse-ink}` テキスト

### Naming Convention

- プロダクト名は "Admith [Product]" 形式 (例: Admith Flow, Admith Signal, Admith Trust)
- プロダクト名のサフィックスは Manrope 400 (display weight より軽く)

### Brand Voice in UI

- コピーは簡潔、技術的、しかし人間的
- "your agent" ではなく "agents" (ユーザーの所有物ではなく、エコシステムの参加者として描写)
- 数値の変化を肯定的に表現: "Saved" "Recovered" "Converted" (not "Reduced waste")
- エラーメッセージは解決手段を含む

## Iteration Guide

1. 1つのコンポーネントに集中し、`components:` トークン名で参照せよ。
2. セクション導入時、まずどのサーフェスレベルに載せるか決定せよ。
3. Body テキストのデフォルトは `{typography.body}` weight 400。
4. 編集後は `npx @google/design.md lint DESIGN.md` でバリデーション。
5. 新バリアント（hover, active, pressed）は別の component entry として追加。
6. Aurora Violet は希少に: ブランドマーク、主CTA、フォーカス、Value Conversion。
7. 数値データは常にモノスペースフォント + tabular-nums。
8. 全プロダクト (Admith Flow, Signal, Trust 等) はこのシステムを継承。プロダクト固有の拡張は別ファイル (DESIGN-[product].md) で管理。

## Agent Prompt Guide

When generating UI for any Admith product:

1. Always resolve tokens from the YAML front matter above before writing CSS/JSX.
2. Never hardcode hex values — use CSS custom properties (--color-*, --font-*).
3. For value displays: positive = Emerald, negative = Rose, neutral = ink-muted. No exceptions.
4. Every card: surface-1 background + hairline border + rounded-lg. No shadows.
5. Data tables: eyebrow headers, mono font for numbers, right-align numeric columns.
6. Prioritize the Value Conversion Animation for any feature that transforms negative resources to positive.
7. When in doubt about surface level, pick ONE level above the parent container.
8. Japanese text: ensure line-height ≥ 1.7 for mixed EN/JP content.
9. All interactive elements need :focus-visible with 2px accent outline at 50% opacity.
10. Use Framer Motion (or CSS transitions) for hover/state changes. Keep durations ≤ 400ms except Value Conversion (800ms).

## Known Gaps

- Light mode inverse mapping は定義済みだが、コンポーネント単位でのバリデーションは未実施。
- チャート/グラフライブラリ (Recharts, D3) 向けのカラーパレット拡張は今後追加予定。
- モバイルジェスチャー (swipe-to-dismiss, pull-to-refresh) のタイミング定義は未策定。
- アクセシビリティ: WCAG AAA の完全準拠は一部の ink-subtle / surface 間コントラストで未達成。
- Manrope は日本語をカバーしないため、見出しでの英日混在時は文字サイズの視覚的整合を手動調整する必要がある。
- 印刷用スタイルシートは未定義。

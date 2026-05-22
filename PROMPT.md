# Admith フロントエンド全面刷新

プロジェクトルートにある `DESIGN.md` を最初に完全に読み込み、以下を実行せよ。

---

## 前提ルール（全作業を通じて厳守）

- hex値の直書き禁止。色はすべてCSS変数 (`var(--color-*)`) またはTailwindトークン経由で参照する
- ドロップシャドウ (`box-shadow` with y-offset) 使用禁止。奥行きはサーフェスレベル差とglow-shadowで表現
- カードの角丸: 必ず `rounded-lg` (12px) 統一
- ボタンの角丸: 必ず `rounded-md` (8px) 統一。最小高さ 40px
- 全インタラクティブ要素に `:focus-visible` (2px accent outline at 50% opacity) を必須で付与
- 正の値: 必ず Emerald (`--color-positive`)。負の値: 必ず Rose (`--color-negative`)。例外なし
- 数値データ: 必ず JetBrains Mono + `font-feature-settings: 'tnum', 'lnum'`
- Aurora Violet (`--color-accent`) の使用箇所: ブランドマーク / 主要CTA / focus-ring / Value Conversion Flash のみ
- アニメーション duration: 最大400ms（Value Conversion Animationの800msのみ例外）
- 日本語混在テキスト: `line-height: 1.7` 以上を確保

---

## STEP 1: CSS基盤・Tailwind設定

### 1-1. tailwind.config.ts

DESIGN.mdのカラー・フォント・spacing・border-radiusトークンをTailwindに反映せよ。

```typescript
// tailwind.config.ts に追加・マージする内容
{
  theme: {
    extend: {
      fontFamily: {
        display: ['Manrope', 'Noto Sans JP', 'sans-serif'],
        body:    ['Inter', 'Noto Sans JP', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
      colors: {
        canvas: '#06060B',
        surface: { 1: '#0C0D14', 2: '#12131D', 3: '#1A1B28', 4: '#222336' },
        ink: { DEFAULT: '#F0F1F5', muted: '#A0A4B8', subtle: '#6B6F82', ghost: '#3D4055' },
        accent: { DEFAULT: '#7C3AED', hover: '#8B5CF6', pressed: '#6D28D9' },
        positive: { DEFAULT: '#10B981', subtle: 'rgba(16,185,129,0.12)' },
        negative: { DEFAULT: '#F43F5E', subtle: 'rgba(244,63,94,0.12)' },
        warning:  { DEFAULT: '#F59E0B', subtle: 'rgba(245,158,11,0.12)' },
        info:     { DEFAULT: '#06B6D4', subtle: 'rgba(6,182,212,0.12)' },
        hairline:        'rgba(255,255,255,0.06)',
        'hairline-strong': 'rgba(255,255,255,0.12)',
      },
      borderRadius: {
        sm: '4px', DEFAULT: '8px', md: '8px', lg: '12px', xl: '16px', xxl: '24px',
      },
      spacing: { section: '80px', hero: '120px' },
    },
  },
}
```

### 1-2. globals.css

以下を globals.css に追加せよ。

```css
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+JP:wght@400;500;600;700&display=swap');

/* Design Tokens */
:root {
  /* Canvas & Surfaces */
  --color-canvas:    #06060B;
  --color-surface-1: #0C0D14;
  --color-surface-2: #12131D;
  --color-surface-3: #1A1B28;
  --color-surface-4: #222336;
  --color-overlay:   rgba(6, 6, 11, 0.80);

  /* Ink */
  --color-ink:        #F0F1F5;
  --color-ink-muted:  #A0A4B8;
  --color-ink-subtle: #6B6F82;
  --color-ink-ghost:  #3D4055;

  /* Hairlines */
  --color-hairline:       rgba(255, 255, 255, 0.06);
  --color-hairline-strong: rgba(255, 255, 255, 0.12);
  --color-hairline-focus:  rgba(255, 255, 255, 0.20);

  /* Accent */
  --color-accent:         #7C3AED;
  --color-accent-hover:   #8B5CF6;
  --color-accent-pressed: #6D28D9;
  --color-accent-glow:    rgba(124, 58, 237, 0.20);

  /* Semantic */
  --color-positive:        #10B981;
  --color-positive-subtle: rgba(16, 185, 129, 0.12);
  --color-positive-glow:   rgba(16, 185, 129, 0.20);
  --color-negative:        #F43F5E;
  --color-negative-subtle: rgba(244, 63, 94, 0.12);
  --color-negative-glow:   rgba(244, 63, 94, 0.20);
  --color-warning:         #F59E0B;
  --color-warning-subtle:  rgba(245, 158, 11, 0.12);
  --color-warning-glow:    rgba(245, 158, 11, 0.20);
  --color-info:            #06B6D4;
  --color-info-subtle:     rgba(6, 182, 212, 0.12);
  --color-info-glow:       rgba(6, 182, 212, 0.20);

  /* Fonts */
  --font-display: 'Manrope', 'Noto Sans JP', sans-serif;
  --font-body:    'Inter', 'Noto Sans JP', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;

  /* Radius */
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-pill: 9999px;

  /* Transitions */
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast:       150ms;
  --duration-normal:     250ms;
  --duration-slow:       400ms;
  --duration-conversion: 800ms;
}

/* Base */
body {
  background-color: var(--color-canvas);
  color: var(--color-ink);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Glow Utilities */
.glow-accent   { box-shadow: 0 0 20px var(--color-accent-glow),   0 0 60px rgba(124,58,237,0.08); }
.glow-positive { box-shadow: 0 0 20px var(--color-positive-glow), 0 0 60px rgba(16,185,129,0.08); }
.glow-negative { box-shadow: 0 0 20px var(--color-negative-glow), 0 0 60px rgba(244,63,94,0.08); }
.glow-info     { box-shadow: 0 0 20px var(--color-info-glow),     0 0 60px rgba(6,182,212,0.08); }

/* Hover Transition */
.hoverable {
  transition:
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}

/* Signature Animations */
@keyframes value-conversion {
  0%   { color: var(--color-negative); text-shadow: 0 0 8px rgba(244,63,94,0.4); }
  40%  { color: var(--color-accent); text-shadow: 0 0 20px rgba(124,58,237,0.6); transform: scale(1.05); }
  100% { color: var(--color-positive); text-shadow: 0 0 12px rgba(16,185,129,0.3); transform: scale(1); }
}
.value-converting {
  animation: value-conversion var(--duration-conversion) var(--ease-out) forwards;
}

@keyframes agent-pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--color-accent-glow); }
  50%       { box-shadow: 0 0 0 6px transparent; }
}
.agent-active {
  animation: agent-pulse 2s var(--ease-in-out) infinite;
}

@keyframes data-shimmer {
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 1; }
}
.data-live {
  animation: data-shimmer 3s var(--ease-in-out) infinite;
}

/* Focus Ring */
:focus-visible {
  outline: 2px solid rgba(124, 58, 237, 0.5);
  outline-offset: 2px;
}
```

---

## STEP 2: 共通コンポーネントの構築

以下のコンポーネントをDESIGN.mdのコンポーネントトークンに厳密に従い実装せよ。

### Button (`components/ui/Button.tsx`)

```
variant: accent / surface / ghost / danger
size: sm (32px) / md (40px) / lg (48px)
状態: hover / pressed / disabled / loading
- accent: bg[--color-accent] hover:bg[--color-accent-hover]
- surface: bg[--color-surface-2] hover:bg[--color-surface-3]
- ghost: bg-transparent hover:bg[--color-surface-1]
- danger: bg[--color-negative]
- 全variant: rounded-md(8px), font-bodyのfont-medium 14px
- disabled: opacity-40 cursor-not-allowed
- loading: スピナー表示。テキスト非表示
```

### Card (`components/ui/Card.tsx`)

```
variant: default / elevated / interactive
- 全variant: rounded-lg(12px), border 1px [--color-hairline], bg[--color-surface-1]
- elevated: bg[--color-surface-2]
- interactive:
  hover → bg[--color-surface-2], border-color[--color-hairline-strong]
  selected → left-border 2px [--color-accent]
- ドロップシャドウ禁止
```

### Badge (`components/ui/Badge.tsx`)

```
variant: default / positive / negative / warning / info
- 全variant: rounded-pill(9999px), font-mono 11px, padding 2px 8px
- default:   bg[--color-surface-3] text[--color-ink-muted]
- positive:  bg[--color-positive-subtle] text[--color-positive]
- negative:  bg[--color-negative-subtle] text[--color-negative]
- warning:   bg[--color-warning-subtle]  text[--color-warning]
- info:      bg[--color-info-subtle]     text[--color-info]
```

### Input / Select (`components/ui/Input.tsx`, `Select.tsx`)

```
- bg[--color-surface-1], border 1px [--color-hairline], rounded-md, padding 10px 14px, height 40px
- label: font-body 13px font-medium color[--color-ink-muted]
- placeholder: color[--color-ink-ghost]
- focus: border-color[--color-accent] + focus-visible ring
- error: border-color[--color-negative] + error text in [--color-negative]
```

### Table (`components/ui/Table.tsx`)

```
- header: font-mono 11px uppercase tracking-wider color[--color-ink-subtle], bg[--color-surface-1], sticky top-0, padding 12px 16px
- row: border-bottom 1px [--color-hairline], padding 12px 16px
- row hover: bg[--color-surface-1] transition
- 数値列: text-right font-mono tabular-nums
- striped禁止（borderで十分）
```

### Modal (`components/ui/Modal.tsx`)

```
- overlay: bg[--color-overlay] backdrop-blur-sm
- panel: bg[--color-surface-2] rounded-xl(16px) padding 32px
- 閉じるボタン: ghost variant Button
- アニメーション: opacity 0→1 + translateY 8px→0, duration 250ms
```

---

## STEP 3: Admith固有コンポーネント

### StatCard (`components/admith/StatCard.tsx`)

```tsx
interface StatCardProps {
  label: string          // eyebrow: JetBrains Mono 11px uppercase
  value: string | number // price-lg: JetBrains Mono 28px font-semibold tabular-nums
  delta?: number         // 変化率: badge-positive(+) or badge-negative(-)
  variant?: 'default' | 'positive' | 'negative'
}
// variant='positive': bg[--color-positive-subtle]
// variant='negative': bg[--color-negative-subtle]
// delta表示: "+12.3%" or "−5.1%"
```

### ResourceCard (`components/admith/ResourceCard.tsx`)

```tsx
interface ResourceCardProps {
  name: string          // heading-sm: Manrope 16px font-semibold
  category: string      // Badge default variant
  value: number         // price: JetBrains Mono 16px
                        //   正: color[--color-positive] + "+"プレフィックス
                        //   負: color[--color-negative] + "−"プレフィックス
  deadline?: Date       // "あと X分" Amber テキスト + 警告アイコン
  agentState: 'idle' | 'active' | 'negotiating'
}
// agentStateはAgentBadgeコンポーネントを使用
```

### AgentBadge (`components/admith/AgentBadge.tsx`)

```tsx
type AgentState = 'idle' | 'active' | 'negotiating'
// idle:         bg[--color-surface-2] text[--color-ink-muted]
// active:       bg[--color-accent-glow] text[--color-accent] + agent-pulse class
// negotiating:  bg[--color-warning-subtle] text[--color-warning] + data-shimmer class
// 全state: rounded-pill font-mono 11px padding 4px 10px
```

### ValueConversionIndicator (`components/admith/ValueConversionIndicator.tsx`)

```tsx
interface ValueConversionProps {
  from: number   // 転換前の値（負）
  to: number     // 転換後の値（正）
  converting?: boolean  // trueのとき value-converting クラスを付与
  size?: 'sm' | 'lg'   // sm: price(16px) / lg: price-lg(28px)
}
// converting=false: from値をRoseで表示
// converting=true:  value-converting アニメーション起動 → Emeraldで終着
// 転換完了: glow-positive クラスを追加してEmeraldグローを残す
// 数値変化: from→to のカウントアップアニメーション（1000ms）と同期
```

### NegotiationTimeline (`components/admith/NegotiationTimeline.tsx`)

```tsx
interface TimelineStep {
  id: string
  label: string
  status: 'pending' | 'active' | 'completed'
  timestamp?: string
  agent?: string
}
// pending:   bg[--color-ink-ghost] ドット + text[--color-ink-ghost]
// active:    bg[--color-accent] ドット + agent-pulse + bg[--color-accent-glow] 行背景
// completed: bg[--color-positive] ドット + text[--color-ink-muted] + checkmark
// 垂直ライン: border-left 1px [--color-hairline]
// timestamp: font-mono 11px color[--color-ink-subtle]
// agent表示: AgentBadge コンポーネントを使用
```

---

## STEP 4: レイアウト・ナビゲーション

### TopNav (`components/layout/TopNav.tsx`)

```
高さ 56px, bg[--color-canvas], border-bottom 1px [--color-hairline]
左: "Admith" Manrope 700 color[--color-ink] + "Flow" Manrope 400 color[--color-ink-muted]
右: 通知ベルアイコン(ghost button) + ユーザーアバター(32px, rounded-full)
768px以下: ハンバーガーアイコン。Sidebar をDrawer表示に切り替え
```

### Sidebar (`components/layout/Sidebar.tsx`)

```
幅 240px, bg[--color-surface-1], border-right 1px [--color-hairline]
ナビアイテム:
  default: bg-transparent text[--color-ink-muted] rounded-md padding 8px 12px
  active:  bg[--color-surface-2] text[--color-ink] border-left 2px [--color-accent]
1024px以下: position fixed, overlay背景, 幅100%でDrawer化
```

### DashboardLayout (`components/layout/DashboardLayout.tsx`)

```
全体: flex。TopNav(56px fixed) + Sidebar(240px) + main
main: padding-top 56px, padding-left 240px (desktop)
      display grid, 12-column, gap 16px, max-width 1440px, padding 24px
StatCard行: grid-cols-3 (desktop) / grid-cols-2 (tablet) / 横スクロール (mobile)
```

---

## STEP 5: ページ実装

### ダッシュボードページ (`app/page.tsx` または `app/dashboard/page.tsx`)

```
レイアウト: DashboardLayout を使用

セクション1 — KPI行 (grid-cols-3, gap 16px)
  StatCard: 本日の取引件数 (data-live class)
  StatCard: 総転換額 variant=positive
  StatCard: 稼働エージェント数 (data-live class)

セクション2 — リソース一覧 (margin-top 32px)
  見出し: "アクティブリソース" eyebrow typography
  ResourceCard のグリッド: auto-fill minmax(320px, 1fr), gap 16px
  期限が近い順にソート。deadlineが24時間以内はwarning Badge

セクション3 — 交渉ログ (margin-top 32px)
  見出し: "交渉タイムライン" eyebrow typography
  NegotiationTimeline: 直近10件のステップ表示

セクション4 — 転換サマリー (margin-top 32px)
  ValueConversionIndicator を大きく配置
  "本日 X件の廃棄を価値に転換しました" の成果メッセージ
```

### リソース詳細ページ (`app/resources/[id]/page.tsx`)

```
ヒーロー:
  ResourceCard の拡張レイアウト (full-width)
  ValueConversionIndicator size='lg' を中央に配置
  転換前/後の値の差分を大きく表示

交渉プロセス:
  NegotiationTimeline: フルプロセス全ステップ

参加エージェント:
  AgentBadge リスト (flex wrap)

詳細データ Table:
  交渉ラウンド / 提示価格 / タイムスタンプ / エージェントID
  全数値列: right-align + font-mono + tabular-nums
```

---

## 最終確認事項

全実装が完了したら以下をセルフチェックせよ:

1. `grep -r "#[0-9A-Fa-f]\{3,6\}" src/` でhexハードコードがゼロであることを確認
2. `grep -r "box-shadow" src/` で y-offset付きのドロップシャドウがないことを確認
3. 全カードの className に `rounded-lg` が含まれることを確認
4. `grep -r "JetBrains Mono\|font-mono" src/` で数値表示箇所全てにモノスペースが適用されていることを確認
5. 全 `<button>` / `<a>` / `<input>` に focus-visible スタイルが効いていることをブラウザDevToolsで確認

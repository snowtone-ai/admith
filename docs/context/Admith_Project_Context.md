# Admith — プロジェクトコンテキスト
**用途:** VSCode Claude Code / Codex に渡す補助コンテキスト  
**役割:** ビジネス戦略書・技術設計書に入らない判断経緯・監査結果・開発方針をまとめる

---

## 1. プロジェクト概要

- **プロダクト名:** Admith（アダム・スミスの「見えざる手」より）
- **Mission:** 世界中の全てのリソースの最適化により、人々に幸福をもたらす
- **プロダクト概要:** AIエージェントによる取引プラットフォーム。物・情報・時間、全てのリソースを人間を介さずAIエージェント同士が自律的に自由取引する
- **開発・テスト環境:** エージェント交渉シミュレーションはGemini API（無料枠等）を活用

---

## 2. これまでのセッション履歴

| Session | 内容 | 成果 |
|---|---|---|
| Session 1-2 | ブレインストーミング | 84リソース定義、本質命題確定、Phase 0-3設計 |
| Session 3-4 | 分類・数値化・法規制 | Cat.0-6分類、ユニットエコノミクス、18ヶ月ロードマップ |
| Deep Research | Felo 5件 + Gemini | 競合・ZKP・法的有効性・交渉プロトコル・ユーザー心理 |
| Session 5 | プロダクト設計 | Admith Accord命名、2製品体系、エージェントロール柔軟化 |
| Session 5続 | システム設計 Step 1,3,4 | アーキテクチャ・データモデル・詳細設計 |
| ChatGPT監査 | 5.5 Thinking拡張 | 58/100点。致命的欠陥6件、改善点6件、攻撃シナリオ10件 |
| Session 5最終 | 監査反映 | 設計v2確定。Human Approval、Resource Lock、TTL分割等 |

---

## 3. ChatGPT監査の主要結果と反映状況

### 致命的欠陥（全て反映済み）

| # | 欠陥 | 修正内容 | 反映先 |
|---|---|---|---|
| 1 | Orchestrator SPOF | Workflow Engine（Durable Execution）採用 | 技術設計書 §1, §2 |
| 2 | Resource二重ロック | lock_token + locked_until + SELECT FOR UPDATE | 技術設計書 §4 Resource |
| 3 | Ed25519署名の法的弱さ | Human Final Approval + 電子契約サービス連携 | 技術設計書 §4, §5 |
| 4 | Sybil価格操作 | KYB必須 + 招待制 + OwnerEntity単位の管理 | 技術設計書 §4, §10 |
| 5 | LLM非決定性 | 契約判断からLLM排除。Rule Engineで確定 | 技術設計書 §7, §9 |
| 6 | TTL=30秒が短すぎ | 5段階TTL分割 | 技術設計書 §5 |

### 過剰設計（全て削減済み）

| 削減対象 | Phase 0の代替 |
|---|---|
| CVE / Vector DB | 削除。Phase 1へ |
| 全状態Event Sourcing + CQRS | Negotiation限定に縮小 |
| Accord公開API | 内部のみ。Phase 1へ |
| Escrow / Micropayment | 請求書払い・月次精算 |
| 汎用Domain Plugin | FoodWaste直書き |
| Trust Score有料API | 削除 |

### 監査で追加された設計要素

- `PENDING_HUMAN_APPROVAL` 状態
- `ApprovalRequest` / `ApprovalDecision` テーブル
- `AgentMandate` テーブル（権限委任台帳）
- `lock_token` / `locked_until` / `locked_by_negotiation_id` カラム
- `nonce` カラム（Message、Replay攻撃防止）
- 下請法→取適法（2026年1月改正）への対応
- 廃棄物処理法の委託契約・マニフェスト確認ワークフロー

---

## 4. 開発環境・ワークフロー

### pm-zero v9.4 (Lean Task Ledger OS)

本プロジェクトは pm-zero v9.4 ワークフローに従う。

| ファイル | 役割 |
|---|---|
| `docs/vision.md` | プロダクトの北極星 |
| `tasks.md` | 実行タスク台帳 |
| `docs/state.md` | 現在のポインタ |
| `docs/decisions.md` | 永続的な判断記録 |
| `docs/issues.md` | 失敗ログ |
| `docs/repo-map.md` | リポジトリナビゲーション |
| `AGENTS.md` | エージェント共通ルール |
| `CLAUDE.md` | Claude Code固有設定 |

### 追加スキル（mattpocock/skills から選択採用）

以下3つをインストール推奨:
```powershell
npx skills@latest add mattpocock/skills/grill-me
npx skills@latest add mattpocock/skills/git-guardrails-claude-code
npx skills@latest add mattpocock/skills/handoff
```

| スキル | 用途 |
|---|---|
| `grill-me` | 設計の穴を徹底的に尋問。ChatGPT監査と同等の効果をClaude Code内で実行 |
| `git-guardrails` | push, reset --hard, clean等の破壊的操作をフックで阻止 |
| `handoff` | セッション間の引継ぎ文書を自動圧縮 |

### 不採用ツール

| ツール | 不採用理由 |
|---|---|
| github/spec-kit | pm-zero v9.4と機能が完全重複。指示系統の二重化を回避 |
| mattpocock/caveman | トークン削減は有用だが、Admithの設計相談では正確性を最優先 |
| mattpocock/write-a-prd | pm-zeroのvision.mdと重複 |

---

## 5. 技術スタック（Phase 0想定）

| レイヤー | 技術 | 理由 |
|---|---|---|
| 言語 | Python (FastAPI) | エージェント・LLM統合のエコシステムが最も成熟 |
| DB | PostgreSQL + PostGIS | JSONB・地理・RLS・SELECT FOR UPDATE |
| キャッシュ | Redis | キャッシュのみ。状態の真実はDB |
| Workflow | Temporal or Inngest | Durable Execution。SPOF解消 |
| LLM | Gemini 1.5 Flash（初期） | コスト$0.40/Mトークン。Abstractionで切替可能 |
| 認証 | OAuth 2.1 | B2B標準 |
| 署名 | Ed25519 | メッセージ署名（法的署名は電子契約サービス） |
| 電子契約 | クラウドサイン等 | 日本法対応の電子契約基盤 |
| マニフェスト | 電子マニフェストAPI | 廃棄物処理法対応 |
| モニタリング | OpenTelemetry | 分散トレーシング |

---

## 6. Phase 0 MVP スコープ

ChatGPT監査の最終判断を反映:

```
Phase 0 MVP =
  食品廃棄物B2Bの
  + 自動候補探索（Matching Engine）
  + 自動交渉案生成（Rule Engine + LLM補助）
  + 人間最終承認（Approval Gate）
  + 確定前Resource Lock（lease token）
  + 電子契約連携
  + 電子マニフェスト連携
  + 監査ログ（ハッシュチェーン）
  + Operator Dashboard

Phase 0 で含めないもの:
  - 完全自動契約（人間承認をバイパス）
  - 汎用プロトコル公開
  - CVE / Vector DB
  - マイクロ決済
  - Trust Score API
```

### 完全自動取引への移行条件

```
- 同一取引パターンで30-50件以上の事故なし
- 価格乖離率が閾値以内
- 相手先がKYB済み
- 物流遅延率が低い
- Human Approvalのreject率が5%未満
- 法務がAgentMandateを承認
```

---

## 7. 開発ステップ（推奨順序）

```
Step 1: ★完了
  システム全体アーキテクチャ設計（本ドキュメント群）

Step 2: 次に実行
  Gemini APIで4者間交渉のPoC
  - 交渉が30秒以内に収束するか検証
  - 200行程度の検証コード（捨てるコード想定）

Step 3: 実装開始
  pm-zero v9.4のPhase 1-3に従い、
  tasks.mdにタスク分解→実装

Step 4: テスト・検証
  Food Waste ドメインでの小規模マッチング実験
```

---

## 8. 参照ファイル一覧

本プロジェクトのコンテキストは以下のファイル群で構成される:

| ファイル | 内容 | 参照タイミング |
|---|---|---|
| `Admith_Business_Strategy.md` | ビジネス戦略・市場・競合・ロードマップ | 設計判断時 |
| `Admith_Technical_Design.md` | システム設計・データモデル・セキュリティ | 実装時 |
| `Admith_Project_Context.md` | 本ファイル。判断経緯・監査結果・開発方針 | セッション開始時 |
| `Admith_Resource_Master_v1.md` | 全84リソースの定義・本質命題 | リソース詳細が必要な時 |
| `Admith_Session_Handoff_v2.md` | Session 3-4の詳細引継ぎ | 数値根拠が必要な時 |
| `Admith_DeepResearch_v1.md` | 市場調査・競合・法規制の一次情報 | エビデンス確認時 |

---

## 9. 注意事項（エージェント向け）

1. **Admithは「完全自動取引」ではなく「自動交渉 + 人間承認」から始める。** これはChatGPT監査で確定した最も重要な設計判断。
2. **LLMは契約判断に使わない。** 価格・制約・合意条件は決定論的Rule Engineで確定。LLMは文面生成・要約のみ。
3. **Phase 0はFood Waste専用。** 汎用プロトコル志向は時期尚早。ドメインに深く刺すことを優先。
4. **招待制10社。** 自由登録は禁止。KYB必須。Sybil攻撃リスクを構造的に排除。
5. **法規制は設計に組み込む。** 廃棄物処理法・食品リサイクル法・取適法の要件はCode外のドキュメントではなく、Compliance Rule Engineとワークフローに直接実装。

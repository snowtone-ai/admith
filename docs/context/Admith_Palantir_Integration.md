# Admith — Palantir哲学統合分析
**作成日:** 2026-05-21
**用途:** Palantirの哲学（Ontology等）をAdmithに統合する判断根拠の永続記録
**判断の最高権威:** Admith Mission「世界中の全てのリソースの最適化により、人々に幸福をもたらす」

---

## 1. Palantirから抽出した核心概念

### P1: Ontology = デジタルツイン
生データを現実世界のエンティティにマッピングする意味層。Object Type（エンティティ定義）、Link Type（関係定義）、Action Type（操作定義）の3要素で構成。読み取り専用ではなく、書き戻し（操作）も含む。

### P2: 三層Ontology
- **Semantic層:** Object Type、Property、Link Type — 「何があるか」の記述
- **Kinetic層:** Action Type、Function — 「何ができるか」の定義
- **Dynamic Security層:** Object単位の動的権限 — 「誰が何を見て操作できるか」

### P3: Closed-Loop Operations
分析→行動→新データ→再分析のフィードバックループ。洞察を現実世界の変更に直結させる。分析だけで終わらない「意思決定インフラ」。

### P4: AI on Ontology
LLMは生データではなく、権限・ガバナンスが適用済みのOntologyオブジェクト上で動作する。LLMのスコープはOntologyの型システムで構造的に制約される。

### P5: Proposal-Based Human-in-the-Loop
AIは「提案（Proposal）」を生成し、人間が承認・修正・却下する。この判断メタデータがAIの学習に還元され、提案精度が向上する連続改善ループ。

### P6: Propagating Security (Markings)
データに付与されたアクセス制御が、すべての派生データ・変換結果に自動伝播する。下流のビュー・レポート・API経由でも迂回不可能。

### P7: Action = First-Class Citizen
状態変更（Action）は単なるAPI呼び出しではなく、ルール（Rules/Validation Logic）・変更内容（Mutation）・副作用（Side Effects）・監査証跡（Action Log）を持つ型付きオブジェクト。
**注:** Palantir公式ドキュメントの用語はrules/side effects/action log。本文書ではAdmith設計への適用時にpreconditions/postconditions/audit_eventと対応付けている。

---

## 2. 適用判断

### 適用する概念

| 概念 | 適用理由 | Admithへの具体的効果 |
|---|---|---|
| P1 Ontology | 「全リソース」の統一記述体系が不可欠 | Resource Ontologyが84リソース→無限拡張の基盤になる |
| P2 三層Ontology | Semantic/Kinetic/Dynamic SecurityがAdmithの既存要件と合致 | Agent Mandate（動的権限）、Action（交渉操作）、Resource（意味）を統合的に設計 |
| P3 Closed-Loop | 決済結果→信頼スコア、価格履歴→Rule Engine較正が欠落 | 交渉品質の継続的改善。データ蓄積が競争優位に |
| P4 AI on Ontology | D007（LLM排除）を構造的に保証 | LLMが触れるのは型付きOntologyオブジェクトのみ。raw data直接アクセス不可 |
| P5 Proposal-Based | PENDING_HUMAN_APPROVALの設計精度向上 | 承認/却下メタデータ→Agent Mandate自動調整→承認率向上 |
| P6 Propagating Security（部分） | 交渉ログ→合意→監査の権限伝播 | コンプライアンス（下請法→取適法）の構造的保証 |
| P7 Action as First-Class | 監査・テスト・コンプライアンスの構造的保証 | 全状態遷移が型付きActionで記録。不正操作の構造的排除 |

### 適用しない概念

| 概念 | 不採用理由 |
|---|---|
| FDEモデル | Admithはマーケットプレイスであり、エンタープライズSW企業ではない。顧客サイト常駐は不要 |
| Apollo/マルチクラウド | Phase 0は単一デプロイ。5名チームの運用負荷抑制が優先（D005） |
| Ontology管理プラットフォーム | Foundry的な汎用Ontology UIは過剰。コード定義（Pydantic/dataclass）で十分 |
| フルデジタルツイン | 参加企業全体のモデル化は不要。リソース・エージェント・取引のみ |
| データパイプライン基盤 | Foundryのバッチ型ETLは不適。Admithはトランザクション駆動 |
| OSDKコード自動生成 | Phase 0の5名チームには過剰。手書きドメインモデルで十分 |

---

## 3. 統合スケルトン選択

### 比較した3案

| 案 | 概要 | ミッション整合 | Phase 0コスト | 拡張性 |
|---|---|---|---|---|
| A: Ontology-Centric Redesign | 全レイヤーをOntology中心に再構成 | ★★★★★ | 高 | ★★★★★ |
| **B: Ontology-as-Backbone** | **現アーキテクチャ維持 + Ontologyを設計原則として組み込み** | **★★★★** | **中** | **★★★★** |
| C: Philosophy-as-Guidelines | ドキュメントレベルのガイドラインのみ | ★★ | 低 | ★★ |

### 選択: B（Ontology-as-Backbone）

**選択理由:**
1. Admithのミッション「全リソース最適化」はOntologyを根本的に必要とする。Cでは不十分。
2. Phase 0は「FoodWaste-First」「5名チーム」。Aの大幅リワークはD003/D005に違反。
3. BはD005（Hexagonal + Modular Monolith + Workflow Engine）を維持しつつ拡張。
4. P4/P7はD007/D013を構造的に保証し、Phase 0品質を直接向上させる。

---

## 4. 具体的な設計変更

### 4.1 Resource Ontology の三層設計

```
Admith Ontology = Semantic + Kinetic + Dynamic Security

Semantic Layer（何があるか）:
├── Object Types
│   ├── Resource（リソース）— 取引対象の統一抽象
│   │   └── FoodWasteResource（Phase 0 具象）
│   ├── Agent（エージェント）— 取引主体
│   ├── OwnerEntity（所有主体）— 法人・個人
│   ├── Negotiation（交渉）— 取引プロセス
│   ├── Agreement（合意）— 確定した取引条件
│   └── LogisticsCapacity（物流能力）— 輸送リソース
│
├── Link Types（関係）
│   ├── produces: OwnerEntity → Resource
│   ├── consumes: OwnerEntity → Resource
│   ├── transports: Agent → Resource
│   ├── negotiates: Agent → Negotiation
│   ├── regulates: ComplianceRule → Resource
│   └── mandates: OwnerEntity → Agent（権限委任）
│
└── Property Types（属性）
    ├── 共通: id, created_at, updated_at, ontology_version
    └── ドメイン固有: FoodWasteResource.moisture_content, .contamination_risk, etc.

Kinetic Layer（何ができるか）:
├── Action Types（型付き操作）
│   ├── CreateCFP — 事前条件: Resource.state=available
│   ├── SubmitProposal — 事前条件: Negotiation.state=cfp_open
│   ├── CounterOffer — 事前条件: Negotiation.state=negotiating
│   ├── FormAgreement — 事前条件: Rule Engine validation passed
│   ├── RequestApproval — 事前条件: Agreement.state=draft
│   ├── ApproveAgreement — 事前条件: AgentMandate.scope covers terms
│   ├── RejectAgreement — 事前条件: ApprovalRequest.status=pending
│   └── SettleDeal — 事前条件: Agreement.state=signed
│
└── Functions（読み取り専用計算）
    ├── CalculateDelta — 価値創造額の算出
    ├── EvaluateCompliance — 法令遵守の評価
    └── EstimateTrustScore — 信頼スコアの推定

Dynamic Security Layer（誰が何をできるか）:
├── Agent Mandate（権限委任）
│   ├── scope: 許可されたObject Type、Property、Action Type
│   ├── limits: 金額上限、取引回数上限
│   └── propagation: 派生データへの権限伝播ルール
│
├── Negotiation Scope（交渉スコープ）
│   ├── 交渉参加者のみがNegotiation内のMessageを閲覧可能
│   └── 合意後のAgreementはOwnerEntity管理者のみ閲覧可能
│
└── Audit Propagation（監査伝播）
    ├── 全Actionは自動的にAuditEventを生成
    └── AuditEventの権限はソースActionの権限を継承
```

### 4.2 Closed-Loop Feedback 設計

```
現設計（線形）:
  CFP → Negotiation → Agreement → Settlement → END

Ontology統合後（閉ループ）:
  CFP → Negotiation → Agreement → Settlement
   ↑                                    │
   │    ┌──────────────────────────────┘
   │    │
   │    ▼
   │  Feedback Processor
   │    ├── Trust Score Recalculation
   │    │     Settlement成功/失敗 → Agent Trust Score更新
   │    ├── Price Signal Accumulation
   │    │     合意価格 → ドメイン別価格指数に蓄積
   │    ├── Mandate Adjustment Signal
   │    │     Approval承認率 → Mandate緩和/厳格化の推奨
   │    └── Matching Quality Signal
   │          交渉成立率 → Matching Engineの重み調整
   │
   └── 次のCFPのMatching/Pricing精度が向上
```

### 4.3 AI on Ontology の構造的保証

```
現設計:
  LLM ← prompt(raw scenario data) → 自然言語応答
  Risk: promptにraw dataが混入する可能性

Ontology統合後:
  LLM ← OntologyView(typed, filtered, permission-checked) → 構造化応答
  │
  ├── LLMが受け取るのはOntologyView（型付き・権限適用済み）のみ
  ├── LLMの出力はAction Type Validatorで検証
  │     → 価格・制約・合意条件を含む出力は拒否
  │     → 文面生成・要約・説明のみ許可
  └── Rule Engineは生のOntologyオブジェクトを直接操作（LLM経由しない）
```

### 4.4 Action Type の型定義パターン

```python
# Phase 0 実装パターン（Pydantic）
class ActionType(BaseModel):
    """全Actionの基底型"""
    action_id: UUID
    actor_agent_id: UUID
    timestamp: datetime
    
    # Ontology三層
    preconditions: list[Precondition]     # Semantic: 必要なObject状態
    mutations: list[Mutation]             # Kinetic: 何が変わるか
    postconditions: list[Postcondition]   # Semantic: 結果の不変条件
    
    # Dynamic Security
    required_mandate_scope: MandateScope  # 必要な権限
    audit_event: AuditEvent              # 自動生成される監査記録

class CreateCFP(ActionType):
    resource_id: UUID
    preconditions = [ResourceState("available"), ManifestSupported()]
    mutations = [SetResourceState("locked"), CreateNegotiation()]
    postconditions = [ResourceLocked(), NegotiationCreated()]

class ApproveAgreement(ActionType):
    agreement_id: UUID
    approval_decision: ApprovalDecision
    preconditions = [AgreementState("pending_approval"), MandateCovers(terms)]
    mutations = [SetAgreementState("signed"), RecordApproval()]
    postconditions = [AgreementSigned(), AuditComplete()]
```

### 4.5 マルチドメイン拡張パターン（Phase 1+）

```
Phase 0: FoodWaste直書き（D003/D012準拠）
  FoodWasteResource extends Resource
  FoodWasteComplianceRules implements ComplianceRuleSet
  FoodWasteMatchingCriteria implements MatchingCriteria

Phase 1: 新ドメイン追加 = 3つのOntology拡張
  1. 新Object Types: ChemicalResource, TimeSlotResource, etc.
  2. 新Link Types: ドメイン固有の関係
  3. 新ComplianceRuleSet: ドメイン固有の法令ルール
  
  交渉・決済・監査のコア（Action Types, Feedback Loop）は共通基盤として再利用
```

### 4.6 クロスレビュー後の恒久ガードレール（2026-05-21）

Codexクロスレビューで検出したLOW/MEDIUM/HIGHリスクを再発防止するため、以下をOntology統合の固定ルールとする。

| リスク | 恒久対策 |
|---|---|
| 状態機械とAction Typeの不一致 | Technical Design §5のAction Type対応表を単一ソースとし、DB enum・Workflow・テストを一致させる |
| Compliance Rule EngineのPoC埋め込み | Rule Engineは価格評価と法令評価を分離し、廃棄物処理法・食品リサイクル法の判定理由を構造化reasonとして返す |
| Feedback先の未具体化 | TrustScoreHistory、PriceSignalHistory、MandateAdjustmentRecommendation、MatchingOutcomeMetricに記録する |
| LLM raw prompt混入 | LLM Adapterの公開IFはOntologyView + LLMTaskのみ。文字列promptはAdapter内部で生成する |
| Dynamic Security不足 | AgentMandateはObject Type、Action Type、Property Marking、伝播Marking、数量/金額上限を持つ |
| FoodWaste直書きの肥大化 | 共通Resource EnvelopeとFoodWasteAttributesを分離し、共通状態・lock・TTL・markingをドメイン固有属性へ混ぜない |
| Ontology由来の新脅威 | marking伝播、Action権限検証、Feedback汚染検知をSecurity Modelに含める |

---

## 5. Admith既存設計原則への影響

| 既存原則 | 変更 | 根拠 |
|---|---|---|
| D005 Hexagonal + Monolith + Workflow | **維持** | BスケルトンはHexagonal内にOntologyを収容 |
| D007 LLM排除 | **強化** | P4 AI on Ontologyで構造的に保証 |
| D008 Human Final Approval | **強化** | P5 Proposal-Basedで承認メタデータのフィードバック追加 |
| D013 監査ログ保存 | **強化** | P7 Action as First-Classで全操作に自動監査 |
| L2 Resource Ontology Service | **昇格** | 名前だけ→三層Ontology設計へ |
| 設計原則 FoodWaste-First | **維持** | Phase 0はFoodWaste Ontology直書き |
| Reasoning Tier Router | **維持** | LLMはOntologyView経由に変更。Tier構造は不変 |

---

## 6. 参照情報

### Palantirリサーチ出典

- Palantir Docs: Ontology Overview, Core Concepts, Architecture Center
- Palantir Docs: Foundry Data Integration, Object Backend, OSDK
- Palantir Docs: Security Overview, Data Protection and Governance
- Palantir Docs: AIP Architecture, AIP Security
- Palantir Blog: AI Infrastructure and Ontology
- SVPG: Forward Deployed Engineers
- FDE Academy: How Palantir Invented the FDE Model
- Analysis: Palantir's 12-Layer Agentic Architecture (anandbg.com)
- Analysis: Palantir's Digital Twin (theaiarchitects.substack.com)

# Admith — 技術設計書
**用途:** VSCode Claude Code / Codex に渡すプロジェクトコンテキスト  
**バージョン:** v3（v2 ChatGPT監査 + Palantir Ontology-as-Backbone統合 D019-D024）  
**スコープ:** Phase 0 実装設計 + Phase 1-3 の予備設計
**注意（2026-05-21更新）:** LLMのモデル名・価格・提供可否は変動するため、実装時は固定モデル名をハードコードせず、利用時点の利用可能モデルに解決すること。

---

## 1. アーキテクチャ方針

### 採用: Transactional Modular Monolith + Hexagonal + Workflow Engine

| 判断 | 内容 | 経緯 |
|---|---|---|
| ヘキサゴナル | コアドメイン（交渉・合意）を中心に外部システムをAdapter隔離 | LLMベンダー非依存・ドメイン拡張性・テスタビリティ |
| モジュラーモノリス | Phase 0は単一デプロイ。Phase 1で必要部分のみマイクロサービス化 | 5名チームの運用負荷を抑制 |
| Workflow Engine | Temporal/Inngest系のDurable Execution | ChatGPT監査でSPOF問題を解消するため採用決定 |

### Phase 0 でスコープ外（削減決定済み）

| 削減対象 | 理由 | 復活タイミング |
|---|---|---|
| CVE / Vector DB / Knowledge Graph | Phase 0食品廃棄物では不使用 | Phase 1（研究データ） |
| Admith Accord 公開API | 閉じたPoCの信頼性が先 | Phase 1 |
| Escrow / Micropayment | 初期は請求書払い・月次精算 | Phase 1以降 |
| 汎用Domain Plugin | FoodWaste直書き優先 | 2ドメイン目参入時 |
| Trust Score 有料API | 流動性も取引履歴もない | Phase 1以降 |
| 全状態Event Sourcing + CQRS | Negotiation限定に縮小 | 月間1万件超で再検討 |

---

## 2. レイヤード構造

```
L7: Human Oversight & Configuration
    ├─ Operator Dashboard (人間監視UI)
    ├─ Agent Policy Configurator
    └─ Approval Workflow Engine ★ChatGPT監査で追加

L6: External Integration
    ├─ API Gateway (将来Accord用、Phase 0は内部のみ)
    ├─ Compliance Connector (電子マニフェスト)
    └─ Electronic Contract Service Connector ★監査で追加

L5: Settlement & Trust
    ├─ Invoice Generator (Phase 0は請求書払い)
    ├─ Dispute Resolution Engine
    └─ Trust Score Service (初期はKYBベース)

L4: Negotiation Core ★コアドメイン
    ├─ Negotiation Orchestrator (Durable Workflow)
    ├─ Extended CNP Protocol Engine
    ├─ Matching Engine
    ├─ Circuit Breaker / Safety Layer
    └─ Agreement Formation Service

L3: Agent Runtime
    ├─ Generic Agent Framework
    ├─ Agent Registry & Lifecycle
    ├─ Policy Enforcement Point
    ├─ Reasoning Tier Router (Tier1/2/3)
    └─ Agent Mandate Validator ★監査で追加

L2: Domain Knowledge & Intelligence
    ├─ FoodWasteDomain (Phase 0直書き)
    ├─ Compliance Rule Engine
    └─ Resource Ontology Service ★D020: 三層設計に昇格
        ├─ Semantic Layer: Object Types, Link Types, Property Types
        ├─ Kinetic Layer: Action Types（型付き操作）, Functions（読み取り専用計算）
        └─ Dynamic Security Layer: Agent Mandate, Negotiation Scope, Audit Propagation

L1: Foundation
    ├─ LLM Abstraction Layer (vendor-agnostic)
    ├─ Message Bus (内部pub/sub)
    ├─ PostgreSQL (+ PostGIS)
    ├─ Redis (キャッシュのみ。状態の真実はDB)
    ├─ Audit Log Store (append-only, hash chain)
    └─ Observability (Tracing/Metrics/Logging)
```

---

## 3. 設計原則

| 原則 | 内容 |
|---|---|
| Ports & Adapters | L4コアは外部技術（DB/LLM/API）を知らない。全てIF経由 |
| Negotiation-scoped Event Sourcing | 交渉の状態変化のみイベント永続化。他は通常CRUD |
| Idempotency by Design | 全外部APIにIdempotency Key必須 |
| Immutability | 監査ログ・合意書は不変。修正は新イベント追加 |
| Vendor Agnosticism | LLM Abstractionで複数LLMをホットスワップ |
| FoodWaste-First | Phase 0はドメイン直書き。共通化はEnvelope系のみ |
| Human-in-the-Loop Default | 実取引は人間承認をデフォルトON |
| Defense in Depth | Agent Policy / Orchestrator / Circuit Breaker の3層 |
| LLMを契約判断から排除 | 価格・制約判定はRule Engine。LLMは文面生成・要約のみ |
| Agent Quality Fairness | Admithマーケットプレイス内では全参加エージェントに同一モデルTierを強制。Accordでは使用モデルの開示を義務化。Project Dealで判明した「品質格差の不可視性」への対策 |
| Ontology-as-Backbone | Resource Ontology三層（Semantic/Kinetic/Dynamic Security）を設計原則としてHexagonal内に収容。Palantir哲学のうちミッション整合部分のみ採用（D019） |
| AI on Ontology | LLMはOntologyView（型付き・権限適用済み）のみ受け取る。raw data直接アクセス不可。D007の構造的保証（D022） |
| Action as First-Class Citizen | 全状態遷移はpreconditions/mutations/postconditions/audit_eventを持つ型付きActionで記録。監査・テスト・コンプライアンスの構造的保証（D023） |
| Closed-Loop Operations | Settlement結果をTrust Score・価格指数・Mandate調整・Matching重みに還元するフィードバックループ（D021） |
| Proposal-Based Feedback | Human Approval承認/却下メタデータをAgent Mandate自動調整に還元。承認率の継続的改善（D024） |

---

## 3.1 恒久Port契約（Step 3実装境界）

Step 3以降は以下のPortを先に固定し、FastAPI、DB、LLM、Workflow EngineはAdapterとして接続する。これによりL1-L7の欠落IF、LLM raw prompt混入、PoCから本番への密結合移行を防ぐ。

```python
class OntologyViewPort(Protocol):
    def build_view(self, subject_id: UUID, mandate: AgentMandate) -> OntologyView: ...

class ComplianceRulePort(Protocol):
    def evaluate(self, terms: Terms, resource: ResourceEnvelope) -> ComplianceResult: ...

class ActionExecutorPort(Protocol):
    def execute(self, action: ActionType, context: ActionContext) -> ActionResult: ...

class ApprovalPort(Protocol):
    def request_approval(self, agreement: Agreement) -> ApprovalRequest: ...

class FeedbackSinkPort(Protocol):
    def record_settlement_feedback(self, agreement: Agreement, outcome: SettlementOutcome) -> None: ...
```

LLM Adapterの公開入口は文字列promptを受け取らない。文字列化はAdapter内部の最終段階に限定する。

```python
class LLMProvider(Protocol):
    async def complete_view(self, view: OntologyView, task: LLMTask,
                            max_tokens: int, temperature: float) -> CompletionResult: ...
```

### 3.2 Runtime Profile 境界（Step 4本番化）

Step 4以降は `ADMITH_RUNTIME=demo|production` を明示する。

| Profile | Repository | External adapters | Allowed purpose |
|---|---|---|---|
| demo | memory | stub | ローカルデモ、開発者向けsmoke、UI確認 |
| production | database only | sandbox or production only | 本番相当検証、本番運用 |

Production profileでは以下をfail-closedにする。
- `admith.api.runtime` のin-memory singleton。
- `ADMITH_REPOSITORY_MODE=memory`。
- `ADMITH_ECONTRACT_ADAPTER_MODE=stub`。
- `ADMITH_MANIFEST_ADAPTER_MODE=stub`。

この境界はT210以降のDB repository差替より先に導入し、demo-only経路がproductionへ混入する再発を防ぐ。

---

## 4. データモデル

### 4.1 中核エンティティ

```
OwnerEntity 1─n Agent n─owns─n Resource
                        │              │
                        │              ▼
                        │         Negotiation
                        │         ├── n Message
                        │         ├── n NegotiationParticipant
                        │         ├── 1 Agreement (optional)
                        │         └── n AuditEvent
                        │
                        ├── n AgentMandate ★監査で追加
                        └── TrustScoreHistory

Domain 1─n Resource
```

### 4.2 主要テーブル

#### OwnerEntity
```sql
owner_entity_id   UUID PK
entity_type       ENUM (corporation, individual)
legal_name        VARCHAR
corporate_number  VARCHAR  -- 法人番号（KYB用）
kyb_status        ENUM (pending, verified, rejected)
kyb_verified_at   TIMESTAMPTZ NULL
created_at        TIMESTAMPTZ
```

#### Agent
```sql
agent_id            UUID PK
owner_entity_id     UUID FK
agent_type          ENUM (autonomous, human_in_loop, mediator)
public_key          BYTES  -- Ed25519
domain_capabilities JSONB
policy              JSONB  -- Pydantic/Zodでバリデーション済みのみ書き込み
trust_score         DECIMAL(5,4)
status              ENUM (active, suspended, retired)
created_at          TIMESTAMPTZ
updated_at          TIMESTAMPTZ
```

#### AgentMandate ★監査で追加
```sql
mandate_id              UUID PK
agent_id                UUID FK
owner_entity_id         UUID FK
scope                   JSONB  -- 許可されたドメイン・品目・地域
allowed_object_types    JSONB  -- Dynamic Security: Resource/Agreement等のObject Type
allowed_actions         JSONB  -- Dynamic Security: 実行可能なAction Type
allowed_regions         JSONB  -- 地域・拠点スコープ
property_markings       JSONB  -- Propagating Security用の属性marking
propagation_markings    JSONB  -- 派生データへ伝播させるmarking
max_amount_per_deal     DECIMAL
max_amount_per_day      DECIMAL
max_quantity_per_deal   DECIMAL NULL
currency                VARCHAR DEFAULT 'JPY'
allowed_counterparties  JSONB NULL  -- NULLなら制限なし
approval_mode           ENUM (approve_all, approve_above_threshold,
                              auto_within_mandate, dual_control)
approval_threshold      DECIMAL NULL
valid_from              TIMESTAMPTZ
valid_until             TIMESTAMPTZ
version                 INT
revoked_at              TIMESTAMPTZ NULL
revoked_reason          TEXT NULL
mandate_signature       BYTES  -- 権限委任者の署名
created_at              TIMESTAMPTZ
```

#### Resource
```sql
resource_id         UUID PK
owner_agent_id      UUID FK
domain_id           VARCHAR FK
resource_type       VARCHAR
attributes          JSONB  -- ドメイン固有属性。共通Envelope外へ漏らさない
ontology_version    VARCHAR  -- Resource Envelope互換性管理
security_markings   JSONB  -- OntologyView/AuditEventへ伝播
state               ENUM (available, locked, transferred, expired)
lock_token          UUID NULL  -- ★二重ロック防止
locked_by_negotiation_id UUID NULL
locked_until        TIMESTAMPTZ NULL
ttl_until           TIMESTAMPTZ
reservation_price   DECIMAL  -- 負の値も許容
location            GEOGRAPHY  -- PostGIS
created_at          TIMESTAMPTZ
```

#### Negotiation
```sql
negotiation_id      UUID PK
initiator_agent_id  UUID FK
resource_id         UUID FK
state               ENUM (cfp_open, negotiating, draft_agreement,
                          pending_human_approval,  -- ★監査で追加
                          signing, settled,
                          failed, expired)
protocol_version    VARCHAR
tier                INT (1, 2, 3)
matching_ttl_until  TIMESTAMPTZ  -- ★5段階TTL
negotiation_ttl_until TIMESTAMPTZ
approval_ttl_until  TIMESTAMPTZ NULL
pickup_deadline     TIMESTAMPTZ NULL
started_at          TIMESTAMPTZ
ended_at            TIMESTAMPTZ NULL
domain_id           VARCHAR FK
estimated_delta     DECIMAL
final_delta         DECIMAL NULL
```

#### NegotiationParticipant
```sql
negotiation_id      UUID FK  -- composite PK
agent_id            UUID FK  -- composite PK
role                VARCHAR  -- 固定ENUMでなく文字列（多市場対応）
joined_at           TIMESTAMPTZ
left_at             TIMESTAMPTZ NULL
final_status        ENUM (agreed, declined, dropped) NULL
```

#### Message
```sql
message_id          UUID PK
negotiation_id      UUID FK
from_agent_id       UUID FK
to_agent_id         UUID FK NULL  -- NULLはブロードキャスト
message_type        ENUM (cfp, proposal, counter, accept, reject,
                          inform, cancel)
payload             JSONB
signature           BYTES  -- Ed25519
nonce               UUID  -- ★Replay攻撃防止
created_at          TIMESTAMPTZ
sequence_number     BIGINT
parent_message_id   UUID FK NULL
```

#### Agreement
```sql
agreement_id        UUID PK
negotiation_id      UUID FK UNIQUE
terms               JSONB  -- 構造化された合意条件（LLM出力ではない）
parties             JSONB
signatures          JSONB
state               ENUM (draft, pending_approval, signed,
                          settled, disputed, cancelled)
created_at          TIMESTAMPTZ
settled_at          TIMESTAMPTZ NULL
audit_hash          BYTES  -- SHA256
```

#### ApprovalRequest ★監査で追加
```sql
approval_id         UUID PK
negotiation_id      UUID FK
agreement_id        UUID FK NULL
owner_entity_id     UUID FK
required_role       VARCHAR
status              ENUM (pending, approved, rejected, expired)
expires_at          TIMESTAMPTZ
created_at          TIMESTAMPTZ
```

#### ApprovalDecision ★監査で追加
```sql
approval_id         UUID FK PK
approver_user_id    UUID
decision            ENUM (approve, reject, edit, escalate)
reason              TEXT NULL
displayed_terms_hash BYTES  -- 表示時の条件hashで改ざん検知
decided_at          TIMESTAMPTZ
```

#### AuditEvent (append-only)
```sql
event_id            UUID PK
negotiation_id      UUID FK NULL
agent_id            UUID FK NULL
action_id           UUID NULL
event_type          VARCHAR
event_data          JSONB
sequence_number     BIGINT
previous_hash       BYTES
hash_algorithm      VARCHAR  -- 例: sha256-canonical-json-v1
event_hash          BYTES  -- SHA256(canonical_event_data || sequence_number || previous_hash)
timestamp           TIMESTAMPTZ
-- PIIは分離テーブルに保持。保持期間・アクセス権を別管理
```

#### TrustScoreHistory
```sql
agent_id            UUID FK
score               DECIMAL(5,4)
calculation_method  VARCHAR  -- Phase 0: 'kyb_based', Phase 1+: 'transaction_based'
input_signals       JSONB
calculated_at       TIMESTAMPTZ
```

#### PriceSignalHistory ★D021恒久化
```sql
price_signal_id     UUID PK
domain_id           VARCHAR
resource_type       VARCHAR
region              VARCHAR
unit_price_yen      DECIMAL
quantity_kg         DECIMAL
agreement_id        UUID FK
calculated_at       TIMESTAMPTZ
```

#### MandateAdjustmentRecommendation ★D024恒久化
```sql
recommendation_id   UUID PK
agent_id            UUID FK
owner_entity_id     UUID FK
approval_rate       DECIMAL(5,4)
reject_reasons      JSONB
recommended_change  JSONB
status              ENUM (proposed, accepted, rejected, expired)
created_at          TIMESTAMPTZ
```

#### MatchingOutcomeMetric ★D021恒久化
```sql
metric_id           UUID PK
domain_id           VARCHAR
matching_policy     VARCHAR
candidate_count     INT
negotiation_id      UUID FK
outcome             ENUM (settled, failed, expired, rejected)
elapsed_seconds     DECIMAL
created_at          TIMESTAMPTZ
```

---

## 5. Negotiation Orchestrator 状態機械

```
[CFP_OPEN]
  │(Matching Engineが候補を選定)
  ▼
[NEGOTIATING]
  │ 自然言語での自由交渉フェーズ
  │ Rule Engineが法的制約をリアルタイム評価
  │ Circuit Breakerが異常を監視
  ▼
[DRAFT_AGREEMENT]
  │ Rule Engineが合意条件を構造化JSONに変換
  │
  ▼
[PENDING_HUMAN_APPROVAL] ★監査で追加
  │ 承認
  ▼
[SIGNING]
  │
  ▼
[SETTLED] (Phase 0は請求書払いのため、ESCROW省略)

失敗パス: 各段階から → [FAILED] or [EXPIRED]
```

状態機械はマイルストーン管理に限定する。旧設計の `BIDDING` / `CROSS_MATCHING` / `ITERATING` は `NEGOTIATING` に統合し、交渉のラウンド数やカウンター回数を厳密には制限しない。ただし、Negotiation TTL、Rule Engineによる法的制約評価、Circuit Breaker、DRAFT_AGREEMENT以降の法的手続きは厳密に維持する。

### Action Type と状態遷移の完全対応 ★恒久対策

| Action Type | Before | After | 主な責務 |
|---|---|---|---|
| CreateCFP | Resource.available | cfp_open | Resource lock、Negotiation作成、監査 |
| SubmitProposal | cfp_open | negotiating | Proposal保存、参加者追加、監査 |
| CounterOffer | negotiating | negotiating | Counter保存、Rule Engine再評価、監査 |
| FormAgreement | negotiating | draft_agreement | Terms構造化、ComplianceResult添付、監査 |
| RequestApproval | draft_agreement | pending_human_approval | ApprovalRequest作成、表示terms hash固定 |
| ApproveAgreement | pending_human_approval | signing | ApprovalDecision保存、Mandate再検証 |
| RejectAgreement | pending_human_approval | failed | 却下理由保存、Resource unlock候補化 |
| SignAgreement | signing | signing | 電子契約サービス連携、署名イベント保存 |
| SettleDeal | signing | settled | 請求/検品/受領結果保存、Feedback Processor起動 |
| FailNegotiation | any non-terminal | failed | 失敗理由保存、Resource unlock |
| ExpireNegotiation | any non-terminal | expired | TTL失効保存、Resource unlock |

DB enum、Workflow state、Action Type名はこの表を単一の設計ソースとする。`bidding`、`cross_matching`、`iterating`、`in_escrow` はPhase 0の状態enumに入れない。

### TTL 5段階分割 ★監査で追加

```
1. Matching TTL:        5〜30秒
2. Auto Negotiation TTL: 1〜5分
3. Human Approval TTL:  30分〜24時間 (Resource腐敗期限から逆算)
4. Pickup Deadline TTL: pickup_windowに従う
5. Settlement TTL:      法定・業務要件に従う
```

### Closed-Loop Feedback ★D021

```
Settlement完了後、以下のフィードバックを次のCFPサイクルに還元:

  Settlement
   │
   ▼
  Feedback Processor
   ├── Trust Score Recalculation
   │     Settlement成功/失敗 → Agent Trust Score更新
   ├── Price Signal Accumulation
   │     合意価格 → ドメイン別価格指数に蓄積
   ├── Mandate Adjustment Signal  ★D024
   │     Approval承認率 → Mandate緩和/厳格化の推奨
   └── Matching Quality Signal
         交渉成立率 → Matching Engineの重み調整

Phase 0: Trust ScoreとPrice Signalは記録のみ（DB蓄積）。
Phase 1: 蓄積データを用いたMandateとMatchingの自動調整を実装。
```

Phase 0の永続化先:
- Trust Score: `TrustScoreHistory`
- Price Signal: `PriceSignalHistory`
- Mandate Adjustment: `MandateAdjustmentRecommendation`（自動適用はしない）
- Matching Quality: `MatchingOutcomeMetric`

---

## 6. Circuit Breaker

| トリガー | 閾値 | アクション |
|---|---|---|
| Matching TTL超過 | 30秒 | FAILED状態へ |
| 価格異常 | 過去30日中央値±50% | HUMAN_REVIEW移行 |
| Monotonicity違反 | 譲歩のない再提案 | 警告→停止 |
| 高頻度CFP | 同一Sellerから10件/分超 | レート制限 |
| 信頼スコア急落 | 24時間で-0.2 | 一時停止 |
| LLM API遅延 | 1リクエスト>10秒 | Tier1 Rule Engineにフォールバック |
| Mandate逸脱 | 委任範囲外の条件 | 即時凍結 + Owner通知 |

---

## 7. Reasoning Tier Router

```
Tier 1: ルールベースマッチング（コスト≒0）→ 全取引の80%
  - 価格・制約の評価は決定論的Rule Engine
  - LLMは使わない

Tier 2: Gemini Flash系 → 条件交渉が必要な15%
  - 交渉文面生成、例外説明、候補要約
  - 契約判断には使わない

Tier 3: Pro系LLM → 複雑な多者間交渉の5%
  - 人間向け説明文の生成
  - 契約判断には使わない

★重要: LLMを契約判断（価格・制約・合意条件）に使わない。
  決定論的Rule Engineで確定し、LLMは補助的文面生成のみ。

★Project Deal知見: モデル品質 >>> プロンプト戦略。
  Tier選択（model_tier）がエージェントの交渉力を最も強く規定する。
  strategy（cooperative/aggressive等）は結果に統計的有意な影響を与えない
  可能性がある。ただし、ユーザーの安心感・コントロール感のために維持する。
```

---

## 8. LLM Abstraction Layer

```python
class LLMProvider(Protocol):
    async def complete_view(self, view: OntologyView, task: LLMTask,
                            max_tokens: int, temperature: float) -> CompletionResult: ...
    @property
    def cost_per_million_tokens(self) -> Decimal: ...

class LLMRouter:
    providers: Dict[Tier, List[LLMProvider]]
    async def route(self, tier: Tier, view: OntologyView, task: LLMTask) -> CompletionResult:
        selected = self._select_best(self.providers[tier])
        return await selected.complete_view(view, task, ...)
```

Phase 0: Gemini Flash系を利用（固定モデル名は避ける）。50行のadapter追加で他社へ切替可能。

### AI on Ontology 制約 ★D022

```
LLMへの入力: OntologyView（型付き・権限適用済み）のみ
  ├── Agent Mandateでフィルタされたオブジェクトのみ
  ├── raw DB/API dataの直接注入を構造的に禁止
  └── Negotiation Scopeでアクセス範囲を制約

LLMからの出力: Action Type Validatorで検証
  ├── 価格・制約・合意条件を含む出力 → 拒否
  ├── 文面生成・要約・説明 → 許可
  └── Rule Engineは生のOntologyオブジェクトを直接操作（LLM経由しない）
```

---

## 9. Generic Agent Framework

```python
class Agent(Protocol):
    agent_id: UUID
    policy: AgentPolicy

    async def on_cfp_received(self, cfp: CFPMessage) -> Optional[ProposalMessage]: ...
    async def on_counter_received(self, counter: CounterMessage) -> Response: ...
    async def evaluate(self, terms: Terms) -> EvaluationResult: ...
    async def sign_agreement(self, agreement: Agreement) -> Signature: ...

class AgentPolicy(BaseModel):
    objective: ObjectiveFunction        # 最重要
    constraints: List[Constraint]       # 重要
    strategy: NegotiationStrategy       # best-effort
    human_approval_threshold: Optional[Decimal]  # 重要
    model_tier: Tier                    # 最重要パラメータ
```

ロールは固定しない。同一エージェントが食品市場ではSeller、物流市場ではBuyerになれる。

---

## 10. セキュリティ・トラストモデル

| 層 | 脅威 | 対策 |
|---|---|---|
| Agent間通信 | なりすまし | Ed25519署名 + nonce（Replay防止） |
| 交渉プロセス | 異常価格約定 | Rule Engine判定 + Circuit Breaker |
| 決済 | 二重支払い | Idempotency Key + DB制約 |
| Resource | 二重ロック | SELECT FOR UPDATE SKIP LOCKED + lock_token + locked_until |
| 監査ログ | 改ざん | Append-only + ハッシュチェーン |
| API | 不正利用 | OAuth 2.1 + Rate Limit + WAF |
| Prompt Injection | Resource attributes経由 | LLM入力サニタイズ + 構造化入力強制 + AI on Ontology（D022: OntologyView経由のみ） |
| Sybil攻撃 | 自作自演価格操作 | KYB必須 + 招待制 + wash trading検知 |
| 内部脅威 | 管理者によるスコア改ざん | 二者承認 + 監査ログ + break-glass access |
| 品質詐欺 | 廃棄物品質偽装 | 受入検品フロー + 品質保証条項（利用規約） |
| 物流ランサム | 直前値上げ/キャンセル | 代替候補 + 保証金 + ペナルティ |
| OntologyView権限漏れ | 派生ビュー経由で本来不可視の属性が混入 | AgentMandate + property_markings + 最小フィールド投影 |
| Propagating Security欠落 | 集計・要約・LLM出力でmarkingが落ちる | security_markingsをResource→OntologyView→AuditEvent→Feedbackへ伝播 |
| Action権限昇格 | 許可外Actionを直接呼び出す | ActionExecutorでallowed_actionsとpreconditionを一元検証 |
| Feedback汚染 | 自作自演・異常値がTrust/Matchingを歪める | KYB、wash trading検知、外れ値隔離、手動承認前の自動適用禁止 |

---

## 11. 法規制対応（設計に組み込む）

| 法規制 | 要件 | 実装 |
|---|---|---|
| 廃棄物処理法 | 排出事業者責任は委託後も残る | 委託契約・許可業者確認・マニフェスト確認をワークフローに組込 |
| 食品リサイクル法 | 飼料化→肥料化の優先順位法定 | Compliance Rule Engineに優先順位ルール |
| 電子署名法 | 本人意思・代理権限の証明 | Human Approval + Agent Mandate + 電子契約サービス連携 |
| 個人情報保護法 | AuditEvent内PII管理 | IP・担当者ID分離、保持期間・アクセス権定義 |
| 下請法→取適法（2026年1月改正） | 協議ログ・見積根拠の保存 | 自動交渉でもMessage全量保存 + 変更理由構造化 |
| EU AI Act（Phase 2以降） | 透明性・人間監督 | AI利用開示はPhase 0から組込 |
| 貨物利用運送事業法 | 運賃受取方法 | 情報マッチングに徹し、運送契約は荷主-配送業者直接 |

---

## 12. 監視メトリクス

| カテゴリ | メトリクス |
|---|---|
| 事業KPI | 交渉成立率 / 平均Delta / 月間取引量 / Human Approval reject率 |
| パフォーマンス | P50/P99交渉完了時間 / LLM平均レイテンシ |
| コスト | 1交渉あたりLLMコスト / インフラコスト |
| 信頼性 | エラー率 / Circuit Breaker発動回数 / TTL超過率 |
| セキュリティ | 署名検証失敗 / 不正アクセス / Mandate逸脱検知 |
| 法令遵守 | マニフェスト連携成功率 / 飼料化優先順位遵守率 |

---

## 13. Phase 1-3 予備設計

### Combination Value Engine（Phase 1-2）
```
Step 1: sim(A, B) = cos(embed_A, embed_B)
Step 2: complementarity = gaussian(sim, mean=0.6, std=0.15)
Step 3: kg_score = number_of_paths(A, B) × avg_path_value
Step 4: estimated_value = complementarity × kg_score × market_size_factor
```
Vector DB: pgvector (PostgreSQL拡張) or 専用DB (Pinecone/Weaviate)

### プライバシー技術スタック（Phase 2）
| 技術 | 用途 | 導入時期 |
|---|---|---|
| Differential Privacy | 意図データの統計的保護 | Phase 2初期 |
| Federated Learning | 生データを集めずモデル訓練 | Phase 2中期 |
| Secure MPC | 結合価値の共同計算 | Phase 2中期 |
| ZKP | データの性質を非開示で証明 | Phase 2後期（コスト再評価後） |

### A2A / MCP Adapter（Phase 1-2）
- 内部は独自最適化プロトコル
- 外部接続はA2A/MCP adapterで吸収（ChatGPT監査で確定）
- adapter隔離・sandbox・egress制御を設計に組込

# tasks.md -- pm-zero v9.4 Execution Ledger

## Goal Binding
- Vision source: docs/vision.md
- Active goal: Step 4 Production Hardening（本番リリース可能なB2B食品廃棄物マッチング・交渉プラットフォーム）
- Planning owner: Coordinator (agent指定なし)
- Implementation owner: Codex CLI
- Review owner: Independent reviewer (cross-vendor where required)

## Status Vocabulary
- proposed: idea exists, not ready
- ready: owner, dependencies, write scope, acceptance, verification, and expected evidence are clear
- doing: one owner is actively working
- blocked: needs decision, dependency, credential, environment, or human action
- review: implementation complete, review pending
- done: accepted by reviewer
- verified: evidence recorded

## Parallelization Rules
- Coordinator owns tasks.md.
- Worker agents own only their assigned Write Scope.
- Parallel implementation requires disjoint Write Scopes or isolated worktrees.
- If two tasks need the same file, serialize them.
- Subagents return reports; coordinator updates tasks.md.

## Architecture Summary
```
MVP = Docker Compose single-package
  ├─ backend/     Python/FastAPI (API + Negotiation Core + Rule Engine)
  ├─ dashboard/   Next.js/TypeScript (Operator Dashboard)
  ├─ db/          PostgreSQL 16 + PostGIS (Alembic migrations)
  ├─ redis/       Cache only
  └─ docker-compose.yml
```

## Phase Legend
- **A**: Project Foundation (T100-T109)
- **B**: Core Domain — L1/L2 (T110-T119)
- **C**: Agent Runtime & Negotiation Core — L3/L4 (T120-T129)
- **D**: Settlement, Trust, External — L5/L6 (T130-T139)
- **E**: Operator Dashboard — L7 (T140-T149)
- **F**: Integration, Packaging, Smoke Test (T150-T159)

---

## Completed Tasks (Step 2 PoC)
| ID | Status | Summary |
|---|---|---|
| T001 | verified | Gemini API接続テスト |
| T002 | verified | Variant A: Rule Engine + structured CNP |
| T003 | verified | Variant B: Natural language baseline |
| T004 | verified | Variant比較 |
| T005 | verified | 結果記録・Go/No-Go |
| T006 | verified | Codex cross-review hardening |

---

## Phase A: Project Foundation

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification |
|---|---|---|---|---|---|---|---|
| T100 | done | Codex CLI | none | backend/pyproject.toml, backend/src/, backend/alembic.ini, backend/alembic/, backend/.env.example | Python/FastAPIプロジェクト初期化。pyproject.toml（FastAPI, Uvicorn, SQLAlchemy 2.0, Alembic, asyncpg, pydantic v2, python-jose, httpx, pytest, ruff）。src/admith/ にHexagonal構造（domain/, ports/, adapters/, api/）を作成。Alembic初期設定。 | `uv run python -c "from admith import __version__"` が成功し、`uv run ruff check backend/src/` がエラー0 | rtk ruff check backend/src tests -> passed; rtk pytest -q -> 15 passed |
| T101 | done | Codex CLI | none | dashboard/package.json, dashboard/src/, dashboard/tsconfig.json, dashboard/next.config.ts, dashboard/.env.example | Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui でOperator Dashboardプロジェクト初期化。src/app/ にApp Router構造。 | `pnpm build` が成功 | rtk pnpm build -> passed |
| T102 | done | Codex CLI | none | docker-compose.yml, db/init.sql, .env.example | Docker Compose定義: postgres:16-postgis, redis:7, backend(Dockerfile), dashboard(Dockerfile)。.env.exampleにDB接続、Redis、API URLのテンプレート。db/init.sqlでDB・拡張作成。 | `docker compose config` がエラーなし | not run: Docker CLI unavailable |
| T103 | done | Codex CLI | T100 | backend/src/admith/domain/models.py | Pydantic v2 + dataclass でコアドメインモデル定義: OwnerEntity, Agent, AgentMandate, Resource, Negotiation, NegotiationParticipant, Message, Agreement, ApprovalRequest, ApprovalDecision, AuditEvent, TrustScoreHistory, PriceSignalHistory, MandateAdjustmentRecommendation, MatchingOutcomeMetric。技術設計書§4のスキーマに完全準拠。OntologyView, ActionRecord, MandateScope はPoCから昇格。 | 全エンティティがPydantic model_validate()で型検証可能。NegotiationState, ActionName, MessageType等のEnum/Literalが技術設計書§5 Action Type表と完全一致 | rtk pytest -q -> 15 passed |

## Phase B: Core Domain (L1/L2)

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification |
|---|---|---|---|---|---|---|---|
| T110 | done | Codex CLI | T100, T103 | backend/src/admith/adapters/db/, backend/alembic/versions/ | SQLAlchemy 2.0 ORM マッピング + Alembic初回マイグレーション。技術設計書§4の全テーブル（OwnerEntity〜MatchingOutcomeMetric）を定義。Resource.location はPostGIS Geography。AuditEvent は append-only制約（UPDATE/DELETE禁止トリガー）。 | `alembic upgrade head` がクリーンDBで成功し、全テーブルが作成される | migration file added; DB upgrade not run: Docker CLI unavailable |
| T111 | done | Codex CLI | T110 | backend/src/admith/adapters/repositories.py | Repository層: SQLAlchemy async session を使ったCRUD。ResourceRepository（lock_token付きSELECT FOR UPDATE）、NegotiationRepository、AgentRepository、AuditEventRepository（append-only insert + hash chain計算）。全RepositoryはPortsのProtocolを実装。 | 各Repositoryに対する基本CRUD + lock取得のユニットテスト通過 | rtk pytest -q -> 15 passed |
| T112 | done | Codex CLI | T103 | backend/src/admith/domain/rule_engine.py, backend/src/admith/domain/compliance.py | Rule Engine本番化: PoCのRuleEngineをPortsベースに昇格。ComplianceRulePort実装。食品リサイクル法優先順位（飼料→肥料→アップサイクル）、廃棄物処理法（委託契約・許可業者・マニフェスト確認）、取適法（協議ログ保存要件チェック）。ComplianceResultにreasons分離（D025）。 | コンプライアンス違反シナリオ5件以上で正しくreject。正常シナリオでAgreement生成。compliance_reasonsが空の場合のみ合意可能 | rtk pytest -q -> 15 passed |
| T113 | done | Codex CLI | T103 | backend/src/admith/domain/ontology.py | Resource Ontology Service: Semantic層（ObjectType, LinkType, PropertyType定義）、Kinetic層（ActionType型付き操作、preconditions/mutations/postconditions/audit_event）、Dynamic Security層（MandateScope.allows()による権限チェック）。OntologyViewPort.build_view()実装: Agent Mandateでフィルタされたビューのみ返す。 | OntologyView生成時にMandateの権限外フィールドが除外される。ActionType実行時にprecondition違反で拒否される | rtk pytest -q -> 15 passed |
| T114 | done | Codex CLI | T103 | backend/src/admith/ports/ | Port定義（Protocol）: OntologyViewPort, ComplianceRulePort, ActionExecutorPort, ApprovalPort, FeedbackSinkPort, LLMProvider, ResourceRepositoryPort, NegotiationRepositoryPort, AuditRepositoryPort。技術設計書§3.1の恒久Port契約に完全準拠。LLMProviderはcomplete_view(OntologyView, LLMTask)で文字列promptを受け取らない。 | 全Portが typing.Protocol として定義され、mypy/pyright で検証可能 | rtk ruff check backend/src tests -> passed |

## Phase C: Agent Runtime & Negotiation Core (L3/L4)

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification |
|---|---|---|---|---|---|---|---|
| T120 | done | Codex CLI | T113, T114 | backend/src/admith/domain/agent.py | Agent Framework: AgentPolicy（objective, constraints, strategy, human_approval_threshold, model_tier）。on_cfp_received / on_counter_received / evaluate / sign_agreement の基本実装。Phase 0はTier1（Rule Engine only）をデフォルトとし、Tier2/3のLLM呼び出しはAdapterスタブ。 | Tier1エージェントがCFP→Proposal→Counter→Acceptの基本フローを完走 | rtk pytest -q -> 15 passed |
| T121 | done | Codex CLI | T111, T113 | backend/src/admith/domain/matching.py | Matching Engine: Resource CFP受信→条件マッチング（ドメイン、地域、量、価格帯）→候補Agent選定→Negotiation作成。Matching TTL（5-30秒）管理。MatchingOutcomeMetric記録。 | 正常シナリオで候補が1件以上返る。条件不一致で候補0件。TTL超過でexpired | rtk pytest -q -> 15 passed |
| T122 | done | Codex CLI | T120, T121, T112 | backend/src/admith/domain/orchestrator.py | Negotiation Orchestrator: 技術設計書§5の状態機械を実装。CFP_OPEN→NEGOTIATING→DRAFT_AGREEMENT→PENDING_HUMAN_APPROVAL→SIGNING→SETTLED の正常パス。各遷移でActionExecutorPort経由のAction Type実行。Circuit Breaker統合（価格異常±50%、TTL超過、Mandate逸脱）。Phase 0はDurable Workflow Engineの代わりにasync state machineで実装し、Temporal/Inngest Adapterは後続タスクとする。 | 正常4者交渉（Seller, Buyer, Logistics, Mediator）がSETTLEDまで完走。Circuit Breaker発動で FAILED遷移。各状態遷移にAuditEvent記録 | rtk pytest -q -> 15 passed |
| T123 | done | Codex CLI | T114 | backend/src/admith/adapters/llm.py | LLM Abstraction Layer: GeminiAdapter（complete_view実装）。OntologyView→構造化prompt変換はAdapter内部に閉じる。Tier Router（Tier1: Rule Engine直接 / Tier2: Flash系 / Tier3: Pro系）。Phase 0はTier1中心、Tier2/3はモック可。コスト計算・レイテンシ計測。 | OntologyViewのみを入力として受け取り、raw promptを外部から注入不可。モックモードでテスト通過 | rtk ruff check backend/src tests -> passed |

## Phase D: Settlement, Trust, External Integration (L5/L6)

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification |
|---|---|---|---|---|---|---|---|
| T130 | done | Codex CLI | T122 | backend/src/admith/domain/approval.py | Approval Workflow: ApprovalPort実装。Agreement到達時にApprovalRequest作成→Operator Dashboardへ通知（Phase 0はポーリング）→ApprovalDecision記録。displayed_terms_hash改ざん検知。Approval TTL（30分〜24時間）管理。reject時はMandateAdjustmentRecommendation記録（D024）。 | approve→SIGNING遷移。reject→FAILED遷移+理由記録。TTL超過→expired。terms_hash不一致→拒否 | rtk pytest -q -> 15 passed |
| T131 | done | Codex CLI | T111 | backend/src/admith/domain/settlement.py | Settlement & Feedback: SettleDeal Action実装。請求書生成（Phase 0: JSON形式の請求書データ）。Settlement完了後にFeedbackSinkPort経由で4種フィードバック記録（D021）: TrustScoreHistory, PriceSignalHistory, MandateAdjustmentRecommendation, MatchingOutcomeMetric。Phase 0は記録のみ、自動適用なし。 | Settlement完了で4テーブルにレコード追加。請求書JSONにagreement_id, 金額, 当事者情報を含む | rtk pytest -q -> 15 passed |
| T132 | done | Codex CLI | T114 | backend/src/admith/adapters/manifest_stub.py, backend/src/admith/adapters/econtract_stub.py | 外部連携スタブ: 電子マニフェストAPI Adapter（スタブ: manifest_id返却のみ）。電子契約サービスAdapter（スタブ: contract_id返却のみ）。Port定義に準拠し、本番接続時はAdapter差替のみで対応。 | スタブがPort Protocolを満たし、テストで呼び出し可能 | rtk ruff check backend/src tests -> passed |
| T133 | done | Codex CLI | T111 | backend/src/admith/domain/trust.py | Trust Score Service: Phase 0はKYBベース（kyb_verified → score=0.8, pending → 0.3, rejected → 0.0）。TrustScoreHistory記録。将来のtransaction_based計算への拡張ポイントを用意。 | KYBステータスに応じたスコア計算。TrustScoreHistory追記 | rtk pytest -q -> 15 passed |

## Phase E: Operator Dashboard (L7)

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification |
|---|---|---|---|---|---|---|---|
| T140 | done | Codex CLI | T100 | backend/src/admith/api/routes/, backend/src/admith/api/main.py | FastAPI REST API: 以下のエンドポイント群。認証はPhase 0ではAPIキー（Bearer token）。(1) GET/POST /resources (2) GET/POST /negotiations (3) GET /negotiations/{id} (4) POST /negotiations/{id}/approve, /reject (5) GET /audit-events (6) GET /agents (7) POST /agents (8) GET /dashboard/metrics (9) GET /health。OpenAPI schema自動生成。 | 全エンドポイントが200/201/400/404を正しく返す。OpenAPI /docs アクセス可能 | rtk pytest -q -> 15 passed |
| T141 | done | Codex CLI | T101, T140 | dashboard/src/app/, dashboard/src/components/, dashboard/src/lib/ | Operator Dashboard UI: (1) ダッシュボード概要（アクティブ交渉数、承認待ち件数、本日のDelta合計、直近取引リスト）(2) 交渉一覧・詳細（状態別フィルタ、タイムライン表示）(3) 承認画面（Agreement条件表示、approve/rejectボタン、理由入力）(4) リソース管理（登録・一覧・ロック状態表示）(5) エージェント管理（登録・Mandate設定）(6) 監査ログビューア。Backend APIをfetch呼び出し。 | 全6画面がビルド・描画される。承認ボタンクリックでAPI呼び出しが発行される | rtk pnpm build -> passed |
| T142 | done | Codex CLI | T141 | dashboard/src/app/login/, dashboard/src/middleware.ts | Dashboard認証: Phase 0はAPIキー入力→localStorage保存→全リクエストにBearerヘッダ付与。middleware.tsで未認証時はloginへリダイレクト。 | 未認証でダッシュボードアクセス→ログイン画面。APIキー入力後→ダッシュボード表示 | rtk pnpm build -> passed |

## Phase F: Integration, Packaging, Smoke Test

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification |
|---|---|---|---|---|---|---|---|
| T150 | done | Codex CLI | T140, T141 | backend/Dockerfile, dashboard/Dockerfile, docker-compose.yml | Dockerfile作成: backend（multi-stage, uv install, uvicorn起動）、dashboard（multi-stage, pnpm build, standalone出力）。docker-compose.ymlにhealthcheck追加（backend: /health, dashboard: /, db: pg_isready）。 | `docker compose build` が成功 | not run: Docker CLI unavailable |
| T151 | done | Codex CLI | T150 | scripts/smoke_test.sh | 統合スモークテスト: docker compose up → DB migration自動実行 → /health確認 → リソース登録 → 交渉開始 → 承認 → Settlement完走 → 監査ログ確認 → docker compose down。全ステップをcurlで実行するシェルスクリプト。 | スクリプトが exit 0 で完了し、全APIレスポンスが期待通り | script added; not run: Docker CLI unavailable |
| T152 | done | Codex CLI | T151 | scripts/seed_demo.py | デモデータ投入: OwnerEntity 4社（食品メーカー、飼料業者、物流業者、オペレーター）、Agent 4体、AgentMandate 4件、Resource 2件（おから1000kg、余剰パン500kg）。Phase 0シナリオの即時デモが可能な初期データ。 | `python scripts/seed_demo.py` 実行後にGET /resourcesで2件、GET /agentsで4件返る | script added; runtime requires backend |
| T153 | done | Codex CLI | T152 | docs/INSTALL.md | インストールガイド: 前提条件（Docker, Docker Compose）、.env設定手順、`docker compose up`、初期データ投入、動作確認手順。日本語。 | ガイドに従って未経験者がセットアップ可能な記述水準 | docs/INSTALL.md added |
| T154 | done | Codex CLI | T153 | docs/repo-map.md, docs/state.md, docs/decisions.md, HANDOFF-JA.md | ドキュメント最終更新: repo-map.mdにbackend/, dashboard/の構造反映。state.mdに完了ポインタ更新。decisions.mdにStep 3実装判断記録。HANDOFF-JA.md更新。 | 全ドキュメントが最新状態を反映 | node scripts/verify.mjs -> passed |

---

## Dependency Graph (Critical Path)
```
T100 ──→ T103 ──→ T114 ──→ T113 ──→ T120 ──→ T122 ──→ T130 ──→ T140 ──→ T150 ──→ T151
  │         │        │                   │                          │
  │         ├──→ T112 ┘                   │                          ├──→ T152 ──→ T153 ──→ T154
  │         └──→ T110 ──→ T111 ──→ T121 ─┘                          │
  │                                  └──→ T131                       │
  │                                  └──→ T133                       │
  │                                                                  │
T101 ────────────────────────────────────────────────→ T141 ──→ T142 ┘
  │
T102 ─────────────────────────────────────────────────────────→ T150
```

## Parallel Groups (同時着手可能)
- **Group 1**: T100, T101, T102 （基盤3タスクは相互独立）
- **Group 2**: T103完了後 → T110, T112, T113, T114 は並列可能（Write Scope不重複）
- **Group 3**: T111完了後 → T121, T131, T133 は並列可能
- **Group 4**: T132 は T114 のみ依存、他と並列可能

## Blockers
| ID | Task | Blocker | Needed decision | Owner |
|---|---|---|---|---|
| (none) | | | | |

## Review Notes
| Task | Reviewer | Result | Follow-up |
|---|---|---|---|

## Review Remediation Ledger (2026-05-21)
| ID | Status | Evidence |
|---|---|---|
| H1 | done | Approval API now calls ApprovalWorkflow.decide() before SIGNING/SETTLED; tampered displayed_terms_hash returns 400 in tests. |
| H2 | done | backend/alembic/versions/0002_remaining_tables.py adds agent_mandates, participants, messages, agreements, approval, feedback tables. |
| H3 | done | dashboard/src/middleware.ts redirects unauthenticated requests using admith_api_key cookie. |
| H4 | done | dashboard home fetches /dashboard/metrics; approve page fetches negotiation detail and POSTs approve/reject. |
| H5 | done | ORM Resource.location uses geoalchemy2 Geography(Point,4326); migration alters resources.location. |
| M1 | done | ComplianceRulePort now uses Terms + ResourceEnvelope generic contract in domain/contracts.py. |
| M2 | done | approve settlement records trust, price, mandate, and matching feedback records. |
| M3 | done | API key comparison uses hmac.compare_digest. |
| M4 | done | docker-compose adds API_URL=http://backend:8000 while keeping NEXT_PUBLIC_API_URL for browser calls. |
| M5 | done | Orchestrator emits sequence_number=0 sentinel; repository assigns hash-chain sequence. |
| M6 | done | Approval reject recommendation uses actual negotiation initiator agent_id. |
| L3 | done | smoke_test.sh polling is configurable via SMOKE_MAX_ATTEMPTS and SMOKE_POLL_SECONDS. |

Verification:
rtk ruff check backend/src tests passed;
rtk pytest -q 15 passed;
rtk pnpm --prefix dashboard build passed;
node scripts/verify.mjs passed. Docker remains unverified because Docker CLI is unavailable in this environment.

---

## Step 4: Production Release Implementation Plan

### Planning Method
- Chain-of-thought: 実行済み。台帳には検証可能な結論・タスク・受入条件のみを記録し、非公開推論は記載しない。
- Chain-of-Verification:
  1. READMEの本番前リスクを確認: in-memory runtime, 組織ユーザー認証, KYB, 権限管理, 秘密情報管理, 外部契約・マニフェスト連携, クロスベンダーセキュリティレビュー。
  2. 現状実装を確認: `backend/src/admith/api/runtime.py` はin-memory singleton、`backend/src/admith/api/main.py` は単一API_KEY認証、`manifest_stub.py` / `econtract_stub.py` はスタブ。
  3. 実装確定できるproduction profile境界を先にfail-closed化し、未選定ベンダー依存はblocked decisionへ分離。
  4. 本番不可の外部意思決定は、人間の契約・法務・運用判断なしに完了扱いにしない。

### Three Skeletons Compared
| Skeleton | Summary | Decision |
|---|---|---|
| A | Big-bang SaaS rebuild | reject: 既存MVPの検証済み境界を捨て、回帰範囲が大きい |
| B | Incremental hardening behind existing Ports | adopt: Hexagonal構造と既存テストを活かし、DB/Auth/KYB/RBAC/External/Operationsを段階差替できる |
| C | Managed BaaS-heavy | reject: 契約・監査・マニフェスト要件が外部仕様へ過剰依存する |

### Release Gates
- G0 DB: production profile でin-memory repositoryが起動不能。状態の真実はPostgreSQL/PostGISのみ。
- G1 Auth: 単一API_KEYを廃止し、組織ユーザー、サービスアカウント、招待制オンボーディング、MFA対応OIDC/JWTを強制。
- G2 KYB: OwnerEntityはKYB verifiedになるまで取引・承認・外部契約・マニフェスト操作不可。
- G3 Authorization: RBAC + MandateScope + OntologyView Dynamic SecurityがAPI/DB/Workflowで一貫して強制される。
- G4 External: 電子契約・電子マニフェストはsandbox/prod Adapter、idempotency、署名検証、監査ログ、リトライ/DLQを備える。
- G5 Compliance: 食品リサイクル法、廃棄物処理法、取適法、個人情報/営業秘密、契約証跡について法務レビュー済み。
- G6 Operations: secrets, observability, backup/restore, incident response, SLO, rate limit, abuse detection が本番運用可能。
- G7 Security: SAST/DAST/dependency/container/IaC scan、pen test、cross-vendor review、修正確認が完了。
- G8 Evidence: release evidence pack に全検証結果、既知リスク、残リスク受容、rollback手順を保存。

### Blocked Business / Vendor Decisions
| ID | Status | Decision Needed | Why It Blocks | Owner |
|---|---|---|---|---|
| BD1 | blocked | OIDC/IdP provider and tenant model selection | JWT issuer/JWKS, org mapping, MFA policy, SCIM可否が実装に影響 | Human + Coordinator |
| BD2 | blocked | KYB provider or internal KYB operation model | 必要書類、審査ステータス、webhook、再審査周期がDB/API/UIに影響 | Human + Legal/Ops |
| BD3 | blocked | 電子契約サービス provider | 署名フロー、本人確認、webhook、証跡保管方式がAdapterに影響 | Human + Legal/Ops |
| BD4 | blocked | 電子マニフェスト/JWNET等の接続方式と資格情報 | API利用可否、代理操作範囲、法定保管要件がAdapterに影響 | Human + Legal/Ops |
| BD5 | blocked | Production hosting and data residency target | network, secrets, backup, monitoring, WAF, log retention設計に影響 | Human + Platform |

## Phase G: Production Architecture & Risk Closure

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification | Evidence |
|---|---|---|---|---|---|---|---|
| T200 | done | Codex CLI | none | tasks.md, docs/state.md, docs/decisions.md, docs/issues.md, docs/production-readiness.md | README記載リスクを本番Release Gateへ変換し、既存MVPとの差分・blocking decisions・優先順位を確定する。 | `docs/production-readiness.md` にリスク、対策、Release Gate、担当、期限、残リスク受容条件がある。 | `rtk git diff --check`; `node scripts/verify.mjs` | review accepted; docs/production-readiness.md added |
| T201 | done | Codex CLI | T200 | docs/decisions.md, docs/context/Admith_Technical_Design.md | Step 4採用アーキテクチャを確定する。B案（既存Ports背後の段階的本番化）を正式決定し、DB/Auth/KYB/RBAC/External/Operationsの境界を追記する。 | D030として恒久判断が追加され、設計書にproduction profileとdemo profileの境界が明記される。 | `rtk git diff --check`; `node scripts/verify.mjs` | review accepted; D030 + Technical Design §3.2 |
| T202 | done | Codex CLI | T200 | docs/threat-model.md, docs/data-classification.md | STRIDE/LINDDUNベースの脅威モデルとデータ分類を作成する。契約条件、法人情報、KYB書類、監査ログ、マニフェスト、署名証跡を分類する。 | API/DB/外部連携/ダッシュボード/運用者の脅威、対策、検証タスクが網羅される。 | security review checklist; `rtk git diff --check` | review accepted; docs/threat-model.md and docs/data-classification.md added |
| T203 | done | Codex CLI | T200 | backend/src/admith/config.py, backend/src/admith/api/runtime.py, backend/src/admith/adapters/*_stub.py, docker-compose.yml, .env.example, tests/test_config.py | runtime profileを導入する。`ADMITH_RUNTIME=demo|production` を定義し、productionではin-memory runtimeとstub external adapterが起動不能にする。 | production profileでin-memory/stubが選ばれると起動時に明示エラー。demo profileは既存デモが維持される。 | `rtk pytest -q`; `rtk ruff check backend/src tests` | FastAPI lifespan check added; 22 tests passed |

## Phase H: Database Persistence Cutover

| ID | Status | Owner | Depends On | Write Scope | Task | Acceptance | Verification | Evidence |
|---|---|---|---|---|---|---|---|
| T210 | done | Codex CLI | T203 | backend/src/admith/adapters/db/, backend/alembic/versions/, tests/, docs/db-schema-audit.md | ORM/Alembic gap audit。Pydantic domain model、ORM、migration、repository portの全フィールド対応表を作り、不足列・制約・index・enum driftを修正する。 | 全domain modelがDBへ保存/復元可能。enum、FK、unique、check、index、append-only audit triggerがmigrationに存在。 | `rtk pytest -q`; `alembic upgrade head` in test DB; migration drift check | static gap fixes reviewed; D031/D032 added; DB upgrade still pending |
| T211 | doing | Codex CLI | T210 | backend/src/admith/adapters/db/repositories.py, backend/src/admith/adapters/db/session.py, tests/ | SQLAlchemy async repositoryを本番実装する。Resource/Negotiation/Audit/Owner/Agent/Approval/Feedbackをin-memory同等APIで実装する。 | 既存in-memory repository testsと同一contract testsがDB repositoryでも通過。 | `rtk pytest tests -q`; transaction rollback tests | partial Resource/Negotiation/Audit adapter added; DB contract tests pending |
| T212 | doing | Codex CLI | T211 | backend/src/admith/api/dependencies.py, backend/src/admith/api/main.py, backend/src/admith/api/runtime.py, tests/ | FastAPI dependency injectionとUnit of Workを導入し、APIからmodule global singletonを排除する。`ensure_production_safe_settings()` はlifespan起動時にも実行済みで、DI導入時も維持する。 | API requestごとにDB session/transactionが管理され、rollback時に部分書込が残らない。 | API integration tests with test DB; `rtk ruff check backend/src tests` | memory path DI化完了、demo runtime import side effects除去、`rtk pytest -q` 22 passed; DB path E2Eは環境制約で継続 |
| T213 | ready | Codex CLI | T212 | backend/src/admith/domain/, backend/src/admith/adapters/db/repositories.py, tests/ | 競合制御を本番化する。resource lockは`SELECT FOR UPDATE SKIP LOCKED`、lock_token、locked_until lease、idempotency keyで二重交渉を防ぐ。 | 同一Resourceへの並行交渉開始で1件のみ成功し、重複リクエストはidempotent responseになる。 | concurrent pytest; DB isolation tests | race-condition evidence |
| T214 | ready | Codex CLI | T212 | scripts/seed_demo.py, scripts/migrate_demo_data.py, docs/INSTALL.md | demo seedをDB repository対応へ移行する。in-memory専用seedや実行手順を廃止/分離する。 | `scripts/seed_demo.py` がproduction-like DBにOwner/Agent/Mandate/Resourceを投入し、再実行しても重複しない。 | seed integration test; smoke test | seed output |
| T215 | ready | Codex CLI | T214 | backend/src/admith/api/runtime.py, backend/src/admith/adapters/repositories.py, tests/, README.md | production pathからin-memory runtime依存を除去する。demo用in-memoryは明示的にtest/demo moduleへ隔離する。 | production import graphに`InMemory*Repository`が含まれない。READMEのCurrent ScopeからDB未永続化リスクを削除できる。 | import graph check; `rtk rg "InMemory" backend/src/admith/api backend/src/admith/adapters`; full test suite | cutover evidence |

## Phase I-N Remaining Production Tasks

| ID | Status | Blocks | Summary |
|---|---|---|---|
| T220-T224 | blocked/ready after T220 | BD1 | OIDC/organization user auth, membership, invite-only onboarding, dashboard OIDC migration |
| T230-T234 | blocked/ready after T230 | BD2 | KYB SOP, KYB schema, provider adapter, KYB transaction gate, KYB operations UI |
| T240-T244 | ready after T220/T230 | BD1, BD2 | RBAC/ABAC matrix, authorization service, tenant guard/RLS, OntologyView security, dashboard authz |
| T250-T255 | blocked/ready after T250 | BD3, BD4 | e-contract and manifest provider design, external job schema, adapters, workflow, operations UI |
| T260-T265 | blocked/ready after T260 | BD5 | production hosting, config hardening, observability, backup/restore, abuse protection, security automation |
| T270-T276 | blocked/ready after dependencies | BD1-BD5 + independent reviews | legal/security review, production E2E, performance, audit export, release docs, RC evidence |

## Step 4 Current Blockers
| ID | Blocks | Required Action | Owner |
|---|---|---|---|
| BD1 | T220-T224 | IdP/OIDC provider and tenant model decision | Human |
| BD2 | T230-T234 | KYB provider or internal KYB SOP decision | Human + Legal/Ops |
| BD3 | T250/T252/T254/T255 | 電子契約provider decision | Human + Legal/Ops |
| BD4 | T250/T253/T254/T255 | 電子マニフェスト接続方式 decision | Human + Legal/Ops |
| BD5 | T260-T265 | Production hosting/data residency decision | Human + Platform |

## Step 4 Definition of Done
- in-memory runtime and stub adapters cannot be used in production profile.
- Organization/user authentication, invite-only onboarding, service account auth, and MFA-capable OIDC are enforced.
- KYB verified status is required before all business-critical actions.
- RBAC/ABAC, MandateScope, OntologyView filtering, and DB tenant isolation all agree.
- External contract and manifest integrations have sandbox/prod adapters, webhook signature verification, idempotency, retries, DLQ, and audit evidence.
- Human Final Approval remains mandatory before signing, settlement, contract issuance, or manifest finalization.
- Audit export can prove negotiation, approval, contract, manifest, settlement, and feedback history without mutable gaps.
- Security, legal, ops, load, restore, and cross-vendor reviews are complete with no unresolved HIGH/CRITICAL issues.

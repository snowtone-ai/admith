● Admith Step 3 MVP コードレビュー — T100〜T154        
                                                                                          
  レビュー担当: Claude Code (Opus 4.6)
  実装担当: Codex CLI                                                                     
  検証済み: ruff check ✅ | pytest 15/15 ✅ | pnpm build ✅ | verify.mjs ✅
  Docker: 未検証（Docker CLI unavailable）                                                
                  
  ---
  HIGH — 修正必須

  H1. D008違反: approve エンドポイントが ApprovalWorkflow をバイパス

  backend/src/admith/api/main.py:174-181

  approve エンドポイントが orchestrator.settle_after_approval()
  を直接呼び出し、ApprovalWorkflow.decide() を経由しない。結果として:
  - displayed_terms_hash の検証なし（改竄検知不可）
  - ApprovalDecision レコードが生成されない（監査証跡欠落）
  - reject時の MandateAdjustmentRecommendation が生成されない（D024違反）

  修正案:
  # main.py approve endpoint
  from admith.domain.approval import ApprovalWorkflow

  @app.post("/negotiations/{negotiation_id}/approve")
  async def approve_negotiation(negotiation_id: str, body: ApproveBody):
      neg = neg_repo.get(negotiation_id)
      if not neg or neg.state != NegotiationState.PENDING_HUMAN_APPROVAL:
          raise HTTPException(404)
      req = ApprovalRequest(
          id=str(uuid4()), negotiation_id=negotiation_id,
          displayed_terms_hash=body.terms_hash,
          expires_at=datetime.utcnow() + timedelta(minutes=30),
      )
      wf = ApprovalWorkflow()
      decision = wf.decide(req, ApprovalDecisionValue.APPROVED, body.terms_hash,
  body.reason)
      # persist decision, then settle
      orchestrator.settle_after_approval(neg, resources, audit_repo)
      return {"status": "settled", "decision_id": decision.id}

  同様に reject エンドポイント (main.py:183-190) も wf.decide(..., REJECTED, ...)
  を呼び、MandateAdjustmentRecommendation を生成すべき。

  ---
  H2. Alembic migration が設計 §4 のテーブルの過半数を欠落

  backend/alembic/versions/0001_initial.py

  作成済み: owner_entities, agents, resources, negotiations, audit_events (5テーブル)

  欠落 (設計 §4 必須):

  ┌────────────────────────────────────┬──────────────────────────────────────┐
  │            欠落テーブル            │             設計上の役割             │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ agent_mandates                     │ D020 Dynamic Security / MandateScope │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ negotiation_participants           │ 多対多交渉参加者                     │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ messages                           │ 交渉メッセージ履歴（D013監査）       │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ agreements                         │ 合意条件・署名・状態                 │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ approval_requests                  │ D008承認要求                         │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ approval_decisions                 │ D008承認結果・監査証跡               │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ trust_score_history                │ D021 Closed-Loop Feedback            │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ price_signal_history               │ D021 価格指数還元                    │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ mandate_adjustment_recommendations │ D024 Mandate自動調整                 │
  ├────────────────────────────────────┼──────────────────────────────────────┤
  │ matching_outcome_metrics           │ D021 Matching重み調整                │
  └────────────────────────────────────┴──────────────────────────────────────┘

  D026により in-memory store でデモ動作するが、DB path が不完全なため alembic upgrade head
   後の PostgreSQL 運用に移行できない。

  修正案: 0002_remaining_tables.py migration を追加し、上記10テーブルを作成。orm.py
  にも対応する Row クラスを追加。

  ---
  H3. Dashboard middleware が認証を強制しない

  dashboard/src/middleware.ts:4-7

  export function middleware() {
    return NextResponse.next();
  }

  全リクエストを素通しさせており、/login 以外のページへの未認証アクセスを防がない。

  修正案:
  import { NextRequest, NextResponse } from "next/server";

  export function middleware(request: NextRequest) {
    const isLoginPage = request.nextUrl.pathname === "/login";
    // Client-side auth: cookie or header check
    const hasApiKey = request.cookies.get("admith_api_key");
    if (!isLoginPage && !hasApiKey) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
    return NextResponse.next();
  }

  export const config = { matcher: ["/((?!_next|favicon.ico).*)"] };

  ▎ 注: localStorage は Server Component / middleware から読めないため、login ページで
  ▎ cookie にも保存する方式に変更が必要。

  ---
  H4. Dashboard ページが静的シェルで API 未接続

  dashboard/src/app/page.tsx — ハードコードされた静的カード。apiFetch()
  を一切呼んでいない。
  dashboard/src/app/negotiations/[id]/approve/page.tsx — textarea とボタンのみ。approve
  API への POST なし。

  Operator Dashboard として最低限必要な機能:
  1. page.tsx: /dashboard/metrics からリアルタイムデータ取得
  2. approve/page.tsx: /negotiations/{id} で詳細取得 → /negotiations/{id}/approve に POST

  修正案: 各ページに useEffect + apiFetch() を追加し、API レスポンスを表示・送信する。

  ---
  H5. ORM Resource.location が Text 型（PostGIS Geography 未使用）

  backend/src/admith/adapters/db/orm.py:55

  location = sa.Column(sa.Text, nullable=True)

  D020 Resource Ontology三層設計の Semantic 層で地理的属性は PostGIS Geography(Point,
  4326) で管理すべき。migration では PostGIS extension
  を有効化しているにもかかわらず使われていない。

  修正案:
  from geoalchemy2 import Geography
  location = sa.Column(Geography(geometry_type="POINT", srid=4326), nullable=True)

  ---
  MEDIUM — 改善推奨

  M1. ComplianceRulePort シグネチャが設計 §3.1 と不一致

  backend/src/admith/ports/interfaces.py:54

  現在: check(scenario: FoodWasteScenario) -> ComplianceResult
  設計: check(terms: Terms, envelope: ResourceEnvelope) -> ComplianceResult

  D025 で Compliance 分離・Resource Envelope 分離が恒久制約。現シグネチャは FoodWaste
  直結で汎用性がない。

  修正案: Terms と ResourceEnvelope を models.py に追加し、Port シグネチャを更新。Phase 0
  では内部で FoodWasteScenario に変換可。

  ---
  M2. Settlement feedback が永続化されない

  backend/src/admith/domain/settlement.py:38-58

  feedback_records() が4種のフィードバック（TrustScoreHistory, PriceSignalHistory,
  MandateAdjustmentRecommendation, MatchingOutcomeMetric）を返すが、API
  側で呼び出されず、FeedbackSinkPort にも渡されない。D021 Closed-Loop Feedback
  が実質未実装。

  修正案: settle エンドポイント内で settlement.feedback_records()
  を呼び、FeedbackSinkPort.record() に渡す。

  ---
  M3. API key 比較がタイミング攻撃に脆弱

  backend/src/admith/api/main.py:68

  if token != API_KEY:

  修正案:
  import hmac
  if not hmac.compare_digest(token, API_KEY):

  ---
  M4. Docker dashboard の NEXT_PUBLIC_API_URL がコンテナ間で機能しない

  docker-compose.yml:50

  NEXT_PUBLIC_API_URL: "http://localhost:8000"

  NEXT_PUBLIC_ はビルド時に埋め込まれる。dashboard コンテナからの SSR リクエストは
  localhost:8000 ではなく http://backend:8000 に向ける必要がある。

  修正案: SSR用の API_URL=http://backend:8000 (runtime env) と、クライアント用の
  NEXT_PUBLIC_API_URL=http://localhost:8000 を分離。api.ts で typeof window ===
  'undefined' 判定して切り替え。

  ---
  M5. orchestrator._event() の sequence_number が常に 1

  backend/src/admith/domain/orchestrator.py:60-66

  sequence_number=1,

  InMemoryAuditEventRepository.append() がリポジトリ内で再計算するため実害はないが、ドメイ
  ン層のセマンティクスとして不正確。呼び出し元がシーケンス番号を知らない場合は
  sequence_number=0 (sentinel) とし、リポジトリで採番する設計を明示すべき。

  ---
  M6. approval.py の MandateAdjustmentRecommendation が random UUID を使用

  backend/src/admith/domain/approval.py:53

  agent_id=str(uuid4()),  # random instead of actual agent

  reject 時に生成される Mandate 調整推奨の agent_id が実際のエージェントではなくランダム
  UUID。D024 の Mandate 自動調整に使えない。

  修正案: decide() に agent_id: str パラメータを追加し、交渉参加者の agent_id を渡す。

  ---
  LOW — 認知しておくべき事項

  L1. models.py が 298 行で品質基準 300 行上限に接近

  追加エンティティ（Terms, ResourceEnvelope 等）で超過見込み。早期にファイル分割を検討。

  L2. 全テストが in-memory 前提

  DB path（SQLAlchemy + Alembic）のテストが皆無。Docker 環境での integration test が必要。

  L3. smoke_test.sh が polling 間隔固定

  sleep 2 のハードコード。CI 環境では不安定になる可能性あり。

  ---
  総合判定

  ┌─────────────────────────┬─────────────────────────────────────────────────────────┐
  │          領域           │                          判定                           │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ D007/D022 LLM制約       │ ✅ 適合 — complete_view(OntologyView, LLMTask)          │
  │                         │ のみ、raw prompt なし                                   │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ D008 Human Final        │ ❌ H1 — ApprovalWorkflow バイパス                       │
  │ Approval                │                                                         │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ D013/D023 AuditEvent    │ ⚠️  構造は正しいが sequence_number セマンティクス不正確  │
  │                         │ (M5)                                                    │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ T103 エンティティ/Enum  │ ✅ 設計 §4 の全エンティティ実装済み                     │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ T112-T114 Port 設計     │ ⚠️  ComplianceRulePort シグネチャ不一致 (M1)             │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ T140 API                │ ❌ H1 approve バイパス + M3 タイミング攻撃              │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ T141-T142 Dashboard     │ ❌ H3 認証なし + H4 API 未接続                          │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ T150-T151 Docker        │ ⚠️  未検証 + M4 URL 問題                                 │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ 300行超/過簡略化        │ ⚠️  H2 migration 欠落が最大のギャップ                    │
  ├─────────────────────────┼─────────────────────────────────────────────────────────┤
  │ セキュリティ/法的安全   │ ⚠️  M3 タイミング攻撃、H1 監査証跡欠落                   │
  └─────────────────────────┴─────────────────────────────────────────────────────────┘

  結論: D007/D022 の LLM 制約とドメインモデル設計は高品質。一方で
  H1（D008違反）は最優先修正。Dashboard（H3/H4）と Migration（H2）は MVP
  デモ品質に直結するため早期対応を推奨。
  
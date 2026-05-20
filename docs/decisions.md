# decisions.md -- Permanent Decisions

| ID | Date | Decision | Rationale / Evidence | Source |
|---|---|---|---|---|
| D001 | 2026-05-20 | Product name is Admith. | Adam Smithの「見えざる手」をデジタルリソースへ適用する構想。 | docs/context/Admith_Project_Context.md §1 |
| D002 | 2026-05-20 | Mission is global resource optimization for human happiness. | 全リソースをAIエージェント間の自律取引対象にする北極星。 | docs/context/Admith_Project_Context.md §1 |
| D003 | 2026-05-20 | Phase 0 focuses on B2B food waste. | データ入手容易、価値測定明確、規制リスクが相対的に低い。 | docs/context/Admith_Business_Strategy.md §4 |
| D004 | 2026-05-20 | Step 2 is Gemini API four-party negotiation PoC. | 30秒以内に4者間交渉が収束するかを捨てるコードで検証する。 | docs/context/Admith_Project_Context.md §7 |
| D005 | 2026-05-20 | Adopt Transactional Modular Monolith + Hexagonal + Workflow Engine. | Phase 0の運用負荷を抑えつつ、SPOFと外部依存を分離する。 | docs/context/Admith_Technical_Design.md §1 |
| D006 | 2026-05-20 | Use Durable Workflow Engine for negotiation orchestration. | ChatGPT監査でOrchestrator SPOFが致命的欠陥とされた。 | docs/context/Admith_Project_Context.md §3 |
| D007 | 2026-05-20 | Exclude LLM from contract decisions. | LLM非決定性を避け、価格・制約・合意条件はRule Engineで確定する。 | docs/context/Admith_Project_Context.md §3 |
| D008 | 2026-05-20 | Require Human Final Approval before signing or settlement. | Ed25519署名だけでは法的に弱く、本人意思・代理権限の証明が必要。 | docs/context/Admith_Project_Context.md §3 |
| D009 | 2026-05-20 | Require KYB and invitation-only onboarding in Phase 0. | Sybil価格操作とwash tradingを初期構造で抑える。 | docs/context/Admith_Project_Context.md §3 |
| D010 | 2026-05-20 | Add resource locking with lock_token and locked_until. | Resource二重ロックを防ぐため、SELECT FOR UPDATEとlease tokenを使う。 | docs/context/Admith_Project_Context.md §3 |
| D011 | 2026-05-20 | Split TTL into matching, negotiation, approval, pickup, settlement phases. | TTL=30秒単一設計は短すぎるため、業務段階別に期限を分ける。 | docs/context/Admith_Project_Context.md §3 |
| D012 | 2026-05-20 | Phase 0 excludes CVE, public Accord API, escrow, generic plugins, and paid Trust Score API. | ChatGPT監査で過剰設計を削減し、Food Waste直書きを優先した。 | docs/context/Admith_Project_Context.md §3 |
| D013 | 2026-05-20 | Store negotiation logs, estimate basis, and change reasons. | 下請法から取適法への2026年1月改正を見据え、協議ログ保存が必要。 | docs/context/Admith_Project_Context.md §3 |
| D014 | 2026-05-20 | Use pm-zero v9.4 Lean Task Ledger OS. | tasks.md、state.md、repo-map.mdで実行管理と引き継ぎ損失を防ぐ。 | C:/Users/chidj/project/pm-zero/pm-zero-knowledge-v9.4.md |
| D015 | 2026-05-20 | Agent routing: planning/design/review by Claude Code, implementation by Codex CLI. | pm-zero v9.4の役割分担にAdmith固有ルールとして明記する。 | user instruction |
| D016 | 2026-05-20 | Use Python/FastAPI for backend and Next.js/TypeScript for Operator Dashboard. | Phase 0規模ではGoの真の並列性は不要。LLM API統合、エージェント交渉、将来のVector DB/差分プライバシー周辺ライブラリはPython-firstが最も強い。UIはTypeScriptが自然。 | user instruction |

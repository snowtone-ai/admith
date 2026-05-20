# vision.md -- Product North Star

## Purpose
Admithは、取引コスト、情報処理、交渉帯域が価値を上回るために市場化されなかったリソースを、AIエージェントの高速・並列・自律交渉で経済圏に引き込む。Phase 0ではB2B食品廃棄物を対象に、負の価値を持つ副産物を飼料・肥料・アップサイクル原料へ転換し、創造価値の20%を収益化する。

## Target Users
- 食品製造業者: おから等の食品副産物・余剰在庫・廃棄予定品の廃棄コストを下げたい企業。
- 飼料・肥料・アップサイクル業者: 安定した低コスト原料を調達したい企業。
- 物流業者: 空車回送や既存ルートの余剰積載を収益化したい企業。
- Admithオペレーター: 交渉、コンプライアンス、Human Final Approval、監査ログを管理する運営者。

## Success Criteria
- Gemini APIを用いた4者間交渉PoCで30秒以内の収束可能性を検証する。
- Phase 0 MVPで交渉成立率30%以上を目指す。
- 1取引あたり平均Deltaを測定し、Month 6時点で平均10,000円未満ならドメイン変更を検討する。
- Human Approval reject率、価格一貫性、LLM/APIコスト、TTL超過率を継続測定する。
- 実取引ではHuman Final Approvalなしに署名・資金移動を行わない。

## Non-goals
- Phase 0では完全自動契約を行わない。
- Phase 0では汎用Admith Accord公開API、CVE、Vector DB、Trust Score有料API、マイクロ決済を実装しない。
- LLMに価格、制約、契約成立可否を判断させない。
- 自由登録型マーケットプレイスにしない。初期は招待制・KYB必須とする。

## Product Principles
- FoodWaste-First: Phase 0は食品廃棄物に深く刺す。
- Rule Engine First: 価格・制約・合意条件は決定論的に確定する。
- Human-in-the-Loop Default: 実取引は人間承認を必須にする。
- Compliance by Design: 廃棄物処理法、食品リサイクル法、取適法対応をワークフローへ組み込む。
- Auditability: 交渉ログ、見積根拠、変更理由、承認履歴を保存する。
- Lean Build: PoCは捨てる前提の小さな検証コードから始める。

## Primary User Flows
1. Seller Agentが食品副産物の種類、量、排出時間、廃棄単価をCFPとして提示する。
2. Buyer Agentが購入条件、Logistics Agentが輸送条件を提出する。
3. Mediator AgentがRule Engineで価値創造額、法令優先順位、制約充足を評価する。
4. 必要に応じてGemini APIが交渉文面、説明、要約を補助する。
5. Agreement Zoneに収束したら構造化された合意案を作成する。
6. Human Final Approval後にのみ署名・契約・請求処理へ進む。

## Failure Cases
- 30秒以内にPoC交渉が収束しない。
- LLM出力が価格・制約判断に混入する。
- 飼料化優先など食品リサイクル法の優先順位を破る。
- 廃棄物処理法上の委託契約・許可業者・マニフェスト確認が欠落する。
- Human Approval前に署名または資金移動が発生する。
- Sybil価格操作、二重ロック、TTL切れ、物流直前キャンセルが発生する。

## Long-term Goal
Admith MarketplaceでCat.5の新市場を開き、Admith Accordで既存市場・業界プラットフォームへエージェント交渉プロトコルを提供する。最終的には物理、時間、情報、制度バッファ、意図などの未市場化リソースに価格発見と流動性を与える。

## Relationship to tasks.md
- This file defines product intent.
- tasks.md defines implementation tasks.
- Store task progress and evidence in tasks.md.
- Store only the current pointer in docs/state.md.

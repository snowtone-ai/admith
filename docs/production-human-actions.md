# production-human-actions.md

## Purpose
本番プロダクト完成のために、人間の契約・法務・運用・インフラ判断が必要な作業を集約する。AIはコード、テスト、文書、静的設計までは進められるが、以下は資格情報、契約、法的責任、実環境承認を伴うため人間が完了させる。

## Required Human Decisions
| ID | Owner | Required output | Blocks | Completion evidence |
|---|---|---|---|---|
| BD1 | Product + Security + IT | OIDC/IdP provider、tenant model、MFA policy、JWKS rotation、SCIM要否、service account方針 | T220-T224, T240-T244 | IdP設定書、test tenant、client ID、JWKS URL、role/group mapping、MFA policy承認 |
| BD2 | Legal + Ops | KYB providerまたは社内KYB SOP、必要書類、審査ステータス、再審査周期、却下/停止手順 | T230-T234, T240-T244 | KYB SOP、審査チェックリスト、サンプルwebhookまたは運用入力仕様、法務承認 |
| BD3 | Legal + Ops | 電子契約provider、署名フロー、本人確認、証跡保管、webhook署名、契約テンプレート | T250, T252, T254, T255 | provider契約、sandbox資格情報、署名証跡サンプル、契約テンプレート法務承認 |
| BD4 | Legal + Ops | 電子マニフェスト/JWNET等の接続方式、代理操作範囲、法定保管要件、運用責任分界 | T250, T253, T254, T255 | 接続資格、sandbox/prod利用条件、操作権限一覧、保管/監査要件承認 |
| BD5 | Platform + Security | 本番hosting、data residency、network、WAF、secret管理、backup/restore、監視、ログ保持 | T260-T265 | インフラ設計、環境URL、secret store、restore rehearsal結果、監視/アラート設定 |

## Required Human Reviews
| Review | Owner | Required output |
|---|---|---|
| Legal/compliance review | Legal | 食品リサイクル法、廃棄物処理法、取適法、個人情報、営業秘密、契約証跡のGo/No-Go判断 |
| Cross-vendor security review | Independent reviewer | Auth、DB schema、RLS/permissions、external API、deploy、secrets、audit chainのHIGH/CRITICALゼロ確認 |
| Operations readiness review | Ops + Platform | incident response、on-call、SLO、backup/restore、rollback、DLQ運用、障害時手順の承認 |
| Production release approval | Product owner + Legal + Security | 残リスク受容、release evidence pack、rollback plan、customer communication planの承認 |

## Environment Work Humans Must Provide
- PostgreSQL 16 + PostGISが利用できるテストDB。本リポジトリでは `alembic upgrade head -> downgrade -> upgrade` とDB repository contract testsを実行する。
- 外部provider sandbox資格情報。電子契約、電子マニフェスト、KYB、OIDCはスタブではなくsandbox/prod adapterで検証する。
- 本番secret values。`.env.example` はテンプレートのみで、実secretはリポジトリへ保存しない。
- 本番相当のログ/監視/backup環境。AIは設定ファイルを作成できるが、実アカウント、権限、保持ポリシー承認は人間が行う。

## Go/No-Go Rule
BD1-BD5、法務レビュー、クロスベンダーセキュリティレビュー、restore rehearsal、外部provider sandbox E2Eのいずれかが未完了の場合、本番リリースはNo-Goとする。

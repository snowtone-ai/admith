# Admith Flow

![Next.js](https://img.shields.io/badge/Next.js-frontend-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-teal?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 食品廃棄物の「売りたい」と「欲しい」を自動でつなぎ、価格交渉まで済ませるB2B向けシステム

食品廃棄物を出している事業者と、それを資源として受け取りたい事業者のマッチング・価格交渉をシステムが自動で処理します。AIが勝手に契約を結ぶことはなく、最終的な確定は必ず人間が承認する仕組みです。

---

## 主な機能

- 食品廃棄物リソースの登録・管理ができる
- 事業者間の交渉を自動で進め、価格・コンプライアンス条件を決定論的ルールエンジンで算出できる
- 人間の最終承認を経て契約・精算が完了する
- 交渉の全経緯を改ざん不可能な監査ログとして記録・確認できる
- オペレーター向けダッシュボードからリソース登録・交渉状況・承認操作ができる

---

## 技術スタック

| カテゴリ | 技術 |
|---|---|
| フロントエンド | Next.js |
| バックエンド | FastAPI, SQLAlchemy, Alembic |
| データベース | PostgreSQL + PostGIS |
| インフラ | Docker Compose |

---

## 設計の工夫

- ヘキサゴナルアーキテクチャを採用しており、データベースやAPIの差し替えが容易
- 価格・契約・コンプライアンス判断をAIではなく決定論的ルールエンジンで処理し、判断の再現性・監査可能性を確保
- 人間の最終承認なしに署名・資金移動・契約確定が実行されない安全設計

---

## セットアップ

必要なツール：Docker Desktop（Docker Compose v2）、Node.js、pnpm、Python 3.12

`.env.example` をコピーして `.env` を作成し、APIキーを設定します。

```bash
cp .env.example .env
```

`.env` に以下を設定してください。

```
API_KEY=任意のランダム文字列
```

スタックを起動します。

```bash
docker compose up -d --build
```

ダッシュボードを開きます。

```
http://localhost:3000
```

`.env` に設定した `API_KEY` でログインしてください。

スタックを停止するには：

```bash
docker compose down
```

---

## ライセンス

MIT

# Admith MVP インストールガイド

## 前提
- Docker Desktop
- Docker Compose v2

## 起動
1. `.env.example` を参考に `.env` を作成し、`API_KEY` を推測されにくい値へ変更します。
2. `docker compose up -d --build` を実行します。
3. `http://localhost:3000` を開き、`.env` の `API_KEY` でログインします。

## デモデータ
Backend起動後に以下を実行します。

```bash
docker compose exec backend uv run python scripts/seed_demo.py
```

## 動作確認
1. `/resources` で食品廃棄物リソースを登録します。
2. `/negotiations` で交渉を開始します。
3. 承認待ちになったら承認画面でapproveします。
4. `/audit` で監査ログを確認します。

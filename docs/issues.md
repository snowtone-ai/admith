# issues.md -- Failure Log

| ID | Date | Task | Issue | Impact | Resolution | Status |
|---|---|---|---|---|---|---|
| I001 | 2026-05-21 | T001 | Gemini connection test reached the API, but legacy fixed model names (`gemini-1.5-flash`, `gemini-1.5-flash-latest`) returned 404; other candidates returned quota/demand errors (429/503). | T001 verification was blocked temporarily. | Implemented `models.list` discovery + fallback and switched to free-tier API key/project. `python scripts/test_gemini_connection.py` succeeded with `gemini-2.5-flash` and `admith-ok`. | closed |

## Escalation Notes
- Record recurring failures, blocked commands, ambiguous requirements, and human decisions here.

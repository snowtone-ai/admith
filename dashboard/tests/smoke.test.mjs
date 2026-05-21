import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("dashboard scripts expose lint, typecheck, test, and build", async () => {
  const pkg = JSON.parse(await readFile(new URL("../package.json", import.meta.url), "utf8"));
  assert.equal(pkg.scripts.lint, "eslint . --max-warnings=0");
  assert.equal(pkg.scripts.typecheck, "tsc --noEmit");
  assert.equal(pkg.scripts.test, "node --test tests/**/*.test.mjs");
  assert.equal(pkg.scripts.build, "next build");
});

test("browser API auth reads the middleware cookie and has no hard-coded demo key", async () => {
  const source = await readFile(new URL("../src/lib/api.ts", import.meta.url), "utf8");
  assert.match(source, /admith_api_key/);
  assert.doesNotMatch(source, /test-key/);
});

import assert from "node:assert/strict";
import test from "node:test";
import { resolve } from "node:path";

import { validateMermaidCorpus } from "../scripts/check-status-quo-mermaid.mjs";

test("every status-quo Mermaid block parses with the pinned renderer", async () => {
  const repositoryRoot = resolve(import.meta.dirname, "../..");

  const result = await validateMermaidCorpus(repositoryRoot);

  assert.ok(result.count >= 16, `expected the required diagram set, found ${result.count}`);
  assert.deepEqual(result.errors, []);
});

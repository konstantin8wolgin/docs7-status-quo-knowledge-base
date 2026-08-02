import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { createServer } from "vite";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const clientRoot = path.resolve(testDir, "..");
const mockLibId = "\0docs7-view-regression-lib";
const mockApiId = "\0docs7-view-regression-api";

function factCardsFromDocuments(documents = []) {
  return documents.flatMap((doc) =>
    (doc.facts || []).map((fact, index) => ({
      id: fact.id || `${doc.id}:${fact.key || index}`,
      person: fact.person || doc.person || "",
      category: fact.category || "identity",
      key: fact.key || `fact_${index}`,
      label: fact.label || fact.key || `Fakt ${index + 1}`,
      value: String(fact.value),
      status: fact.status || "proposed",
      source_doc_id: fact.source_doc_id || doc.id,
      updated_at: fact.updated_at || doc.created_at,
      verification_id: fact.verification_id,
    }))
  );
}

async function withViewServer(run) {
  const server = await createServer({
    root: clientRoot,
    logLevel: "error",
    appType: "custom",
    server: { middlewareMode: true, hmr: false, ws: false },
    plugins: [
      {
        name: "docs7-view-regression-mocks",
        enforce: "pre",
        resolveId(source) {
          if (source === "../lib.jsx" || source.endsWith("/src/lib.jsx")) return mockLibId;
          if (source === "../api.js" || source.endsWith("/src/api.js")) return mockApiId;
          return null;
        },
        load(id) {
          if (id === mockApiId) {
            return `
              export const api = {
                listAllDocuments: async () => globalThis.__DOCS7_VIEW_TEST_DOCS__ || [],
                listEntities: async () => globalThis.__DOCS7_VIEW_TEST_ENTITIES__ || [],
                entityCard: async (id) => (globalThis.__DOCS7_VIEW_TEST_CARDS__ || {})[id],
                messages: async () => globalThis.__DOCS7_VIEW_TEST_MESSAGES__ || [],
                verifyFact: async (id, value) => ({ id, value, status: "verified" }),
              };
            `;
          }
          if (id !== mockLibId) return null;
          return `
            import React from "react";
            export const FACT_CAT_LABEL = { identity: "Identität", tax: "Steuer" };
            export function useStore() {
              return globalThis.__DOCS7_VIEW_TEST_STORE__;
            }
            export function initials(name = "") {
              return name.split(" ").map((part) => part[0]).slice(0, 2).join("").toUpperCase();
            }
            export function Empty({ title, sub, children }) {
              return React.createElement("div", null, title, sub, children);
            }
            export function FolderIcon() {
              return React.createElement("span", null);
            }
            export function FactIcon() {
              return React.createElement("span", null);
            }
            export function Tick({ verified }) {
              return React.createElement("span", null, verified ? "verified" : "proposed");
            }
            export function fmtDate(value) {
              return value || "-";
            }
            export function factsFromDocuments(documents = []) {
              return (${factCardsFromDocuments.toString()})(documents);
            }
          `;
        },
      },
    ],
  });

  try {
    return await run(server);
  } finally {
    await server.close();
    delete globalThis.__DOCS7_VIEW_TEST_STORE__;
    delete globalThis.__DOCS7_VIEW_TEST_DOCS__;
    delete globalThis.__DOCS7_VIEW_TEST_MESSAGES__;
    delete globalThis.__DOCS7_VIEW_TEST_ENTITIES__;
    delete globalThis.__DOCS7_VIEW_TEST_CARDS__;
  }
}

async function withRealViewServer(run) {
  const server = await createServer({
    root: clientRoot,
    logLevel: "error",
    appType: "custom",
    server: { middlewareMode: true, hmr: false, ws: false },
  });

  try {
    return await run(server);
  } finally {
    await server.close();
  }
}

const iljaDoc = {
  id: "doc-ilja",
  person: "Ilja Stehle",
  relationLabel: "Du",
  personColor: "#2f88ff",
  folder: "Steuern",
  title: "Steuerbescheid",
  doc_date: "2026-06-01",
  created_at: "2026-06-10T10:00:00Z",
  action: { needed: false },
  facts: [
    {
      id: "fact-ilja-tax",
      person: "Ilja Stehle",
      category: "tax",
      key: "steuer_id",
      label: "Steuer-ID",
      value: "12 345 678 901",
      status: "proposed",
      source_doc_id: "doc-ilja",
      updated_at: "2026-06-10T10:00:00Z",
    },
  ],
};

const familyDocs = [
  iljaDoc,
  {
    id: "doc-mira",
    person: "Mira Stehle",
    relationLabel: "Kind",
    personColor: "#e58fb0",
    folder: "Familie",
    title: "Geburtsurkunde Mira",
    doc_date: "2026-05-01",
    created_at: "2026-06-09T10:00:00Z",
    action: { needed: false },
    facts: [
      {
        id: "fact-mira-birth",
        person: "Mira Stehle",
        category: "identity",
        key: "date_of_birth",
        label: "Geburtsdatum",
        value: "2020-01-02",
        status: "verified",
        source_doc_id: "doc-mira",
        updated_at: "2026-06-09T10:00:00Z",
      },
    ],
  },
  {
    id: "doc-jonas",
    person: "Jonas Stehle",
    relationLabel: "Kind",
    personColor: "#0fa3a3",
    folder: "Familie",
    title: "Schulbescheinigung Jonas",
    doc_date: "2026-04-01",
    created_at: "2026-06-08T10:00:00Z",
    action: { needed: false },
    facts: [
      {
        id: "fact-jonas-school",
        person: "Jonas Stehle",
        category: "identity",
        key: "school",
        label: "Schule",
        value: "Grundschule",
        status: "proposed",
        source_doc_id: "doc-jonas",
        updated_at: "2026-06-08T10:00:00Z",
      },
    ],
  },
];

test("insights labels all income amount kinds in German", async () => {
  const source = await fs.readFile(path.join(clientRoot, "src", "views", "Einblicke.jsx"), "utf8");

  assert.match(source, /rent_income:\s*"Mieteinnahmen"/);
  assert.match(source, /salary:\s*"Gehalt"/);
  assert.match(source, /other_income:\s*"Sonstige Einnahmen"/);
});
test("family view renders person cards from the entity register", async () => {
  await withViewServer(async (server) => {
    const { FamilyGrid, familyEntities } = await server.ssrLoadModule("/src/views/Familie.jsx");
    const members = familyEntities([
      { id: "entity-mira", kind: "person", name: "Mira Stehle", subtype: "Kind", personId: "person-mira", aliases: [], docCount: 2 },
      { id: "entity-jonas", kind: "person", name: "Jonas Stehle", subtype: "Kind", personId: "person-jonas", aliases: [], docCount: 1 },
      { id: "entity-school", kind: "organization", name: "Grundschule", aliases: [], docCount: 1 },
    ]);

    const html = renderToStaticMarkup(React.createElement(FamilyGrid, { members, onSelect: () => {} }));

    assert.match(html, /Mira Stehle/);
    assert.match(html, /Jonas Stehle/);
    assert.doesNotMatch(html, /Grundschule/);
    assert.doesNotMatch(html, /Familienkonto/);
  });
});

test("facts view renders verify affordance for proposed canonical facts", async () => {
  await withViewServer(async (server) => {
    globalThis.__DOCS7_VIEW_TEST_DOCS__ = [iljaDoc];
    globalThis.__DOCS7_VIEW_TEST_STORE__ = {
      state: {
        person: "Ilja Stehle",
        stats: { factsVerified: 0, factsTotal: 1 },
        recentDocuments: [iljaDoc],
      },
      openDoc: () => {},
      refresh: async () => {},
      toast: () => {},
      documentsByScope: {
        current: { items: [iljaDoc], nextCursor: null, loaded: true, loading: false, error: null },
      },
      loadDocuments: async () => [iljaDoc],
    };
    const { default: Fakten } = await server.ssrLoadModule("/src/views/Fakten.jsx");

    const html = renderToStaticMarkup(React.createElement(Fakten));

    assert.match(html, /Steuer-ID/);
    assert.match(html, /Bestätigen/);
  });
});

test("family source calls entities API and no longer derives members from documents", async () => {
  await withViewServer(async (server) => {
    const source = await fs.readFile(path.join(clientRoot, "src", "views", "Familie.jsx"), "utf8");

    assert.match(source, /listEntities\(\{ kind: "person" \}\)/);
    assert.match(source, /EntityCardDetail/);
    assert.doesNotMatch(source, /factsFromDocuments|listAllDocuments/);
  });
});

test("facts helper renders one card for one current fact with multiple supporting documents", async () => {
  await withRealViewServer(async (server) => {
    const { factsFromDocuments } = await server.ssrLoadModule("/src/lib.jsx");
    const facts = factsFromDocuments([
      {
        id: "doc-wallet-a",
        person: "Ilja Stehle",
        created_at: "2026-06-01T10:00:00Z",
        facts: [
          {
            id: "raw-address-a",
            person: "Ilja Stehle",
            category: "address",
            key: "address",
            label: "Adresse",
            value: "Musterstr. 1",
            status: "proposed",
            source_doc_id: "doc-wallet-a",
            verification_id: "canonical-address",
            verification_status: "verified",
            verification_updated_at: "2026-07-01T08:00:00Z",
          },
        ],
      },
      {
        id: "doc-wallet-b",
        person: "Ilja Stehle",
        created_at: "2026-06-02T10:00:00Z",
        facts: [
          {
            id: "raw-address-b",
            person: "Ilja Stehle",
            category: "address",
            key: "address",
            label: "Adresse",
            value: "Musterstr. 1",
            status: "proposed",
            source_doc_id: "doc-wallet-b",
            verification_id: "canonical-address",
            verification_status: "verified",
            verification_updated_at: "2026-07-01T08:00:00Z",
          },
        ],
      },
    ]);

    assert.equal(facts.length, 1);
    assert.equal(facts[0].id, "canonical-address");
    assert.equal(facts[0].source_doc_id, "doc-wallet-a");
  });
});

test("hash routes resolve to the matching client view", async () => {
  await withRealViewServer(async (server) => {
    const { routeFromHash } = await server.ssrLoadModule("/src/lib.jsx");

    const expectedRoutes = {
      "#/uebersicht": "dashboard",
      "#/aufnehmen": "capture",
      "#/formulare": "forms",
      "#/assistent": "assistant",
      "#/aufgaben": "tasks",
      "#/dokumente": "documents",
      "#/fakten": "facts",
      "#/datenbank": "database",
      "#/familie": "family",
      "#/personen-objekte": "entities",
      "#/einblicke": "insights",
      "#/verlauf": "history",
    };

    for (const [hash, view] of Object.entries(expectedRoutes)) {
      assert.deepEqual(routeFromHash(hash), { view, activeDocId: null });
    }
  });
});

test("unknown hash routes fall back to the dashboard", async () => {
  await withRealViewServer(async (server) => {
    const { routeFromHash } = await server.ssrLoadModule("/src/lib.jsx");

    assert.deepEqual(routeFromHash("#/gibt-es-nicht"), { view: "dashboard", activeDocId: null });
    assert.deepEqual(routeFromHash("#fakten"), { view: "dashboard", activeDocId: null });
    assert.deepEqual(routeFromHash("#/fakten/extra"), { view: "dashboard", activeDocId: null });
    assert.deepEqual(routeFromHash("#/dokumente/"), { view: "dashboard", activeDocId: null });
  });
});

test("redundant navigation recognizes hashes already resolved to the same route", async () => {
  await withRealViewServer(async (server) => {
    const { hashMatchesRoute } = await server.ssrLoadModule("/src/lib.jsx");

    assert.equal(hashMatchesRoute("", "dashboard"), true);
    assert.equal(hashMatchesRoute("#/gibt-es-nicht", "dashboard"), true);
    assert.equal(hashMatchesRoute("#/fakten", "facts"), true);
    assert.equal(hashMatchesRoute("#/dokumente/doc-a", "documents", "doc-a"), true);
    assert.equal(hashMatchesRoute("#/dokumente/doc-a", "documents"), false);
  });
});

test("document hash routes resolve the drawer deep link", async () => {
  await withRealViewServer(async (server) => {
    const { hashForRoute, routeFromHash } = await server.ssrLoadModule("/src/lib.jsx");
    const docId = "doc/mit leerzeichen";
    const hash = hashForRoute("documents", docId);

    assert.equal(hash, "#/dokumente/doc%2Fmit%20leerzeichen");
    assert.deepEqual(routeFromHash(hash), { view: "documents", activeDocId: docId });
  });
});

test("document cache shares concurrent full-list requests", async () => {
  await withRealViewServer(async (server) => {
    const { createDocumentCache } = await server.ssrLoadModule("/src/lib.jsx");
    let release;
    let calls = 0;
    const cache = createDocumentCache(() => {
      calls += 1;
      return new Promise((resolve) => { release = resolve; });
    });

    const first = cache.loadAll("current");
    const second = cache.loadAll("current");
    assert.equal(calls, 1);

    release({ items: [{ id: "doc-a" }], nextCursor: null });
    const [firstItems, secondItems] = await Promise.all([first, second]);
    assert.deepEqual(firstItems, [{ id: "doc-a" }]);
    assert.deepEqual(secondItems, firstItems);
    assert.equal(calls, 1);
  });
});

test("document cache continues a full load from its cached page cursor", async () => {
  await withRealViewServer(async (server) => {
    const { createDocumentCache } = await server.ssrLoadModule("/src/lib.jsx");
    const cursors = [];
    const cache = createDocumentCache(async (_scope, cursor) => {
      cursors.push(cursor);
      return cursor
        ? { items: [{ id: "doc-b" }], nextCursor: null }
        : { items: [{ id: "doc-a" }], nextCursor: "page-2" };
    });

    await cache.loadNext("current");
    const items = await cache.loadAll("current");

    assert.deepEqual(cursors, [null, "page-2"]);
    assert.deepEqual(items.map(({ id }) => id), ["doc-a", "doc-b"]);
  });
});

test("document cache invalidation discards stale in-flight results", async () => {
  await withRealViewServer(async (server) => {
    const { createDocumentCache } = await server.ssrLoadModule("/src/lib.jsx");
    let release;
    let calls = 0;
    const cache = createDocumentCache(() => {
      calls += 1;
      if (calls === 1) return new Promise((resolve) => { release = resolve; });
      return Promise.resolve({ items: [{ id: "fresh" }], nextCursor: null });
    });

    const staleLoad = cache.loadAll("current");
    cache.invalidate();
    release({ items: [{ id: "stale" }], nextCursor: null });
    await staleLoad;
    assert.deepEqual(cache.snapshot().current.items, []);

    assert.deepEqual(await cache.loadAll("current"), [{ id: "fresh" }]);
  });
});

test("document cache starts a fresh page load immediately after invalidation", async () => {
  await withRealViewServer(async (server) => {
    const { createDocumentCache } = await server.ssrLoadModule("/src/lib.jsx");
    const releases = [];
    let calls = 0;
    const cache = createDocumentCache(() => {
      calls += 1;
      return new Promise((resolve) => { releases.push(resolve); });
    });

    const staleLoad = cache.loadNext("current");
    cache.invalidate();
    const freshLoad = cache.loadNext("current");
    assert.equal(calls, 2);

    releases[1]({ items: [{ id: "fresh" }], nextCursor: null });
    await freshLoad;
    releases[0]({ items: [{ id: "stale" }], nextCursor: null });
    await staleLoad;

    assert.deepEqual(cache.snapshot().current.items, [{ id: "fresh" }]);
    assert.equal(cache.snapshot().current.loaded, true);
  });
});

test("document-consuming views use the shared cache without private list fetches", async () => {
  const viewNames = ["Assistant", "DatabaseView", "Documents", "Einblicke", "Fakten", "Formulare"];
  for (const viewName of viewNames) {
    const source = await fs.readFile(path.join(clientRoot, "src", "views", `${viewName}.jsx`), "utf8");
    assert.doesNotMatch(source, /api\.list(?:All)?Documents/);
    assert.match(source, /documentsByScope/);
  }
});

// Shared context, hooks, formatting helpers, icon maps and tiny primitives.
import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import {
  Receipt, Home, Briefcase, HeartPulse, ShieldCheck, Landmark, Users, Building2, Archive,
  FileText, Check, CreditCard, IdCard, MapPin, Building, Stethoscope, Banknote, User, ListPlus,
} from "lucide-react";
import { api } from "./api.js";
export { ENTITY_KIND_LABELS, IDENTIFIER_KIND_LABELS } from "./entity-labels.js";

/* ---------- formatting ---------- */
const deNum = new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" });
export const fmtEUR = (n, cur = "EUR") =>
  typeof n === "number" ? (cur === "EUR" ? deNum.format(n) : `${n.toLocaleString("de-DE")} ${cur}`) : "—";

export function fmtDate(iso, long = false) {
  if (!iso) return "—";
  const d = new Date(iso);
  if (isNaN(d)) return iso;
  return d.toLocaleDateString("de-DE", long
    ? { day: "numeric", month: "long", year: "numeric" }
    : { day: "2-digit", month: "2-digit", year: "numeric" });
}

export function relDays(days) {
  if (days === 0) return "heute fällig";
  if (days === 1) return "morgen fällig";
  if (days === -1) return "gestern";
  if (days > 1) return `in ${days} Tagen`;
  return `vor ${Math.abs(days)} Tagen`;
}

export const initials = (name = "") =>
  name.split(" ").map((p) => p[0]).slice(0, 2).join("").toUpperCase();

function normalizeDocumentFact(doc, fact, index, { preferVerificationId = false } = {}) {
  if (fact?.value == null || fact.value === "") return null;
  const key = fact.key || fact.label || `fact_${index}`;
  const category = fact.category || "other";
  const value = String(fact.value);
  const sourceDocId = fact.source_doc_id || doc.id;
  const person = fact.person || doc.person || "";
  const rawId = fact.id || `${doc.id}:${key}:${index}`;
  const verificationId = fact.verification_id || fact.verificationId || null;
  const verificationStatus = fact.verification_status || fact.verificationStatus || "";
  const verificationUpdatedAt =
    fact.verification_updated_at || fact.verificationUpdatedAt || "";
  return {
    id: preferVerificationId && verificationId ? verificationId : rawId,
    person,
    category,
    key,
    label: fact.label || key,
    value,
    raw_status: fact.status || "proposed",
    status: verificationStatus || fact.status || "proposed",
    source_doc_id: sourceDocId,
    updated_at: fact.updated_at || doc.created_at || "",
    verification_id: verificationId,
    verification_status: verificationStatus,
    verification_updated_at: verificationUpdatedAt,
    verifiable: fact.verifiable === false ? false : Boolean(verificationId || fact.id),
  };
}

export function factsFromDocuments(documents = []) {
  const facts = [];
  const seen = new Set();
  for (const doc of documents) {
    for (const [index, fact] of (doc.facts || []).entries()) {
      const normalized = normalizeDocumentFact(doc, fact, index, { preferVerificationId: true });
      if (!normalized) continue;
      const dedupe = normalized.verification_id
        || JSON.stringify([normalized.category, normalized.key, normalized.value, normalized.person]);
      if (seen.has(dedupe)) continue;
      seen.add(dedupe);
      facts.push(normalized);
    }
  }
  return facts;
}

/* ---------- icon maps ---------- */
export const FOLDER_ICONS = {
  Steuern: Receipt, Wohnen: Home, Arbeit: Briefcase, Gesundheit: HeartPulse,
  Versicherungen: ShieldCheck, Finanzen: Landmark, Familie: Users, "Behörden": Building2, Archiv: Archive,
};
export function FolderIcon({ name, size = 16, ...p }) {
  const I = FOLDER_ICONS[name] || FileText;
  return <I size={size} {...p} />;
}

export const FACT_ICONS = {
  identity: IdCard, address: MapPin, tax: Receipt, financial: CreditCard,
  insurance: ShieldCheck, employment: Building, health: Stethoscope,
  custom: ListPlus,
};
export const FACT_CAT_LABEL = {
  identity: "Identität", address: "Adresse", tax: "Steuer", financial: "Finanzen",
  insurance: "Versicherung", employment: "Beschäftigung", health: "Gesundheit",
  custom: "Weitere Angaben",
};
export function FactIcon({ category, size = 16, ...p }) {
  const I = FACT_ICONS[category] || User;
  return <I size={size} {...p} />;
}

/* ---------- tiny primitives ---------- */
export const Spinner = () => <span className="spinner" />;
export const Dots = () => <span className="dots"><span /><span /><span /></span>;

export function Tick({ verified }) {
  return (
    <span className={"tick" + (verified ? " verified" : "")} title={verified ? "Von dir bestätigt" : "Von der KI vorgeschlagen"}>
      <Check size={12} strokeWidth={3} />
    </span>
  );
}

export function Empty({ icon: Icon = FileText, title, sub, children }) {
  return (
    <div style={{ textAlign: "center", padding: "54px 20px", color: "var(--muted)" }}>
      <div style={{ width: 54, height: 54, borderRadius: 16, background: "var(--accent-soft)", color: "var(--accent)", display: "grid", placeItems: "center", margin: "0 auto 14px" }}>
        <Icon size={26} />
      </div>
      <div style={{ fontWeight: 620, color: "var(--ink)", fontSize: 15 }}>{title}</div>
      {sub && <div style={{ fontSize: 13, marginTop: 4, maxWidth: 340, marginInline: "auto" }}>{sub}</div>}
      {children && <div style={{ marginTop: 16 }}>{children}</div>}
    </div>
  );
}

/* ---------- global store ---------- */
const Ctx = createContext(null);
export const useStore = () => useContext(Ctx);

const VIEW_HASH_PATHS = {
  dashboard: "uebersicht",
  capture: "aufnehmen",
  forms: "formulare",
  assistant: "assistent",
  tasks: "aufgaben",
  documents: "dokumente",
  facts: "fakten",
  database: "datenbank",
  family: "familie",
  entities: "personen-objekte",
  insights: "einblicke",
  history: "verlauf",
};
const HASH_PATH_VIEWS = Object.fromEntries(
  Object.entries(VIEW_HASH_PATHS).map(([viewName, hashPath]) => [hashPath, viewName]),
);

export function routeFromHash(hash = "") {
  const rawHash = String(hash);
  if (!rawHash.startsWith("#/")) return { view: "dashboard", activeDocId: null };
  const path = rawHash.slice(2);
  const segments = path.split("/");
  const viewName = HASH_PATH_VIEWS[segments[0]];
  if (!viewName) return { view: "dashboard", activeDocId: null };
  if (viewName !== "documents") {
    return segments.length === 1
      ? { view: viewName, activeDocId: null }
      : { view: "dashboard", activeDocId: null };
  }
  if (segments.length === 1) return { view: "documents", activeDocId: null };
  if (segments.length !== 2 || !segments[1]) return { view: "dashboard", activeDocId: null };
  try {
    return { view: "documents", activeDocId: decodeURIComponent(segments[1]) };
  } catch {
    return { view: "dashboard", activeDocId: null };
  }
}

export function hashForRoute(viewName, activeDocId = null) {
  const hashPath = VIEW_HASH_PATHS[viewName] || VIEW_HASH_PATHS.dashboard;
  if (viewName === "documents" && activeDocId) {
    return `#/${hashPath}/${encodeURIComponent(activeDocId)}`;
  }
  return `#/${hashPath}`;
}

export function hashMatchesRoute(hash, viewName, activeDocId = null) {
  const currentRoute = routeFromHash(hash);
  const nextRoute = routeFromHash(hashForRoute(viewName, activeDocId));
  return currentRoute.view === nextRoute.view
    && currentRoute.activeDocId === nextRoute.activeDocId;
}

const emptyDocumentScope = () => ({
  items: [],
  nextCursor: null,
  loaded: false,
  loading: false,
  error: null,
});

const mergeDocuments = (current, incoming) => {
  const byId = new Map(current.map((document) => [document.id, document]));
  for (const document of incoming) byId.set(document.id, document);
  return [...byId.values()];
};

export function createDocumentCache(fetchPage, initialListener = () => {}) {
  let listener = initialListener;
  let scopes = { current: emptyDocumentScope(), all: emptyDocumentScope() };
  const inFlight = { current: null, all: null };
  const epochs = { current: 0, all: 0 };

  const scopeState = (scope) => {
    if (!Object.hasOwn(scopes, scope)) throw new Error(`Unknown document scope: ${scope}`);
    return scopes[scope];
  };
  const publish = (scope, next) => {
    scopes = { ...scopes, [scope]: next };
    listener(scopes);
    return next;
  };

  const loadNext = async (scope = "current") => {
    const current = scopeState(scope);
    if (current.loaded && !current.nextCursor) return current;
    if (inFlight[scope]) return inFlight[scope];

    const cursor = current.loaded ? current.nextCursor : null;
    const requestEpoch = epochs[scope];
    publish(scope, { ...current, loading: true, error: null });

    let request;
    try {
      request = Promise.resolve(fetchPage(scope, cursor));
    } catch (error) {
      request = Promise.reject(error);
    }
    const flight = request.then(
      (page) => {
        if (requestEpoch !== epochs[scope]) return scopeState(scope);
        const pageItems = Array.isArray(page?.items) ? page.items : [];
        return publish(scope, {
          items: cursor ? mergeDocuments(current.items, pageItems) : pageItems,
          nextCursor: page?.nextCursor || null,
          loaded: true,
          loading: false,
          error: null,
        });
      },
      (error) => {
        if (requestEpoch === epochs[scope]) {
          publish(scope, { ...scopeState(scope), loading: false, error });
        }
        throw error;
      },
    );
    inFlight[scope] = flight;
    try {
      return await flight;
    } finally {
      if (inFlight[scope] === flight) inFlight[scope] = null;
    }
  };

  const loadAll = async (scope = "current") => {
    const requestEpoch = epochs[scope];
    while (requestEpoch === epochs[scope]) {
      const current = scopeState(scope);
      if (current.loaded && !current.nextCursor) return current.items;
      await loadNext(scope);
    }
    return scopeState(scope).items;
  };

  const invalidate = (scopeNames = ["current", "all"]) => {
    for (const scope of scopeNames) {
      scopeState(scope);
      epochs[scope] += 1;
      inFlight[scope] = null;
      scopes = { ...scopes, [scope]: emptyDocumentScope() };
    }
    listener(scopes);
  };

  return {
    snapshot: () => scopes,
    setListener: (nextListener = () => {}) => { listener = nextListener; },
    loadNext,
    loadAll,
    invalidate,
  };
}

const fetchDocumentPage = (scope, cursor) => api.listDocuments(scope, cursor);

export function StoreProvider({ children }) {
  const initialRoute = routeFromHash(typeof window === "undefined" ? "" : window.location.hash);
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [documentCache] = useState(() => createDocumentCache(fetchDocumentPage));
  const [documentsByScope, setDocumentsByScope] = useState(() => documentCache.snapshot());
  const [view, setViewState] = useState(initialRoute.view);
  const [activeDocId, setActiveDocId] = useState(initialRoute.activeDocId);
  const [toasts, setToasts] = useState([]);
  const [pendingAsk, setPendingAsk] = useState(null); // dashboard → assistant quick-ask
  const [reviewInboxOpen, setReviewInboxOpen] = useState(false);
  const [activeEntityId, setActiveEntityId] = useState(null);

  useEffect(() => {
    documentCache.setListener(setDocumentsByScope);
    return () => documentCache.setListener();
  }, [documentCache]);

  const invalidateDocuments = useCallback(
    (scopes) => documentCache.invalidate(scopes),
    [documentCache],
  );
  const loadDocuments = useCallback(
    (scope = "current") => documentCache.loadAll(scope),
    [documentCache],
  );
  const loadMoreDocuments = useCallback(
    (scope = "current") => documentCache.loadNext(scope),
    [documentCache],
  );
  const applyState = useCallback((s) => {
    if (!s) return;
    documentCache.invalidate();
    setState(s);
  }, [documentCache]);
  const refresh = useCallback(async () => {
    documentCache.invalidate();
    const s = await api.summary();
    setState(s); return s;
  }, [documentCache]);

  useEffect(() => { refresh().finally(() => setLoading(false)); }, [refresh]);

  const navigate = useCallback((nextView, nextDocId = null, { replace = false } = {}) => {
    const nextHash = hashForRoute(nextView, nextDocId);
    const nextRoute = routeFromHash(nextHash);
    const routeAlreadyActive = typeof window !== "undefined"
      && hashMatchesRoute(window.location.hash, nextView, nextDocId);
    setViewState(nextRoute.view);
    setActiveDocId(nextRoute.activeDocId);
    if (typeof window === "undefined" || routeAlreadyActive) return;
    if (replace) {
      window.history.replaceState(
        null,
        "",
        `${window.location.pathname}${window.location.search}${nextHash}`,
      );
    } else {
      window.location.hash = nextHash;
    }
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return undefined;
    const syncFromHash = () => {
      const nextRoute = routeFromHash(window.location.hash);
      setViewState(nextRoute.view);
      setActiveDocId(nextRoute.activeDocId);
    };
    window.addEventListener("hashchange", syncFromHash);
    return () => window.removeEventListener("hashchange", syncFromHash);
  }, []);

  const toast = useCallback((message, kind = "ok") => {
    const id = Math.random().toString(36).slice(2);
    setToasts((t) => [...t, { id, message, kind }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 2600);
  }, []);

  const setView = useCallback((nextView) => navigate(nextView), [navigate]);
  const openDoc = useCallback((id) => { if (id) navigate("documents", id); }, [navigate]);
  const closeDoc = useCallback(() => navigate("documents", null, { replace: true }), [navigate]);

  const askDocuments = useCallback((q) => { setPendingAsk(q); setView("assistant"); }, []);
  const openReviewInbox = useCallback(() => setReviewInboxOpen(true), []);
  const closeReviewInbox = useCallback(() => setReviewInboxOpen(false), []);
  const openEntity = useCallback((id) => { setActiveEntityId(id); setView("entities"); }, []);
  const closeEntity = useCallback(() => setActiveEntityId(null), []);

  const value = { state, loading, view, setView, refresh, applyState, documentsByScope, loadDocuments, loadMoreDocuments, invalidateDocuments, openDoc, closeDoc, activeDocId, toast, toasts, pendingAsk, setPendingAsk, askDocuments, reviewInboxOpen, openReviewInbox, closeReviewInbox, activeEntityId, openEntity, closeEntity };
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

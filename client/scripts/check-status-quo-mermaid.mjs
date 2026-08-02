import { readdir, readFile } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const MERMAID_FENCE = /^```mermaid[ \t]*\r?\n([\s\S]*?)^```[ \t]*$/gm;

async function markdownFiles(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await markdownFiles(path));
    else if (entry.isFile() && entry.name.endsWith(".md")) files.push(path);
  }
  return files.sort();
}

export function extractMermaidBlocks(markdown) {
  return [...markdown.matchAll(MERMAID_FENCE)].map((match) => match[1].trim());
}

export async function validateMermaidCorpus(repositoryRoot) {
  const corpusRoot = resolve(repositoryRoot, "docs/status-quo");
  const { JSDOM } = await import("jsdom");
  const dom = new JSDOM("<!doctype html><html><body></body></html>");
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.navigator = dom.window.navigator;

  const { default: mermaid } = await import("mermaid");
  mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });

  const errors = [];
  let count = 0;
  for (const path of await markdownFiles(corpusRoot)) {
    const markdown = await readFile(path, "utf8");
    const blocks = extractMermaidBlocks(markdown);
    for (const [index, definition] of blocks.entries()) {
      count += 1;
      try {
        await mermaid.parse(definition);
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        errors.push(`${relative(repositoryRoot, path)}: Mermaid block ${index + 1}: ${message}`);
      }
    }
  }

  dom.window.close();
  return { count, errors };
}

async function main() {
  const scriptDirectory = dirname(fileURLToPath(import.meta.url));
  const defaultRoot = resolve(scriptDirectory, "../..");
  const flagIndex = process.argv.indexOf("--repo-root");
  const repositoryRoot = flagIndex >= 0 ? resolve(process.argv[flagIndex + 1]) : defaultRoot;
  const result = await validateMermaidCorpus(repositoryRoot);
  for (const error of result.errors) console.error(error);
  if (result.errors.length) process.exitCode = 1;
  else console.log(`Validated ${result.count} Mermaid diagrams.`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  await main();
}

<template>
  <Spinner class="w-16" v-if="isStarting" />

  <div v-else class="flex flex-col gap-4 m-8 items-center">
    <div>
      reStructuredText:
      <button @click="rerunPreview" class="border w-16 bg-slate-600 text-white ml-8">Run</button>
    </div>
    <textarea v-model="snippet" class="bg-slate-200 font-mono h-100 w-3/4"></textarea>

    Output raw HTML:
    <textarea v-model="outputRaw" class="bg-slate-200 font-mono h-100 w-3/4"></textarea>

    Output rendered HTML:
    <div ref="outputHtml" class="prose max-w-none overflow-auto bg-slate-200 font-mono h-100 w-3/4"></div>

    Status:
    <textarea v-model="status" class="bg-slate-200 font-mono h-50 w-3/4"></textarea>

    Warnings:
    <textarea v-model="warnings" class="bg-slate-200 font-mono h-50 w-3/4"></textarea>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, useTemplateRef } from "vue";
import Spinner from "./components/Spinner.vue";
import {
  loadPyodide,
  version as pyodideVersion,
  type PyodideAPI,
} from "pyodide";
import whlUrl from "./assets/sphinx_preview-0.1.0-py3-none-any.whl?url";
import type { ISphinxPreview } from "./sphinx-preview.d.ts";

const isStarting = ref(true);

const snippet = ref("Hello\n=====\nHow **are** you, *guys*?");
const outputRaw = ref("");
const outputHtml = useTemplateRef("outputHtml")
const status = ref("");
const warnings = ref("");

let pyodide: PyodideAPI | undefined = undefined;
let sphinxpreview: ISphinxPreview | undefined = undefined;
const whl_filename = whlUrl.split("/").pop()!; // Get the last part, e.g., "sphinx_preview-0.1.0-py3-none-any.whl"
const srcdir = "/srcdir/";
const confdir = srcdir;
const outdir = "/outdir/";

onMounted(async () => {
  // Load Pyodide
  pyodide = await loadPyodide({
    indexURL: `https://cdn.jsdelivr.net/pyodide/v${pyodideVersion}/full/`,
  });

  // Download wheel and copy it to Emscripten FS
  const resp = await fetch(whlUrl);
  const data = new Uint8Array(await resp.arrayBuffer());
  pyodide.FS.writeFile(whl_filename, data);

  // Install using micropip and import the package
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("emfs:" + whl_filename);
  sphinxpreview = pyodide.pyimport("sphinx_preview");

  isStarting.value = false;
});

function rerunPreview() {
  if (!pyodide || !sphinxpreview) return;

  // (Re-)create Sphinx project
  rmdirRecursive(pyodide, srcdir);
  [srcdir, confdir, outdir].forEach((path) => pyodide!.FS.mkdirTree(path));
  pyodide.FS.writeFile(srcdir + "index.rst", snippet.value);
  pyodide.FS.writeFile(srcdir + "conf.py", "");

  // Run
  const { status: sphinxStatus, warnings: sphinxWarnings } = sphinxpreview
    .SphinxPreview(srcdir, confdir, outdir)
    .build();

  // @ts-expect-error
  const html = pyodide.FS.readFile(outdir + "index.html", { encoding: "utf8" });

  outputRaw.value = html;
  outputHtml.value!.innerHTML = html

  status.value = sphinxStatus;
  warnings.value = sphinxWarnings;
}

function rmdirRecursive(pyodide: PyodideAPI, path: string): void {
  const fs = pyodide.FS

  // If path doesn't exist, do nothing
  try {
    fs.stat(path)
  } catch {
    return
  }

  // If path is a file, delete it
  if (!fs.isDir(fs.stat(path).mode)) {
    fs.unlink(path);
    return;
  }

  const entries: string[] = fs.readdir(path).filter(
    (name) => name !== "." && name !== ".."
  );

  for (const entry of entries) {
    rmdirRecursive(pyodide, path + "/" + entry);
  }

  fs.rmdir(path);
}
</script>

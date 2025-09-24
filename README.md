# Sphinx reStructuredText/Markdown preview in a browser HOWTO

_If you are looking for editing, previewing Sphinx try https://snippets.documatt.com._

Minimal but realistic demonstration of running full-blown Python entirely inside your browser. Powered by WebAssembly Pyodide and Vue for front-end.

🚧 Detail tutorial will come soon. [Follow me on socials](https://liborjelinek.github.io) to don't miss updates. 🚧

## What we will be doing

In this tutorial, I wish to show how to build simple but complete example of running complex Python toolchain entirely in a browser. I will create two apps:

- Python app embedding Sphinx documentation generator producing a bunch of HTML files from reStructuredText
- Vue.js app with a UI to enter text, run Python, and display output HTML

I want to build a real-world app. Pyodide makes executing a short Python snippets a breeze, but I want to install and run in browser a more realistic app.

For my case, I will wrap Sphinx into a simple API and build it to wheel (.whl) distribution format.

At browser side, I will boot Python interpreter, install wheel, and call my app. Simple UI to enter text, Run button, and view output, will be coded with Vue.js and Tailwind CSS.

## Python

1. mkdir py-sphinx-preview
2. uv init
3. uv add sphinx
4. Folder structure (src layout)
5. do `__init__.py` přidat naší classu
6. turn into library (add [build-system] to pyproject.toml)
7. uv build

## JS

1. npx vue create
2. add tailwind (with typography)
3. code ui
4. boot pyodide
5. install our whl
6. run Python to preview
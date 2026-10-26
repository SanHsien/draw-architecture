#!/usr/bin/env node
// Assembles a canvas HTML file from the bundled template + a scene.js data file.
//
// Usage:
//   node build.js --scene scene.js --out out/index.html \
//     --title "Acme — platform architecture" \
//     --kicker "ACME — PLATFORM ARCHITECTURE" \
//     --sub "<b>ingest</b> → <b>process</b> → <b>serve</b>" \
//     --slug acme-architecture

'use strict';
const fs = require('fs');
const path = require('path');

function arg(name, fallback) {
  const i = process.argv.indexOf('--' + name);
  if (i === -1 || i === process.argv.length - 1) {
    if (fallback !== undefined) return fallback;
    console.error('missing required argument: --' + name);
    process.exit(1);
  }
  return process.argv[i + 1];
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
  );
}

function escapeJsSingleQuoted(s) {
  return String(s)
    .replace(/\\/g, '\\\\')
    .replace(/'/g, "\\'")
    // `<` as an escape keeps `</script>` (and `<!--`) from ending the script
    // element; the JS string still evaluates to the same characters.
    .replace(/</g, '\\x3c')
    .replace(/\r|\n|\u2028|\u2029/g, '');
}

const scenePath = arg('scene');
const outPath = arg('out');
const title = arg('title');
const kicker = arg('kicker', title.toUpperCase());
const sub = arg('sub', '');
const slug = arg('slug', title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''));

const template = fs.readFileSync(path.join(__dirname, '..', 'assets', 'template.html'), 'utf8');
const scene = fs.readFileSync(scenePath, 'utf8');

if (/<\/script/i.test(scene)) {
  console.error('scene contains </script> which would break out of the canvas template');
  process.exit(1);
}

// One pass with a function replacer: a string replacement would expand `$&`,
// `$'` and `$$` inside values, and chained replaces would let a value that
// contains `{{SCENE}}` steal the next slot.
const values = {
  TITLE: escapeHtml(title),
  KICKER: escapeHtml(kicker),
  SUB_HTML: sub,
  SLUG: escapeJsSingleQuoted(slug),
  SCENE: scene
};
const html = template.replace(
  /\{\{(TITLE|KICKER|SUB_HTML|SLUG|SCENE)\}\}/g,
  (_, key) => values[key]
);

fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
fs.writeFileSync(outPath, html);
console.log('wrote ' + outPath + ' (' + html.length + ' bytes)');

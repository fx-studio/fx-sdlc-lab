'use strict';
// Words the customer sees, and the page's external references. AC24, AC26.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const backup = require('../app/backup.js');
const { readIndexHtml } = require('./helpers.js');

// Text a customer can see or hear from index.html: element text plus labels read by screen readers.
function visibleText(html) {
  const noCode = html
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<(script|style)\b[\s\S]*?<\/\1\s*>/gi, ' ');
  const attrs = [];
  for (const m of noCode.matchAll(/\b(aria-label|title|placeholder|alt)\s*=\s*(?:"([^"]*)"|'([^']*)')/gi)) {
    attrs.push(m[2] !== undefined ? m[2] : m[3]);
  }
  return [noCode.replace(/<[^>]*>/g, ' '), ...attrs].join('\n');
}

test('AC24: no new customer-facing text contains "localStorage", "JSON" or "console"', () => {
  const texts = [];
  for (const [key, value] of Object.entries(backup.MESSAGES)) {
    assert.equal(typeof value, 'string', `MESSAGES.${key} is a sentence`);
    texts.push([`MESSAGES.${key}`, value]);
    texts.push([`MESSAGES.${key} filled`, backup.fill(value, { n: 12, m: 30 })]);
  }
  for (const args of [
    { readError: false, current: 12, incoming: 30 },
    { readError: false, current: 1, incoming: 30 },
    { readError: true, current: 0, incoming: 30 },
    { readError: true, current: 3, incoming: 30 },
  ]) {
    const q = backup.confirmText(args);
    if (q !== null) texts.push([`confirmText(${JSON.stringify(args)})`, q]);
  }
  texts.push(['index.html', visibleText(readIndexHtml())]);

  for (const [where, text] of texts) {
    // A11: the ".json" ending of the file name is shown by the OS and does not count.
    const checked = String(text).replace(/\.json\b/gi, '');
    // AMBIGUOUS: the spec lists the words with this casing; any casing is treated as the same technical word.
    const hit = checked.match(/localStorage|JSON|console/i);
    assert.equal(hit, null, `${where} contains "${hit && hit[0]}"`);
  }
});

test('AC26: app/index.html has no <script> or <link> pointing outside the app', () => {
  const html = readIndexHtml().replace(/<!--[\s\S]*?-->/g, ' ');
  const external = (url) => /^(\/\/|[a-z][a-z0-9+.-]*:)/i.test(url.trim()) && !/^data:/i.test(url.trim());
  const found = [];
  for (const m of html.matchAll(/<script\b[^>]*\bsrc\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi)) {
    const url = m[1] ?? m[2] ?? m[3];
    if (external(url)) found.push(`<script src="${url}">`);
  }
  for (const m of html.matchAll(/<link\b[^>]*\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi)) {
    const url = m[1] ?? m[2] ?? m[3];
    if (external(url)) found.push(`<link href="${url}">`);
  }
  // AMBIGUOUS: AC26 says no *added* external <script>/<link>; without the previous index.html to diff
  // against, the test requires none at all, which policy-security@1#S4 also implies.
  assert.deepEqual(found, []);
});

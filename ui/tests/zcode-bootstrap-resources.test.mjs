import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { readFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ui = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const root = resolve(ui, '..');
const name = JSON.parse(await readFile(join(root, 'plugin.json'), 'utf8')).name;

test('ZCode 从实际 MCP 资源列表发现可后台保留的 WASM 面板', async () => {
  const child = spawn(process.execPath, [join(ui, 'bootstrap.mjs')], {
    cwd: root,
    env: { ...process.env, ZCODE_PLUGIN_ROOT: root, ZCODE_PROJECT_DIR: root },
    stdio: ['pipe', 'pipe', 'pipe'],
  });
  const pending = new Map();
  createInterface({ input: child.stdout }).on('line', line => {
    const message = JSON.parse(line);
    const waiter = pending.get(message.id);
    if (waiter) { pending.delete(message.id); waiter(message); }
  });
  const request = (id, method, params = {}) => new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`${method} timed out`)); }, 10000);
    pending.set(id, value => { clearTimeout(timer); resolve(value); });
    child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
  try {
    assert.ok((await request(1, 'initialize', {
      protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'zcode-resource-test', version: '1' },
    })).result);
    const response = await request(2, 'resources/list');
    const panel = response.result.resources.find(resource => resource.uri === `ui://${name}/panel.html`);
    assert.ok(panel, 'panel resource is discoverable');
    assert.equal(panel._meta?.ui?.backgroundRetention, true);
    assert.equal(panel._meta?.['zcode/csp']?.wasmUnsafeEval, true);
  } finally {
    child.kill();
    await new Promise(resolve => child.once('exit', resolve));
  }
});

import test from 'node:test';
import assert from 'node:assert/strict';
import { alignZcodeResponse } from '../zcode-parity.mjs';

test('面板保留 ZCode 的后台驻留与 WASM CSP，且不覆盖其他元数据', () => {
  const source = { contents: [{ uri: 'ui://photocraft/panel.html', _meta: { ui: { custom: true } } }] };
  const result = alignZcodeResponse('resources/read', { uri: 'ui://photocraft/panel.html' }, source, 'photocraft');
  assert.deepEqual(result.contents[0]._meta, {
    ui: { custom: true, prefersBorder: false, backgroundRetention: true },
    'zcode/csp': { wasmUnsafeEval: true },
  });
  assert.equal(source.contents[0]._meta.ui.backgroundRetention, undefined);
});

test('只有真实任务轮询才标记后台活动', () => {
  const pending = { structuredContent: { request: null } };
  assert.equal(alignZcodeResponse('tools/call', { name: '_editor_poll' }, pending, 'photocraft'), pending);
  const active = alignZcodeResponse('tools/call', { name: '_editor_poll' }, { structuredContent: { request: { id: '1' } } }, 'photocraft');
  assert.equal(active._meta['zcode/activity'], true);
});

test('资源列表中的面板声明也带后台驻留元数据', () => {
  const result = alignZcodeResponse('resources/list', {}, { resources: [
    { uri: 'ui://photocraft/panel.html' }, { uri: 'ui://photocraft/assets.json' },
  ] }, 'photocraft');
  assert.equal(result.resources[0]._meta.ui.backgroundRetention, true);
  assert.equal(result.resources[1]._meta, undefined);
});

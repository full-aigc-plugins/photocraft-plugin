import test from 'node:test';
import assert from 'node:assert/strict';
import { authorizeRequest, workspacePath } from '../security.mjs';
test('拒绝缺少令牌及外站来源', () => {
 const origin='http://127.0.0.1:12345';
 assert.equal(authorizeRequest({headers:{host:'127.0.0.1:12345'}},origin,'token',''),false);
 assert.equal(authorizeRequest({headers:{host:'127.0.0.1:12345',origin:'https://evil.example'}},origin,'token','token'),false);
 assert.equal(authorizeRequest({headers:{host:'evil.example'}},origin,'token','token'),false);
 assert.equal(authorizeRequest({headers:{host:'127.0.0.1:12345',origin}},origin,'token','token'),true);
});
test('必须明确工作区绝对路径', () => {
 assert.throws(()=>workspacePath('relative'));
 assert.equal(workspacePath('/tmp'),'/tmp');
});

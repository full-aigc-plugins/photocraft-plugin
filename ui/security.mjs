import { timingSafeEqual } from 'node:crypto';
import { isAbsolute, resolve } from 'node:path';
export function authorizeRequest(request, origin, expected, actual) {
 const a=Buffer.from(expected), b=Buffer.from(actual || '');
 return request.headers.host === new URL(origin).host && (!request.headers.origin || request.headers.origin === origin) && a.length === b.length && timingSafeEqual(a,b);
}
export function workspacePath(value) {
 if (!value || !isAbsolute(value)) throw new Error('请通过 workspace 参数或 CRAFT_WORKSPACE_ROOT 指定工作区绝对路径');
 return resolve(value);
}

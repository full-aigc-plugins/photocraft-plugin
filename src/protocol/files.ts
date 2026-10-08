import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, realpathSync } from 'node:fs';
import { dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import { strictJson } from './strict_json.ts';

/** 将 JSON 内容规范化，数字必须有限，属性顺序不影响身份。 */
export function canonical(value: any): string {
  if (typeof value === 'number' && !Number.isFinite(value)) throw new Error('nonfinite_json_value');
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  if (value !== null && typeof value === 'object') {
    return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
  }
  const encoded = JSON.stringify(value);
  if (encoded === undefined) throw new Error('invalid_json_value');
  return encoded;
}

export const digest = (value: string | Buffer) => createHash('sha256').update(value).digest('hex');
export const readJson = (path: string) => strictJson(readFileSync(safePath(path), 'utf8'));
export const fileDigest = (path: string) => digest(readFileSync(safePath(path)));

/** 拒绝任意路径段的符号链接；允许最终目标尚未创建。 */
export function safePath(path: string): string {
  if (typeof path !== 'string' || !isAbsolute(path)) throw new Error('absolute_path_required');
  const target = resolve(path); let current = target;
  while (true) {
    if (existsSync(current) || (() => { try { return lstatSync(current).isSymbolicLink(); } catch { return false; } })()) {
      if (lstatSync(current).isSymbolicLink()) throw new Error('symlink_not_allowed');
    }
    const parent = dirname(current); if (parent === current) break; current = parent;
  }
  return target;
}

export function within(path: string, root: string): string {
  const target = safePath(path); const base = realpathSync(safePath(root));
  const child = relative(base, target);
  if (!child || child === '..' || child.startsWith('..' + sep) || isAbsolute(child)) throw new Error('path_outside_authorization');
  return target;
}

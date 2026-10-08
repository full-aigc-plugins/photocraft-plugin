import { validationError } from './operation_error.ts';

/** 拒绝重复键和非有限值，保留数组及特殊键的完整字段位置。 */
export function strictJson(text: string): any {
  let offset = 0;
  const space = () => { while (/[ \t\r\n]/.test(text[offset] ?? '') && offset < text.length) offset++; };
  const string = (path:string) => {
    const start = offset++;
    while (offset < text.length) {
      if (text[offset] === '\\') { offset += 2; continue; }
      if (text[offset++] === '"') {
        try {return JSON.parse(text.slice(start, offset));}
        catch {throw validationError('invalid_json_string',path);}
      }
    }
    throw validationError('invalid_json_string',path);
  };
  const value = (depth = 0,path='$'): any => {
    if (depth > 128) throw validationError('json_depth_limit',path);
    space(); const token = text[offset];
    if (token === '"') return string(path);
    if (token === '{') {
      offset++; space(); const result: Record<string, any> = {}; const seen = new Set<string>();
      if (text[offset] === '}') { offset++; return result; }
      while (true) {
        space(); if (text[offset] !== '"') throw validationError('invalid_json_object',path);
        const key = string(path);const child=/^[A-Za-z_][A-Za-z0-9_]*$/.test(key)?path+'.'+key:path+'['+JSON.stringify(key)+']';
        if (seen.has(key)) throw validationError('duplicate_json_key',child,'duplicate_json_key: '+key);
        seen.add(key); space(); if (text[offset++] !== ':') throw validationError('invalid_json_object',child);
        Object.defineProperty(result, key, { value: value(depth + 1,child), enumerable: true, writable: true });
        space(); const delimiter = text[offset++];
        if (delimiter === '}') return result;
        if (delimiter !== ',') throw validationError('invalid_json_object',path);
      }
    }
    if (token === '[') {
      offset++; space(); const result = [];
      if (text[offset] === ']') { offset++; return result; }
      while (true) {
        result.push(value(depth + 1,path+'['+result.length+']')); space(); const delimiter = text[offset++];
        if (delimiter === ']') return result;
        if (delimiter !== ',') throw validationError('invalid_json_array',path);
      }
    }
    const literal = /^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(text.slice(offset));
    if (!literal) throw validationError('invalid_json_value',path);
    offset += literal[0].length; const result = JSON.parse(literal[0]);
    if (typeof result === 'number' && !Number.isFinite(result)) throw validationError('nonfinite_json_value',path);
    return result;
  };
  const result = value(); space();
  if (offset !== text.length) throw validationError('invalid_json_trailing_content');
  return result;
}

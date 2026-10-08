/** 拒绝重复键和非有限值，避免计划、账本与评估回执的歧义。 */
export function strictJson(text: string): any {
  let offset = 0;
  const space = () => { while (/[ \t\r\n]/.test(text[offset] ?? '') && offset < text.length) offset++; };
  const string = () => {
    const start = offset++;
    while (offset < text.length) {
      if (text[offset] === '\\') { offset += 2; continue; }
      if (text[offset++] === '"') return JSON.parse(text.slice(start, offset));
    }
    throw new Error('invalid_json_string');
  };
  const value = (depth = 0): any => {
    if (depth > 128) throw new Error('json_depth_limit');
    space(); const token = text[offset];
    if (token === '"') return string();
    if (token === '{') {
      offset++; space(); const result: Record<string, any> = {}; const seen = new Set<string>();
      if (text[offset] === '}') { offset++; return result; }
      while (true) {
        space(); if (text[offset] !== '"') throw new Error('invalid_json_object');
        const key = string(); if (seen.has(key)) throw new Error('duplicate_json_key: ' + key);
        seen.add(key); space(); if (text[offset++] !== ':') throw new Error('invalid_json_object');
        Object.defineProperty(result, key, { value: value(depth + 1), enumerable: true, writable: true });
        space(); const delimiter = text[offset++];
        if (delimiter === '}') return result;
        if (delimiter !== ',') throw new Error('invalid_json_object');
      }
    }
    if (token === '[') {
      offset++; space(); const result = [];
      if (text[offset] === ']') { offset++; return result; }
      while (true) {
        result.push(value(depth + 1)); space(); const delimiter = text[offset++];
        if (delimiter === ']') return result;
        if (delimiter !== ',') throw new Error('invalid_json_array');
      }
    }
    const literal = /^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(text.slice(offset));
    if (!literal) throw new Error('invalid_json_value');
    offset += literal[0].length; const result = JSON.parse(literal[0]);
    if (typeof result === 'number' && !Number.isFinite(result)) throw new Error('nonfinite_json_value');
    return result;
  };
  const result = value(); space();
  if (offset !== text.length) throw new Error('invalid_json_trailing_content');
  return result;
}

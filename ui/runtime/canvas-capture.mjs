// 保留 WebGL 帧缓冲，供 MCP 在下一帧之外读取当前可见画面。
export function installCanvasCapture(Canvas) {
 const original = Canvas.prototype.getContext;
 Canvas.prototype.getContext = function (kind, options, ...rest) {
  const captured = kind === 'webgl' || kind === 'webgl2' || kind === 'experimental-webgl';
  return original.call(this, kind, captured ? {...options, preserveDrawingBuffer: true} : options, ...rest);
 };
}

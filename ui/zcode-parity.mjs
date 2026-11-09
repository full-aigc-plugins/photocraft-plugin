// 保留增强版编辑器，同时补齐 ZCode 面板的宿主协议元数据。
export function alignZcodeResponse(method, params, result, name) {
  const panelUri = `ui://${name}/panel.html`;
  const panelMetadata = meta => ({
    ...meta,
    ui: { ...meta?.ui, prefersBorder: false, backgroundRetention: true },
    'zcode/csp': { ...meta?.['zcode/csp'], wasmUnsafeEval: true },
  });
  if (method === 'resources/list') {
    return {
      ...result,
      resources: result.resources?.map(resource => resource.uri === panelUri
        ? { ...resource, _meta: panelMetadata(resource._meta) } : resource),
    };
  }
  if (method === 'resources/read' && params?.uri === panelUri) {
    return {
      ...result,
      contents: result.contents?.map(content => ({
        ...content,
        _meta: panelMetadata(content._meta),
      })),
    };
  }
  if (method === 'tools/call' && params?.name === '_editor_poll' && result?.structuredContent?.request) {
    return { ...result, _meta: { ...result._meta, 'zcode/activity': true } };
  }
  return result;
}

// 宿主能力声明只附加到 HTML 面板，编辑器资源与通用协议保持不变。
export function withPanelMetadata(result, metadata = {}) {
 const decorate = item => item.mimeType?.startsWith('text/html')
  ? {...item, _meta: {...item._meta, ...metadata}} : item;
 return {...result, ...(result.contents ? {contents: result.contents.map(decorate)} : {}),
  ...(result.resources ? {resources: result.resources.map(decorate)} : {})};
}

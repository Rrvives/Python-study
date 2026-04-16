/** 后端 API 根路径，例如 `http://127.0.0.1:8000/api` */
export function getApiBaseUrl(): string {
  // 未配置时默认走同源 `/api`，配合 Vite dev proxy 避免本地开发出现 404。
  const raw = import.meta.env.VITE_API_BASE_URL?.trim() ?? '/api'
  return raw.replace(/\/$/, '')
}

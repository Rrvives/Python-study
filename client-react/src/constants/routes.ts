/**
 * 集中维护路由 path，避免魔法字符串散落在菜单、跳转、面包屑中。
 */
export const ROUTE_PATHS = {
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  /** 访问时重定向到「用户管理」子页 */
  SYSTEM: '/system',
  SYSTEM_USERS: '/system/users',
  SYSTEM_MENU_MANAGEMENT: '/system/menu-management',
  AUDIT_LOGS: '/audit/logs',
  AUDIT_STRATEGY: '/audit/strategy',
  GATEWAY: '/gateway',
  INTEGRATION_BACKEND_DEMO: '/integration/backend-demo',
} as const

export type RoutePath = (typeof ROUTE_PATHS)[keyof typeof ROUTE_PATHS]

/** React Router 嵌套在 `/` 下的子路由 `path`（不带前导 `/`） */
export function childRoutePath(fullPath: RoutePath): string {
  return fullPath.startsWith('/') ? fullPath.slice(1) : fullPath
}

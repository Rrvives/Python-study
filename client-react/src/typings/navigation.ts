/**
 * 后端统一下发的导航项：
 * - menu_patch: 覆盖已有菜单文案
 * - menu_extra: 追加新菜单
 * - extra_route: 追加动态路由
 */
export type RemoteNavigationItem = {
  id: string
  type: 'menu_patch' | 'menu_extra' | 'extra_route' | 'managed_menu'
  matchKey: string | null
  key: string | null
  label: string | null
  path: string | null
  componentKey: string | null
  parentKey?: string | null
  sort?: number | null
}

export type RemoteNavigationManifest = {
  version: string
  managedMenuEnabled?: boolean
  items?: RemoteNavigationItem[]
}

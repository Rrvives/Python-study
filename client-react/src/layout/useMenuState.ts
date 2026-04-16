import { useEffect, useState } from 'react'
import { ROUTE_PATHS } from '@/constants/routes'

const AUDIT_SUBMENU_KEY = 'audit'
const SYSTEM_SUBMENU_KEY = 'system'

function selectedKeysForPath(pathname: string): string[] {
  if (pathname.startsWith(ROUTE_PATHS.AUDIT_LOGS)) {
    return [ROUTE_PATHS.AUDIT_LOGS]
  }
  // 系统管理子路由：精确匹配子 path，避免前缀误匹配
  if (pathname.startsWith(ROUTE_PATHS.SYSTEM_MENU_MANAGEMENT)) {
    return [ROUTE_PATHS.SYSTEM_MENU_MANAGEMENT]
  }
  if (
    pathname.startsWith(ROUTE_PATHS.SYSTEM_USERS) ||
    pathname === ROUTE_PATHS.SYSTEM
  ) {
    return [ROUTE_PATHS.SYSTEM_USERS]
  }
  return [pathname]
}

export function useMenuState(pathname: string) {
  const [openKeys, setOpenKeys] = useState<string[]>(() => {
    const keys: string[] = []
    if (pathname.startsWith(ROUTE_PATHS.AUDIT_LOGS)) {
      keys.push(AUDIT_SUBMENU_KEY)
    }
    if (pathname.startsWith('/system')) {
      keys.push(SYSTEM_SUBMENU_KEY)
    }
    return keys
  })

  // 从其它菜单跳入系统管理时自动展开「系统管理」分组
  useEffect(() => {
    if (pathname.startsWith('/system')) {
      setOpenKeys((prev) =>
        prev.includes(SYSTEM_SUBMENU_KEY) ? prev : [...prev, SYSTEM_SUBMENU_KEY],
      )
    }
  }, [pathname])

  return {
    openKeys,
    setOpenKeys,
    selectedKeys: selectedKeysForPath(pathname),
  }
}

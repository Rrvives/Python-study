import { useContext } from 'react'
import { NavigationMenuContext } from '@/layout/navigationContext'

export function useNavigationMenuItems() {
  const ctx = useContext(NavigationMenuContext)
  if (!ctx) {
    throw new Error('useNavigationMenuItems 必须在 NavigationMenuProvider 内使用')
  }
  return ctx.menuItems
}

import { createContext } from 'react'
import type { MenuProps } from 'antd'

type MenuItem = Required<MenuProps>['items'][number]

export type NavigationMenuContextValue = {
  menuItems: MenuItem[]
}

export const NavigationMenuContext =
  createContext<NavigationMenuContextValue | null>(null)

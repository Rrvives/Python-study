import type { ReactNode } from 'react'
import type { MenuProps } from 'antd'
import { NavigationMenuContext } from '@/layout/navigationContext'

type MenuItem = Required<MenuProps>['items'][number]

export function NavigationMenuProvider({
  menuItems,
  children,
}: {
  menuItems: MenuItem[]
  children: ReactNode
}) {
  return (
    <NavigationMenuContext.Provider value={{ menuItems }}>
      {children}
    </NavigationMenuContext.Provider>
  )
}

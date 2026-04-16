import type { MenuProps } from 'antd'
import { ROUTE_PATHS } from '@/constants/routes'

type MenuItem = Required<MenuProps>['items'][number]

/** 侧栏菜单与路由 key 一致 */
export const defaultMenuItems: MenuItem[] = [
  {
    key: 'system',
    label: '系统管理',
    children: [
      { key: ROUTE_PATHS.SYSTEM_USERS, label: '用户管理' },
      { key: ROUTE_PATHS.SYSTEM_MENU_MANAGEMENT, label: '菜单管理' },
    ],
  },
]

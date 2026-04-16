import { Card, Empty } from 'antd'
import { useLocation } from 'react-router-dom'
import { ROUTE_PATHS, type RoutePath } from '@/constants/routes'

const TITLES: Partial<Record<RoutePath, string>> = {
  [ROUTE_PATHS.DASHBOARD]: '首页',
  [ROUTE_PATHS.SYSTEM]: '系统管理',
  [ROUTE_PATHS.SYSTEM_USERS]: '用户管理',
  [ROUTE_PATHS.SYSTEM_MENU_MANAGEMENT]: '菜单管理',
  [ROUTE_PATHS.AUDIT_STRATEGY]: '审计策略',
  [ROUTE_PATHS.GATEWAY]: '网关配置',
  [ROUTE_PATHS.INTEGRATION_BACKEND_DEMO]: '后端动态路由（示例）',
}

export default function PlaceholderPage() {
  const { pathname } = useLocation()
  const title = TITLES[pathname as RoutePath] ?? '页面'

  return (
    <div style={{ padding: 16 }}>
      <Card title={title}>
        <Empty description="示例布局占位页" />
      </Card>
    </div>
  )
}

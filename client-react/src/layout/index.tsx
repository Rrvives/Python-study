import { useState } from 'react'
import { Navigate, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { Layout, theme } from 'antd'
import type { MenuProps } from 'antd'
import { ROUTE_PATHS } from '@/constants/routes'
import { useAuth } from '@/hooks/useAuth'
import { useUserStore } from '@/store'
import { Header } from '@/layout/Header'
import { Sidebar } from '@/layout/Sidebar'
import { useNavigationMenuItems } from '@/layout/useNavigationMenuItems'
import { useMenuState } from '@/layout/useMenuState'

const { Content } = Layout

export default function MainLayout() {
  const menuItems = useNavigationMenuItems()
  const { username, clearAuth } = useAuth()
  const [collapsed, setCollapsed] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { token } = theme.useToken()
  const { openKeys, setOpenKeys, selectedKeys } = useMenuState(location.pathname)

  const onMenuClick: MenuProps['onClick'] = (e) => {
    if (typeof e.key === 'string' && e.key.startsWith('/')) {
      navigate(e.key)
    }
  }

  const onLogout = () => {
    clearAuth()
    useUserStore.getState().setDisplayName(null)
    useUserStore.getState().setAuthFlags({})
    navigate(ROUTE_PATHS.LOGIN, { replace: true })
  }

  if (!username) {
    return <Navigate to={ROUTE_PATHS.LOGIN} replace />
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sidebar
        collapsed={collapsed}
        onCollapse={setCollapsed}
        menuItems={menuItems}
        openKeys={openKeys}
        onOpenChange={setOpenKeys}
        selectedKeys={selectedKeys}
        onMenuClick={onMenuClick}
      />
      <Layout>
        <Header username={username} onLogout={onLogout} />
        <Content
          style={{
            margin: 0,
            minHeight: 280,
            background: token.colorBgLayout,
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}

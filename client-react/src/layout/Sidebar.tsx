import type { MenuProps } from 'antd'
import { Layout, Menu } from 'antd'

const { Sider } = Layout

type SidebarProps = {
  collapsed: boolean
  onCollapse: (v: boolean) => void
  menuItems: MenuProps['items']
  openKeys: string[]
  onOpenChange: (keys: string[]) => void
  selectedKeys: string[]
  onMenuClick: MenuProps['onClick']
}

export function Sidebar({
  collapsed,
  onCollapse,
  menuItems,
  openKeys,
  onOpenChange,
  selectedKeys,
  onMenuClick,
}: SidebarProps) {
  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={onCollapse}
      theme="dark"
      width={220}
      style={{ background: '#001529' }}
    >
      <div
        style={{
          height: 48,
          margin: 12,
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'flex-start',
          color: '#fff',
          fontWeight: 600,
          fontSize: collapsed ? 12 : 14,
          lineHeight: 1.2,
          paddingInline: collapsed ? 0 : 8,
        }}
      >
        {collapsed ? '网关' : '数据交换网关'}
      </div>
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={selectedKeys}
        openKeys={openKeys}
        onOpenChange={onOpenChange}
        items={menuItems}
        onClick={onMenuClick}
        style={{ borderRight: 0 }}
      />
    </Sider>
  )
}

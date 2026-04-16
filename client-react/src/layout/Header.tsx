import {
  ApiOutlined,
  LogoutOutlined,
  SearchOutlined,
  UserOutlined,
} from '@ant-design/icons'
import { Layout, Space, Typography } from 'antd'

const { Header: AntHeader } = Layout
const { Text } = Typography

type HeaderProps = {
  username?: string | null
  onLogout?: () => void
}

export function Header({ username, onLogout }: HeaderProps) {
  return (
    <AntHeader
      style={{
        padding: '0 24px',
        background: '#0d3d7a',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: 56,
        lineHeight: '56px',
      }}
    >
      <Text style={{ color: '#fff', fontSize: 16, fontWeight: 500 }}>
        网通S01-数据服务隔离交换网关
      </Text>
      <Space size="middle" style={{ color: 'rgba(255,255,255,0.85)' }}>
        <SearchOutlined style={{ fontSize: 16, cursor: 'pointer' }} />
        <Space size={4}>
          <ApiOutlined />
          <span style={{ fontSize: 13 }}>已连接</span>
        </Space>
        <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 13 }}>
          V1.0.0
        </Text>
        <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 13 }}>
          192.168.1.101
        </Text>
        <Space size={4}>
          <UserOutlined style={{ fontSize: 16 }} />
          <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 13 }}>
            {username || '访客'}
          </Text>
        </Space>
        <LogoutOutlined
          style={{ fontSize: 16, cursor: 'pointer' }}
          onClick={onLogout}
          title="退出登录"
        />
      </Space>
    </AntHeader>
  )
}

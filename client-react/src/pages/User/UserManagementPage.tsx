import { Card, Typography } from 'antd'
import { UserList } from '@/pages/User/UserList'

const { Title, Paragraph } = Typography

/** 用户管理：增删改用户、分配 Django Group、设置密码 */
export default function UserManagementPage() {
  return (
    <div style={{ padding: 16 }}>
      <Title level={4} style={{ marginTop: 0 }}>
        用户管理
      </Title>
      <Paragraph type="secondary" style={{ marginBottom: 16 }}>
        创建用户、设置密码，并通过「角色」绑定到 Django 用户组；路由可见性由组与导航配置共同决定。
      </Paragraph>
      <Card variant="borderless">
        <UserList />
      </Card>
    </div>
  )
}

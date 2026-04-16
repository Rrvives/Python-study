import { Card, Typography } from 'antd'

const { Title, Paragraph } = Typography

export default function DashboardPage() {
  return (
    <div style={{ padding: 16 }}>
      <Card>
        <Title level={4}>仪表盘</Title>
        <Paragraph>在「首页」菜单下可替换为真实仪表盘内容。</Paragraph>
      </Card>
    </div>
  )
}

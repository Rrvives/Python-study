import { useState } from 'react'
import { Button, Card, Form, Input, Typography, message } from 'antd'
import { useNavigate } from 'react-router-dom'
import { loginApi } from '@/api/auth'
import { getApiBaseUrl } from '@/constants/config'
import { ROUTE_PATHS } from '@/constants/routes'
import { useAuth } from '@/hooks/useAuth'
import { useUserStore } from '@/store'
import { ApiError } from '@/utils/ApiError'

const { Title, Paragraph } = Typography

type LoginFormValues = {
  username: string
  password: string
}

export default function LoginPage() {
  const navigate = useNavigate()
  const { setToken, setUsername } = useAuth()
  const setDisplayName = useUserStore((s) => s.setDisplayName)
  const [submitting, setSubmitting] = useState(false)

  const handleLogin = async (values: LoginFormValues) => {
    setSubmitting(true)
    try {
      const result = await loginApi(values)
      if (!result.accessToken) {
        message.error('登录响应缺少 accessToken')
        return
      }
      setToken(result.accessToken)
      setUsername(result.username ?? values.username)
      setDisplayName(result.displayName ?? result.username ?? values.username)
      useUserStore.getState().setAuthFlags({
        isSuperuser: result.isSuperuser,
        isStaff: result.isStaff,
      })
      message.success('登录成功')
      navigate(ROUTE_PATHS.AUDIT_LOGS, { replace: true })
    } catch (err) {
      const isApiMode = Boolean(getApiBaseUrl())
      if (isApiMode) {
        const msg =
          err instanceof ApiError
            ? err.message
            : err instanceof Error
              ? err.message
              : '登录失败'
        message.error(msg)
        return
      }

      // 未配置后端地址时，降级为本地联调模式
      setToken('demo-token')
      setUsername(values.username)
      setDisplayName(values.username)
      useUserStore.getState().setAuthFlags({ isSuperuser: true, isStaff: true })
      message.warning('未配置后端登录接口，已进入联调模式')
      navigate(ROUTE_PATHS.AUDIT_LOGS, { replace: true })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#f0f2f5',
      }}
    >
      <Card style={{ width: 400 }}>
        <Title level={3} style={{ textAlign: 'center' }}>
          登录
        </Title>
        <Paragraph type="secondary" style={{ textAlign: 'center' }}>
          请输入已创建的系统账号；首次使用请先在后端创建管理员账号
        </Paragraph>
        <Form<LoginFormValues> layout="vertical" onFinish={handleLogin}>
          <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
            <Input placeholder="例如：admin" />
          </Form.Item>
          <Form.Item name="password" label="密码" rules={[{ required: true }]}>
            <Input.Password placeholder="请输入对应账号密码" />
          </Form.Item>
          <Button type="primary" htmlType="submit" block loading={submitting}>
            登录
          </Button>
        </Form>
      </Card>
    </div>
  )
}

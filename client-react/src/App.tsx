import { useEffect, useMemo, useState } from 'react'
import { ConfigProvider, Result, Spin, message } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { RouterProvider } from 'react-router-dom'
import { fetchNavigationManifestByUser } from '@/api/navigation'
import { ROUTE_PATHS } from '@/constants/routes'
import { defaultMenuItems } from '@/layout/menuConfig'
import { NavigationMenuProvider } from '@/layout/NavigationMenuProvider'
import { createAppRouter, mergeDashboardMenu } from '@/router'
import { useAppStore } from '@/store'
import { useUserStore } from '@/store'
import type { RemoteNavigationManifest } from '@/typings/navigation'
import { ApiError } from '@/utils/ApiError'
import { setUnauthorizedHandler } from '@/utils/authEvents'

type BootstrapState =
  | { status: 'loading' }
  | { status: 'ready'; manifest: RemoteNavigationManifest }
  | { status: 'error'; message: string }

export default function App() {
  const [state, setState] = useState<BootstrapState>({ status: 'loading' })
  const username = useAppStore((s) => s.username)
  const token = useAppStore((s) => s.token)
  const isSuperuser = useUserStore((s) => s.isSuperuser)

  useEffect(() => {
    setUnauthorizedHandler(() => {
      useAppStore.getState().clearAuth()
      message.warning('登录状态已失效，请重新登录')
      window.location.assign(ROUTE_PATHS.LOGIN)
    })
    return () => setUnauthorizedHandler(null)
  }, [])

  useEffect(() => {
    let cancelled = false
    fetchNavigationManifestByUser(username ?? undefined)
      .then((manifest) => {
        if (!cancelled) setState({ status: 'ready', manifest })
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          const msg =
            err instanceof ApiError
              ? err.message
              : err instanceof Error
                ? err.message
                : '导航配置加载失败'
          setState({ status: 'error', message: msg })
        }
      })
    return () => {
      cancelled = true
    }
  }, [username, token])

  const router = useMemo(() => {
    if (state.status !== 'ready') return null
    return createAppRouter(state.manifest)
  }, [state])

  const menuItems = useMemo(() => {
    if (state.status !== 'ready') return defaultMenuItems
    const managedOnly = Boolean(state.manifest.managedMenuEnabled && !isSuperuser)
    return mergeDashboardMenu(defaultMenuItems, state.manifest, { managedOnly })
  }, [state, isSuperuser])

  if (state.status === 'loading') {
    return (
      <ConfigProvider locale={zhCN}>
        <Spin size="large" fullscreen tip="加载导航与路由…" />
      </ConfigProvider>
    )
  }

  if (state.status === 'error' || !router) {
    return (
      <ConfigProvider locale={zhCN}>
        <Result
          status="error"
          title="导航加载失败"
          subTitle={state.status === 'error' ? state.message : undefined}
        />
      </ConfigProvider>
    )
  }

  return (
    <ConfigProvider locale={zhCN}>
      <NavigationMenuProvider menuItems={menuItems}>
        <RouterProvider router={router} />
      </NavigationMenuProvider>
    </ConfigProvider>
  )
}

import type { RouteObject } from 'react-router-dom'
import { Navigate } from 'react-router-dom'
import { childRoutePath, ROUTE_PATHS } from '@/constants/routes'
import { RouteSuspense } from '@/components/RouteSuspense'
import MainLayout from '@/layout'
import DashboardPage from '@/pages/Dashboard'
import LoginPage from '@/pages/Login'
import PlaceholderPage from '@/pages/Placeholder'
import MenuManagementPage from '@/pages/User/MenuManagementPage'
import SystemLayout from '@/pages/User/SystemLayout'
import UserManagementPage from '@/pages/User/UserManagementPage'
import type { RemoteNavigationManifest } from '@/typings/navigation'
import { lazyComponentFromKey } from '@/router/routeRegistry'

function normalizeRoutePath(path: string): string {
  return path.startsWith('/') ? path.slice(1) : path
}

function buildExtraRouteElements(manifest: RemoteNavigationManifest): RouteObject[] {
  const out: RouteObject[] = []
  const routeItems = (manifest.items ?? []).filter(
    (x) => x.type === 'extra_route' && x.path && x.componentKey,
  )
  for (const r of routeItems) {
    const routeId = r.id
    const routePath = r.path as string
    const componentKey = r.componentKey as string
    const Comp = lazyComponentFromKey(componentKey)
    if (!Comp) {
      console.warn(`[navigation] 跳过未知 componentKey: ${componentKey} (${routeId})`)
      continue
    }
    out.push({
      path: normalizeRoutePath(routePath),
      element: (
        <RouteSuspense>
          <Comp />
        </RouteSuspense>
      ),
    })
  }
  return out
}

function buildManagedMenuRouteElements(manifest: RemoteNavigationManifest): RouteObject[] {
  const out: RouteObject[] = []
  const staticRoutePaths = new Set([
    childRoutePath(ROUTE_PATHS.DASHBOARD),
    childRoutePath(ROUTE_PATHS.SYSTEM),
    childRoutePath(ROUTE_PATHS.SYSTEM_USERS),
    childRoutePath(ROUTE_PATHS.SYSTEM_MENU_MANAGEMENT),
    childRoutePath(ROUTE_PATHS.AUDIT_LOGS),
    childRoutePath(ROUTE_PATHS.AUDIT_STRATEGY),
    childRoutePath(ROUTE_PATHS.GATEWAY),
  ])

  const routeItems = (manifest.items ?? []).filter(
    (x) => x.type === 'managed_menu' && x.path && x.componentKey,
  )
  for (const r of routeItems) {
    const routePath = normalizeRoutePath(r.path as string)
    if (staticRoutePaths.has(routePath)) {
      continue
    }
    const componentKey = r.componentKey as string
    const Comp = lazyComponentFromKey(componentKey)
    if (!Comp) {
      console.warn(`[managed_menu] 跳过未知 componentKey: ${componentKey} (${r.id})`)
      continue
    }
    out.push({
      path: routePath,
      element: (
        <RouteSuspense>
          <Comp />
        </RouteSuspense>
      ),
    })
  }
  return out
}

export function buildRouteTree(manifest: RemoteNavigationManifest): RouteObject[] {
  const LogManagementPage = lazyComponentFromKey('audit.logs')
  if (!LogManagementPage) {
    throw new Error('缺少本地路由注册: audit.logs')
  }

  const shellChildren: RouteObject[] = [
    {
      index: true,
      element: <Navigate to={ROUTE_PATHS.AUDIT_LOGS} replace />,
    },
    {
      path: childRoutePath(ROUTE_PATHS.DASHBOARD),
      element: <DashboardPage />,
    },
    {
      path: childRoutePath(ROUTE_PATHS.SYSTEM),
      element: <SystemLayout />,
      children: [
        {
          index: true,
          element: <Navigate to={ROUTE_PATHS.SYSTEM_USERS} replace />,
        },
        {
          path: 'users',
          element: <UserManagementPage />,
        },
        {
          path: 'menu-management',
          element: <MenuManagementPage />,
        },
      ],
    },
    {
      path: childRoutePath(ROUTE_PATHS.AUDIT_LOGS),
      element: (
        <RouteSuspense>
          <LogManagementPage />
        </RouteSuspense>
      ),
    },
    {
      path: childRoutePath(ROUTE_PATHS.AUDIT_STRATEGY),
      element: <PlaceholderPage />,
    },
    {
      path: childRoutePath(ROUTE_PATHS.GATEWAY),
      element: <PlaceholderPage />,
    },
    ...buildExtraRouteElements(manifest),
    ...buildManagedMenuRouteElements(manifest),
  ]

  return [
    {
      path: ROUTE_PATHS.LOGIN,
      element: <LoginPage />,
    },
    {
      path: '/',
      element: <MainLayout />,
      children: shellChildren,
    },
  ]
}

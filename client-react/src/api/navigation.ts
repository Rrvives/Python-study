import { childRoutePath, ROUTE_PATHS } from '@/constants/routes'
import { getApiBaseUrl } from '@/constants/config'
import type { RemoteNavigationManifest } from '@/typings/navigation'
import { request } from '@/utils/request'

const MOCK_DELAY_MS = 280

function getMockNavigationManifest(): RemoteNavigationManifest {
  return {
    version: 'mock-1',
    managedMenuEnabled: false,
    items: [
      {
        id: 'menu_patch:dashboard',
        type: 'menu_patch',
        matchKey: '/dashboard',
        key: null,
        label: '首页（后端覆盖标题示例）',
        path: null,
        componentKey: null,
      },
      {
        id: 'menu_extra:backend-demo',
        type: 'menu_extra',
        matchKey: null,
        key: ROUTE_PATHS.INTEGRATION_BACKEND_DEMO,
        label: '后端下发的菜单（示例）',
        path: null,
        componentKey: null,
      },
      {
        id: 'integration-backend-demo',
        type: 'extra_route',
        matchKey: null,
        key: null,
        label: null,
        path: childRoutePath(ROUTE_PATHS.INTEGRATION_BACKEND_DEMO),
        componentKey: 'placeholder',
      },
    ],
  }
}

export async function fetchNavigationManifest(): Promise<RemoteNavigationManifest> {
  return fetchNavigationManifestByUser()
}

export async function fetchNavigationManifestByUser(username?: string): Promise<RemoteNavigationManifest> {
  if (!getApiBaseUrl()) {
    await new Promise((r) => setTimeout(r, MOCK_DELAY_MS))
    return getMockNavigationManifest()
  }

  const res = await request.get<RemoteNavigationManifest>('/navigation/manifest', {
    params: username ? { username } : undefined,
  })
  return res.data
}

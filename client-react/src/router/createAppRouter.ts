import { createBrowserRouter } from 'react-router-dom'
import { buildRouteTree } from '@/router/buildRouteTree'
import type { RemoteNavigationManifest } from '@/typings/navigation'

export function createAppRouter(manifest: RemoteNavigationManifest) {
  return createBrowserRouter(buildRouteTree(manifest))
}

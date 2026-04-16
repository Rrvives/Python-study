import { lazy, type ComponentType, type LazyExoticComponent } from 'react'

type LazyLoader = () => Promise<{ default: ComponentType }>

export const routeModuleLoaders = {
  'audit.logs': () => import('@/pages/Audit/Logs'),
  placeholder: () => import('@/pages/Placeholder'),
} as const satisfies Record<string, LazyLoader>

export type RouteModuleKey = keyof typeof routeModuleLoaders

export function lazyComponentFromKey(
  key: string,
): LazyExoticComponent<ComponentType> | null {
  const loader = routeModuleLoaders[key as RouteModuleKey]
  if (!loader) return null
  return lazy(loader)
}

import type { MenuProps } from 'antd'
import type { RemoteNavigationManifest } from '@/typings/navigation'

type MenuItem = Required<MenuProps>['items'][number]
type BasicMenuNode = {
  key: string
  label: string
  parentKey: string | null
  sort: number
}

function cloneMenuItems(items: MenuItem[]): MenuItem[] {
  return items.map((item) => {
    if (!item || typeof item !== 'object') return item
    const base = item as { key?: string; label?: unknown; children?: MenuItem[] }
    const next: MenuItem = { ...base } as MenuItem
    if (Array.isArray(base.children)) {
      ;(next as { children?: MenuItem[] }).children = cloneMenuItems(base.children)
    }
    return next
  })
}

function applyPatches(
  items: MenuItem[],
  manifestItems: RemoteNavigationManifest['items'],
): MenuItem[] {
  const patches = (manifestItems ?? []).filter(
    (x) => x.type === 'menu_patch' && x.matchKey && x.label,
  )
  if (!patches.length) return items
  const map = new Map(patches.map((p) => [p.matchKey as string, p.label as string]))

  const walk = (nodes: MenuItem[]): MenuItem[] =>
    nodes.map((node) => {
      if (!node || typeof node !== 'object') return node
      const n = node as { key?: string; label?: unknown; children?: MenuItem[] }
      const label = n.key && map.has(n.key) ? map.get(n.key)! : n.label
      const children = n.children ? walk(n.children) : undefined
      return { ...n, label, ...(children ? { children } : {}) } as MenuItem
    })

  return walk(items)
}

function buildManagedMenuItems(manifest: RemoteNavigationManifest): MenuItem[] {
  const rows: BasicMenuNode[] = (manifest.items ?? [])
    .filter((x) => x.type === 'managed_menu' && x.key && x.label)
    .map((x) => ({
      key: x.key as string,
      label: x.label as string,
      parentKey: x.parentKey ?? null,
      sort: Number(x.sort ?? 0),
    }))
    .sort((a, b) => a.sort - b.sort || a.key.localeCompare(b.key))

  if (!rows.length) return []

  const byKey = new Map<string, BasicMenuNode>()
  for (const row of rows) {
    byKey.set(row.key, row)
  }

  const childrenMap = new Map<string, BasicMenuNode[]>()
  const roots: BasicMenuNode[] = []
  for (const row of rows) {
    if (row.parentKey && byKey.has(row.parentKey)) {
      const siblings = childrenMap.get(row.parentKey) ?? []
      siblings.push(row)
      childrenMap.set(row.parentKey, siblings)
    } else {
      roots.push(row)
    }
  }

  const toMenuItem = (node: BasicMenuNode): MenuItem => {
    const children = (childrenMap.get(node.key) ?? []).map(toMenuItem)
    if (children.length) {
      return {
        key: node.key,
        label: node.label,
        children,
      } as MenuItem
    }
    return {
      key: node.key,
      label: node.label,
    } as MenuItem
  }

  return roots.map(toMenuItem)
}

function itemKey(node: MenuItem): string | null {
  if (!node || typeof node !== 'object') return null
  const raw = (node as { key?: unknown }).key
  return typeof raw === 'string' ? raw : null
}

function mergeMenuItems(baseItems: MenuItem[], incomingItems: MenuItem[]): MenuItem[] {
  const out = cloneMenuItems(baseItems)

  const mergeChildren = (baseChildren: MenuItem[] | undefined, addChildren: MenuItem[]) => {
    if (!baseChildren?.length) return cloneMenuItems(addChildren)
    return mergeMenuItems(baseChildren, addChildren)
  }

  for (const incoming of incomingItems) {
    const incomingKey = itemKey(incoming)
    if (!incomingKey) {
      out.push(incoming)
      continue
    }
    const hitIndex = out.findIndex((x) => itemKey(x) === incomingKey)
    if (hitIndex < 0) {
      out.push(incoming)
      continue
    }

    const baseNode = out[hitIndex] as { children?: MenuItem[] }
    const addNode = incoming as { children?: MenuItem[] }
    if (Array.isArray(addNode.children) && addNode.children.length) {
      out[hitIndex] = {
        ...(baseNode as object),
        children: mergeChildren(baseNode.children, addNode.children),
      } as MenuItem
    }
  }

  return out
}

export function mergeDashboardMenu(
  localItems: MenuItem[],
  manifest: RemoteNavigationManifest,
  options?: { managedOnly?: boolean },
): MenuItem[] {
  // 叠加策略默认：保留默认菜单，再叠加 managed_menu。
  // 受控模式：仅显示 managed_menu（用于非超管按用户授权展示）。
  const managedItems = buildManagedMenuItems(manifest)
  if (options?.managedOnly) {
    return managedItems
  }

  let merged = cloneMenuItems(localItems)
  merged = applyPatches(merged, manifest.items)
  if (managedItems.length) {
    merged = mergeMenuItems(merged, managedItems)
  }

  const extras = (manifest.items ?? [])
    .filter((x) => x.type === 'menu_extra' && x.key && x.label)
    .map(
    (m) =>
      ({
        key: m.key as string,
        label: m.label as string,
      }) as MenuItem,
    )

  return extras.length ? mergeMenuItems(merged, extras) : merged
}
